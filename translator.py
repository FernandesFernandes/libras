import json
import time
import os
import hashlib

from libras.glosa_generator import GlosaGenerator


class Translator:

    def __init__(
        self,
        input_file="transcriptions.jsonl",
        output_file="glosas.jsonl",
        process_existing=True
    ):

        self.input_file = input_file
        self.output_file = output_file

        self.process_existing = process_existing

        self.last_position = 0

        self.glosa_generator = GlosaGenerator()

        # Não usar apenas ID, porque seu histórico tem IDs repetidos.
        self.processed_keys = set()

        self.load_processed_keys()

        if not self.process_existing:
            self.move_to_end_of_input_file()

    # ======================================================
    # CHAVE ÚNICA SEGURA
    # ======================================================

    def build_key_from_values(
        self,
        timestamp,
        texto
    ):

        raw = f"{timestamp}|{texto}"

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

    def build_key_from_input_item(
        self,
        item
    ):

        timestamp = item.get(
            "timestamp",
            ""
        )

        texto = item.get(
            "texto",
            ""
        )

        return self.build_key_from_values(
            timestamp,
            texto
        )

    def build_key_from_output_item(
        self,
        item
    ):

        timestamp = item.get(
            "timestamp",
            ""
        )

        texto = item.get(
            "texto_original",
            ""
        )

        return self.build_key_from_values(
            timestamp,
            texto
        )

    # ======================================================
    # CARREGA GLOSAS JÁ PROCESSADAS
    # ======================================================

    def load_processed_keys(self):

        if not os.path.exists(
            self.output_file
        ):
            return

        try:

            with open(
                self.output_file,
                "r",
                encoding="utf-8"
            ) as file:

                for line in file:

                    line = line.strip()

                    if not line:
                        continue

                    try:

                        item = json.loads(
                            line
                        )

                    except json.JSONDecodeError:
                        continue

                    key = self.build_key_from_output_item(
                        item
                    )

                    self.processed_keys.add(
                        key
                    )

            print(
                f"[LIBRAS] Glosas já processadas carregadas: {len(self.processed_keys)}"
            )

        except Exception as e:

            print(
                "[LIBRAS][ERRO AO CARREGAR PROCESSADOS]",
                e
            )

    # ======================================================
    # INICIAR NO FIM DO ARQUIVO
    # ======================================================

    def move_to_end_of_input_file(self):

        if not os.path.exists(
            self.input_file
        ):
            self.last_position = 0
            return

        self.last_position = os.path.getsize(
            self.input_file
        )

        print(
            f"[LIBRAS] Iniciando apenas com novas linhas. Posição={self.last_position}"
        )

    # ======================================================
    # TRADUZ TEXTO PARA GLOSA
    # ======================================================

    def to_glosa(
        self,
        texto
    ):

        return self.glosa_generator.translate(
            texto
        )

    # ======================================================
    # VERIFICA PROCESSAMENTO
    # ======================================================

    def already_processed(
        self,
        item
    ):

        key = self.build_key_from_input_item(
            item
        )

        return key in self.processed_keys

    def mark_processed(
        self,
        item
    ):

        key = self.build_key_from_input_item(
            item
        )

        self.processed_keys.add(
            key
        )

    # ======================================================
    # MONTA SAÍDA
    # ======================================================

    def build_output(
        self,
        item,
        glosa
    ):

        return {
            "id": item.get("id"),
            "timestamp": item.get("timestamp"),
            "texto_original": item.get("texto", ""),
            "glosa": glosa
        }

    # ======================================================
    # GRAVA SAÍDA
    # ======================================================

    def write_output(
        self,
        output
    ):

        with open(
            self.output_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(
                    output,
                    ensure_ascii=False
                )
                + "\n"
            )

    # ======================================================
    # PROCESSA ITEM
    # ======================================================

    def process_item(
        self,
        item
    ):

        if self.already_processed(
            item
        ):
            return

        texto = item.get(
            "texto",
            ""
        ).strip()

        if not texto:
            return

        glosa = self.to_glosa(
            texto
        )

        if not glosa:
            return

        output = self.build_output(
            item,
            glosa
        )

        self.write_output(
            output
        )

        self.mark_processed(
            item
        )

        print(
            f"[LIBRAS] ID={item.get('id')} traduzido"
        )

        print(
            f"[GLOSA] {glosa}"
        )

    # ======================================================
    # LÊ LINHAS NOVAS
    # ======================================================

    def read_new_lines(self):

        if not os.path.exists(
            self.input_file
        ):
            return []

        current_size = os.path.getsize(
            self.input_file
        )

        # Se o arquivo foi apagado/recriado/truncado,
        # a posição antiga fica inválida.
        if current_size < self.last_position:

            print(
                "[LIBRAS] Arquivo de transcrição reiniciado. Resetando posição."
            )

            self.last_position = 0

        with open(
            self.input_file,
            "r",
            encoding="utf-8"
        ) as file:

            file.seek(
                self.last_position
            )

            lines = file.readlines()

            self.last_position = file.tell()

        return lines

    # ======================================================
    # LOOP PRINCIPAL
    # ======================================================

    def run(self):

        print(
            "[LIBRAS] Monitor iniciado"
        )

        print(
            f"[LIBRAS] Lendo arquivo: {self.input_file}"
        )

        print(
            f"[LIBRAS] Gravando arquivo: {self.output_file}"
        )

        print(
            f"[LIBRAS] Processar histórico existente: {self.process_existing}"
        )

        while True:

            try:

                lines = self.read_new_lines()

                for line in lines:

                    line = line.strip()

                    if not line:
                        continue

                    try:

                        item = json.loads(
                            line
                        )

                    except json.JSONDecodeError:

                        print(
                            "[LIBRAS][ERRO] Linha inválida ignorada"
                        )

                        continue

                    self.process_item(
                        item
                    )

            except Exception as e:

                print(
                    "[LIBRAS][ERRO]",
                    e
                )

            time.sleep(
                1
            )