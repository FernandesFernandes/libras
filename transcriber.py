# stt/transcriber.py

import threading
import queue
import time
import numpy as np

from faster_whisper import WhisperModel


class Transcriber:

    def __init__(
        self,
        audio_queue,
        text_queue,
        writer_queue
    ):

        self.audio_queue = audio_queue
        self.text_queue = text_queue
        self.writer_queue = writer_queue

        self.running = False

        self.thread = None

        self.sample_rate = 16000

        # 144000 amostras = aproximadamente 9 segundos em 16kHz
        self.min_samples_to_transcribe = 144000

        print(
            "[WHISPER] Carregando modelo..."
        )

        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

        print(
            "[WHISPER] Modelo carregado"
        )

    def transcribe_audio(
        self,
        audio
    ):

        audio_seconds = len(audio) / self.sample_rate

        inicio = time.perf_counter()

        segments, info = self.model.transcribe(
            audio,
            language="pt",
            beam_size=1
        )

        texto = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        fim = time.perf_counter()

        processamento = fim - inicio

        if audio_seconds > 0:
            rtf = processamento / audio_seconds
        else:
            rtf = 0

        print(
            "[METRICA] "
            f"audio={audio_seconds:.2f}s | "
            f"processamento={processamento:.2f}s | "
            f"RTF={rtf:.2f}"
        )

        return texto

    def worker(self):

        buffer = []

        while self.running:

            try:

                chunk = self.audio_queue.get(
                    timeout=1
                )

                buffer.append(
                    chunk.flatten()
                )

                total_samples = sum(
                    len(x)
                    for x in buffer
                )

                if total_samples < self.min_samples_to_transcribe:
                    continue

                audio = np.concatenate(
                    buffer
                ).astype(
                    np.float32
                )

                buffer.clear()

                print(
                    "[WHISPER] Transcrevendo..."
                )

                texto = self.transcribe_audio(
                    audio
                )

                if texto:

                    print(
                        f"[TEXTO] {texto}"
                    )

                    # Envia para a interface Tkinter
                    self.text_queue.put(
                        texto
                    )

                    # Envia para o TranscriptWriter salvar em arquivo
                    self.writer_queue.put(
                        texto
                    )

            except queue.Empty:

                pass

            except Exception as e:

                print(
                    "[WHISPER][ERRO]",
                    e
                )

        # Ao encerrar, tenta processar algum áudio pendente
        if buffer:

            try:

                audio = np.concatenate(
                    buffer
                ).astype(
                    np.float32
                )

                print(
                    "[WHISPER] Transcrevendo bloco final..."
                )

                texto = self.transcribe_audio(
                    audio
                )

                if texto:

                    print(
                        f"[TEXTO FINAL] {texto}"
                    )

                    self.text_queue.put(
                        texto
                    )

                    self.writer_queue.put(
                        texto
                    )

            except Exception as e:

                print(
                    "[WHISPER][ERRO FINAL]",
                    e
                )

        print(
            "[WHISPER] Worker encerrado"
        )

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
            "[WHISPER] Iniciado"
        )

    def stop(self):

        if not self.running:
            return

        self.running = False

        print(
            "[WHISPER] Encerrando..."
        )