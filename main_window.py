import tkinter as tk

from services.service_manager import ServiceManager


class MainWindow:

    def __init__(self):

        self.service = ServiceManager()

        self.root = tk.Tk()

        self.root.title(
            "Tradutor Libras"
        )

        self.root.geometry(
            "900x600"
        )

        # ==================================================
        # TÍTULO
        # ==================================================

        self.title_label = tk.Label(
            self.root,
            text="Tradutor Português → Libras",
            font=("Arial", 18, "bold")
        )

        self.title_label.pack(
            pady=15
        )

        # ==================================================
        # STATUS
        # ==================================================

        self.status_label = tk.Label(
            self.root,
            text="Status: PARADO",
            fg="red",
            font=("Arial", 14, "bold")
        )

        self.status_label.pack(
            pady=10
        )

        # ==================================================
        # TÍTULO TRANSCRIÇÃO
        # ==================================================

        self.transcricao_title = tk.Label(
            self.root,
            text="Transcrição em Tempo Real",
            font=("Arial", 12, "bold")
        )

        self.transcricao_title.pack(
            pady=(20, 5)
        )

        # ==================================================
        # ÁREA DE TEXTO
        # ==================================================

        self.transcricao_text = tk.Text(
            self.root,
            width=100,
            height=20,
            font=("Consolas", 11)
        )

        self.transcricao_text.pack(
            padx=10,
            pady=5,
            fill="both",
            expand=True
        )

        # ==================================================
        # SCROLLBAR
        # ==================================================

        scrollbar = tk.Scrollbar(
            self.transcricao_text
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.transcricao_text.config(
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(
            command=self.transcricao_text.yview
        )

        # ==================================================
        # FRAME DOS BOTÕES
        # ==================================================

        button_frame = tk.Frame(
            self.root
        )

        button_frame.pack(
            pady=20
        )

        self.btn_start = tk.Button(
            button_frame,
            text="INICIAR",
            bg="green",
            fg="white",
            width=20,
            height=2,
            command=self.start
        )

        self.btn_start.grid(
            row=0,
            column=0,
            padx=10
        )

        self.btn_stop = tk.Button(
            button_frame,
            text="ENCERRAR",
            bg="red",
            fg="white",
            width=20,
            height=2,
            command=self.stop
        )

        self.btn_stop.grid(
            row=0,
            column=1,
            padx=10
        )

        # inicia monitor da fila
        self.update_transcription()

    # ======================================================
    # INICIAR
    # ======================================================

    def start(self):

        self.transcricao_text.delete(
            "1.0",
            tk.END
        )

        self.service.start()

        self.status_label.config(
            text="Status: EXECUTANDO",
            fg="green"
        )

    # ======================================================
    # PARAR
    # ======================================================

    def stop(self):

        self.service.stop()

        self.status_label.config(
            text="Status: PARADO",
            fg="red"
        )

    # ======================================================
    # MONITORA FILA DE TRANSCRIÇÕES
    # ======================================================

    def update_transcription(self):

        try:

            while not self.service.text_queue.empty():

                texto = (
                    self.service.text_queue.get_nowait()
                )

                self.transcricao_text.insert(
                    tk.END,
                    texto + "\n"
                )

                self.transcricao_text.see(
                    tk.END
                )

        except Exception as e:

            print(
                "[UI ERRO]",
                e
            )

        self.root.after(
            500,
            self.update_transcription
        )

    # ======================================================
    # LOOP TKINTER
    # ======================================================

    def run(self):

        self.root.mainloop()