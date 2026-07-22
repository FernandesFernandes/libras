import sounddevice as sd
import queue


class AudioCapture:

    def __init__(self, audio_queue):

        self.audio_queue = audio_queue
        self.stream = None

    def callback(self, indata, frames, time, status):

        if status:
            print(status)

        self.audio_queue.put(indata.copy())

    def start(self):

        print("[CAPTURE] Iniciando microfone...")

        self.stream = sd.InputStream(
            samplerate=16000,
            channels=1,
            callback=self.callback
        )

        self.stream.start()

    def stop(self):

        print("[CAPTURE] Parando microfone...")

        if self.stream:
            self.stream.stop()
            self.stream.close()