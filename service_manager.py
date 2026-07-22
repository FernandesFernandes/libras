import queue

from audio.capture import AudioCapture
from stt.transcriber import Transcriber
from storage.transcript_writer import TranscriptWriter


class ServiceManager:

    def __init__(self):

        self.running = False

        # Fila de áudio capturado pelo microfone / entrada de áudio
        self.audio_queue = queue.Queue()

        # Fila usada pela interface Tkinter para exibir o texto
        self.text_queue = queue.Queue()

        # Fila usada para salvar as transcrições em arquivo
        self.writer_queue = queue.Queue()

        self.capture = AudioCapture(
            self.audio_queue
        )

        self.transcriber = Transcriber(
            audio_queue=self.audio_queue,
            text_queue=self.text_queue,
            writer_queue=self.writer_queue
        )

        self.writer = TranscriptWriter(
            writer_queue=self.writer_queue,
            output_file="transcriptions.jsonl"
        )

    def clear_queue(self, q):

        try:

            while not q.empty():
                q.get_nowait()

        except queue.Empty:
            pass

    def start(self):

        if self.running:
            return

        self.running = True

        self.clear_queue(
            self.audio_queue
        )

        self.clear_queue(
            self.text_queue
        )

        self.clear_queue(
            self.writer_queue
        )

        self.writer.start()

        self.transcriber.start()

        self.capture.start()

        print(
            "[SERVICE] Sistema iniciado"
        )

    def stop(self):

        if not self.running:
            return

        self.running = False

        self.capture.stop()

        self.transcriber.stop()

        self.writer.stop()

        print(
            "[SERVICE] Sistema encerrado"
        )