import json
import os
import threading
import time


class GlosaReader:

    def __init__(
        self,
        avatar_queue,
        input_file="glosas.jsonl"
    ):

        self.avatar_queue = avatar_queue
        self.input_file = input_file

        self.running = False
        self.thread = None

        self.last_position = 0
        self.processed_ids = set()

    # ==================================================
    # LÊ NOVAS LINHAS
    # ==================================================

    def read_new_lines(
        self
    ):

        if not os.path.exists(
            self.input_file
        ):
            return []

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

    # ==================================================
    # PROCESSA ITEM
    # ==================================================

    def process_item(
        self,
        item
    ):

        item_id = item.get(
            "id"
        )

        if item_id in self.processed_ids:
            return

        glosa = item.get(
            "glosa",
            ""
        ).strip()

        if not glosa:
            return

        payload = {
            "id": item_id,
            "timestamp": item.get("timestamp"),
            "texto_original": item.get("texto_original"),
            "glosa": glosa
        }

        self.avatar_queue.put(
            payload
        )

        if item_id is not None:
            self.processed_ids.add(
                item_id
            )

        print(
            f"[GLOSA_READER] Enviado para avatar ID={item_id}"
        )

    # ==================================================
    # LOOP
    # ==================================================

    def worker(
        self
    ):

        print(
            f"[GLOSA_READER] Monitorando arquivo: {self.input_file}"
        )

        while self.running:

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
                            "[GLOSA_READER][ERRO] Linha inválida ignorada"
                        )

                        continue

                    self.process_item(
                        item
                    )

            except Exception as e:

                print(
                    "[GLOSA_READER][ERRO]",
                    e
                )

            time.sleep(
                1
            )

        print(
            "[GLOSA_READER] Worker encerrado"
        )

    # ==================================================
    # START
    # ==================================================

    def start(
        self
    ):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.worker,
            daemon=True
        )

        self.thread.start()

        print(
            "[GLOSA_READER] Iniciado"
        )

    # ==================================================
    # STOP
    # ==================================================

    def stop(
        self
    ):

        if not self.running:
            return

        self.running = False

        print(
            "[GLOSA_READER] Encerrando..."
        )