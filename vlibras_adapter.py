# avatar/vlibras_adapter.py

import threading
import queue

from avatar.vlibras_server import VLibrasServer


class VLibrasAdapter:

    def __init__(
        self,
        avatar_queue,
        host="127.0.0.1",
        port=8765
    ):

        self.avatar_queue = avatar_queue

        self.running = False
        self.thread = None

        self.server = VLibrasServer(
            host=host,
            port=port,
            auto_open_browser=True
        )

        self.processed_count = 0

    def process_payload(
        self,
        payload
    ):

        texto_original = (
            payload.get(
                "texto_original",
                ""
            ).strip()
        )

        glosa = (
            payload.get(
                "glosa",
                ""
            ).strip()
        )

        if not texto_original and not glosa:

            print(
                "[VLIBRAS] Payload vazio ignorado."
            )

            return

        # =====================================
        # IMPORTANTE:
        # texto_original -> histórico exibido
        # texto_atual    -> enviado ao VLibras
        # =====================================

        vlibras_payload = {

            "id":
                payload.get(
                    "id"
                ),

            "timestamp":
                payload.get(
                    "timestamp"
                ),

            "texto_original":
                texto_original,

            # O VLibras vai traduzir a glosa
            "texto_atual":
                glosa,

            "glosa":
                glosa
        }

        self.server.set_payload(
            vlibras_payload
        )

        self.processed_count += 1

        print()
        print("=" * 80)

        print(
            f"[VLIBRAS] ID={payload.get('id')}"
        )

        print(
            f"[VLIBRAS] Texto: {texto_original}"
        )

        print(
            f"[VLIBRAS] Glosa enviada ao avatar: {glosa}"
        )

        print(
            f"[VLIBRAS] Total sessão: {self.processed_count}"
        )

        print("=" * 80)

    def worker(
        self
    ):

        print(
            "[VLIBRAS] Worker iniciado"
        )

        while self.running:

            try:

                payload = (
                    self.avatar_queue.get(
                        timeout=1
                    )
                )

                self.process_payload(
                    payload
                )

            except queue.Empty:

                continue

            except Exception as e:

                print(
                    "[VLIBRAS][ERRO]",
                    e
                )

        print(
            "[VLIBRAS] Worker encerrado"
        )

    def start(
        self
    ):

        if self.running:
            return

        self.running = True

        self.server.start()

        self.thread = threading.Thread(
            target=self.worker,
            daemon=True
        )

        self.thread.start()

        print(
            "[VLIBRAS] Adapter iniciado"
        )

    def stop(
        self
    ):

        if not self.running:
            return

        self.running = False

