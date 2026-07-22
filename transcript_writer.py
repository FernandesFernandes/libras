import json
import os
import threading
import queue

from datetime import datetime


class TranscriptWriter:

    def __init__(
        self,
        writer_queue,
        output_file="transcriptions.jsonl"
    ):

        self.writer_queue = writer_queue
        self.output_file = output_file

        self.running = False
        self.thread = None

        self.next_id = self.load_next_id()

    # ======================================================
    # CARREGA PRÓXIMO ID
    # ======================================================

    def load_next_id(self):

        if not os.path.exists(self.output_file):
            return 1

        max_id = 0

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

                        item = json.loads(line)

                    except json.JSONDecodeError:
                        continue

                    item_id = item.get("id")

                    if isinstance(item_id, int):
                        max_id = max(max_id, item_id)

        except Exception as e:

            print(
                "[WRITER][ERRO AO LER IDS]",
                e
            )

        return max_id + 1

    # ======================================================
    # CRIA DOCUMENTO
    # ======================================================

    def create_document(
        self,
        texto
    ):

        texto = str(texto).strip()

        document = {
            "id": self.next_id,
            "timestamp": datetime.now().isoformat(),
            "texto": texto,
            "traduzido": False
        }

        self.next_id += 1

        return document

    # ======================================================
    # ESCREVE DOCUMENTO
    # ======================================================

    def write_document(
        self,
        document
    ):

        with open(
            self.output_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(
                    document,
                    ensure_ascii=False
                )
                + "\n"
            )

    # ======================================================
    # PROCESSA UM ITEM
    # ======================================================

    def process_text(
        self,
        texto
    ):

        texto = str(texto).strip()

        if not texto:
            return

        document = self.create_document(
            texto
        )

        self.write_document(
            document
        )

        print(
            f"[WRITER] Salvo ID={document['id']}"
        )

    # ======================================================
    # LOOP
    # ======================================================

    def worker(self):

        while self.running or not self.writer_queue.empty():

            try:

                texto = self.writer_queue.get(
                    timeout=1
                )

                self.process_text(
                    texto
                )

            except queue.Empty:

                continue

            except Exception as e:

                print(
                    "[WRITER][ERRO]",
                    e
                )

        print(
            "[WRITER] Worker encerrado"
        )

    # ======================================================
    # START
    # ======================================================

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.worker,
            daemon=True
        )

        self.thread.start()

        print(
            f"[WRITER] Iniciado. Próximo ID={self.next_id}"
        )

    # ======================================================
    # STOP
    # ======================================================

    def stop(self):

        if not self.running:
            return

        self.running = False

        print(
            "[WRITER] Encerrando..."
        )