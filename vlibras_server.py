import json
import threading
import webbrowser

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


# ==========================================================
# ESTADO DO VLIBRAS
# ==========================================================

class VLibrasState:

    def __init__(self):

        self.history = []

        # quantidade máxima de frases
        self.max_history = 20

        self.lock = threading.Lock()
                
        self.current_payload = {
            "id": None,
            "timestamp": None,
            "texto_original": "",
            "texto_atual": "",
            "glosa": ""
        }


    def set_payload(
        self,
        payload
    ):

        texto = payload.get(
            "texto_original",
            ""
        ).strip()

        if not texto:
            return

        with self.lock:

            self.current_payload = {
                "id": payload.get("id"),

                "timestamp":
                    payload.get(
                        "timestamp"
                    ),

                "texto_original":
                    texto,

                "texto_atual":
                    payload.get(
                        "texto_atual",
                        ""
                    ),

                "glosa":
                    payload.get(
                        "glosa",
                        ""
                    )
            }

            texto_normalizado = (
                texto
                .strip()
                .lower()
            )

            historico_normalizado = [
                item.strip().lower()
                for item in self.history
            ]

            if texto_normalizado in historico_normalizado:
                return

            self.history.append(
                texto
            )

            self.history = self.history[
                -self.max_history:
            ]

    def get_payload(
        self
):

        with self.lock:

            return {

                "id":
                    self.current_payload.get(
                        "id"
                    ),

                "timestamp":
                    self.current_payload.get(
                        "timestamp"
                    ),

                "texto_original":
                    "\n\n".join(
                        self.history
                    ),

                "texto_atual":
                    self.current_payload.get(
                        "texto_atual",
                        ""
                    ),

                "glosa":
                    self.current_payload.get(
                        "glosa",
                        ""
                    )
            }


# ==========================================================
# HTTP HANDLER
# ==========================================================

class VLibrasRequestHandler(
    BaseHTTPRequestHandler
):

    state = None

    def log_message(
        self,
        format,
        *args
    ):
        return

    def send_json(
        self,
        data,
        status=200
    ):

        body = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(
            status
        )

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.end_headers()

        self.wfile.write(
            body
        )

    def send_html(
        self,
        html,
        status=200
    ):

        body = html.encode(
            "utf-8"
        )

        self.send_response(
            status
        )

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.end_headers()

        self.wfile.write(
            body
        )

    def do_GET(
        self
    ):

        if self.path == "/":

            self.send_html(
                self.build_page()
            )

            return

        if self.path == "/api/current":

            payload = self.state.get_payload()

            self.send_json(
                payload
            )

            return

        self.send_json(
            {
                "error": "not_found"
            },
            status=404
        )

    def build_page(
        self
    ):

        return """
<!DOCTYPE html>
<html lang="pt-BR">

<head>

<meta charset="UTF-8">

<title>VLibras - Culto ao Vivo</title>

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
/>

<style>

body{
    font-family:Arial,sans-serif;
    background:#111827;
    color:#f9fafb;
    margin:0;
    padding:0;
}

.container{
    max-width:1200px;
    margin:0 auto;
    padding:32px;
}

.title{
    font-size:40px;
    font-weight:bold;
}

.subtitle{
    color:#9ca3af;
    margin-top:10px;
    margin-bottom:20px;
}

.card{
    background:#1f2937;
    border-radius:16px;
    padding:24px;
    margin-bottom:20px;
}

.label{
    font-size:14px;
    color:#9ca3af;
    margin-bottom:10px;
    text-transform:uppercase;
}

#texto-original{

    max-height:500px;

    overflow-y:auto;

    font-size:30px;

    line-height:1.6;

    white-space:pre-wrap;
}

#glosa{

    font-size:20px;

    color:#93c5fd;

    white-space:pre-wrap;
}

.meta{

    margin-top:10px;

    font-size:13px;

    color:#6b7280;
}

.hint{

    background:#0f172a;

    border-left:4px solid #3b82f6;

    border-radius:8px;

    padding:15px;
}

</style>

</head>

<body>

<div class="container">

    <div class="title">
        Tradutor Libras - Culto ao Vivo
    </div>

    <div class="subtitle">
        Histórico acumulado das últimas frases reconhecidas.
    </div>

    <div class="card">

        <div class="label">
            Texto Original
        </div>

        <div id="texto-original">

            <div id="vlibras-target">
                Aguardando transcrição...
            </div>

        </div>

        <div
            class="meta"
            id="meta"
        ></div>

    </div>

    <div class="card">

        <div class="label">
            Última Glosa
        </div>

        <div id="glosa">
            Aguardando glosa...
        </div>

    </div>

    <div class="hint">

        Histórico das últimas frases recebidas.

        O VLibras normalmente funciona melhor
        com texto contínuo do que com frases
        substituídas constantemente.

    </div>

</div>

<!-- VLibras -->

<div vw class="enabled">

    <div
        vw-access-button
        class="active">
    </div>

    <div vw-plugin-wrapper>

        <div
            class="vw-plugin-top-wrapper">
        </div>

    </div>

</div>

<script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>

<script>

new window.VLibras.Widget(
    "https://vlibras.gov.br/app"
);

function keepFeedbackCollapsed() {

    const feedbackPanel =
        document.querySelector(
            ".vp-rate-box-header"
        )?.parentElement;

    if (!feedbackPanel) {
        return;
    }

    feedbackPanel.style.height =
        "48px";

    feedbackPanel.style.maxHeight =
        "48px";

    feedbackPanel.style.minHeight =
        "48px";

    feedbackPanel.style.overflow =
        "hidden";

    const content =
        feedbackPanel.querySelector(
            ".vp-rate-box-content"
        );

    if (content) {

        content.style.height =
            "0px";        
    }
}

setInterval(
    keepFeedbackCollapsed,
    500
);
</script>

<script>

let lastText = "";
let lastAutoTranslated = "";

function autoTranslateVLibras(texto){

    if (!texto){
        return;
    }

    if (
        texto === lastAutoTranslated
    ){
        return;
    }

    const textarea =
        document.querySelectorAll(
            ".vp-user-textarea"
        )[0];

    const button =
        document.querySelector(
            ".vp-play-gloss-button"
        );

    if (
        !textarea ||
        !button
    ){
        return;
    }

    textarea.focus();

    textarea.value =
        texto;

    textarea.dispatchEvent(
        new Event(
            "input",
            {
                bubbles:true
            }
        )
    );

    textarea.dispatchEvent(
        new Event(
            "change",
            {
                bubbles:true
            }
        )
    );

    setTimeout(
        () => {

            button.click();

            lastAutoTranslated =
                texto;

            setTimeout(
                keepFeedbackCollapsed,
                500
            );

            setTimeout(
                keepFeedbackCollapsed,
                1000
            );

            setTimeout(
                keepFeedbackCollapsed,
                1500
            );

        },
        300
    );
}

async function loadCurrent() {

    try {

        const response =
            await fetch(
                "/api/current"
            );

        const data =
            await response.json();

        const textoHistorico =
            data.texto_original || "";

        const textoAtual =
            data.texto_atual || "";

        const glosa =
            data.glosa || "";

        const id =
            data.id;

        const timestamp =
            data.timestamp || "";

        if (
            textoHistorico &&
            textoHistorico !== lastText
        ) {

            const container =
                document.getElementById(
                    "vlibras-target"
                );

            container.innerText =
                textoHistorico;

            document.getElementById(
                "glosa"
            ).innerText =
                glosa;

            document.getElementById(
                "meta"
            ).innerText =
                "ID: "
                + id
                + " | "
                + timestamp;

            container.scrollTop =
                container.scrollHeight;

            lastText =
                textoHistorico;

            autoTranslateVLibras(
                glosa || textoAtual
            );
        }

    }
    catch(error){

        console.error(
            "[AUTO_VLIBRAS]",
            error
        );
    }
}

setInterval(
    loadCurrent,
    500
);

loadCurrent();

</script>

</body>
</html>
        """


# ==========================================================
# SERVIDOR
# ==========================================================

class VLibrasServer:

    def __init__(
        self,
        host="127.0.0.1",
        port=8765,
        auto_open_browser=True
    ):

        self.host = host
        self.port = port
        self.auto_open_browser = auto_open_browser

        self.state = VLibrasState()

        self.httpd = None
        self.thread = None

        self.running = False

    def set_payload(
        self,
        payload
    ):

        self.state.set_payload(
            payload
        )

    def start(
        self
    ):

        if self.running:
            return

        self.running = True

        VLibrasRequestHandler.state = (
            self.state
        )

        self.httpd = HTTPServer(
            (
                self.host,
                self.port
            ),
            VLibrasRequestHandler
        )

        self.thread = threading.Thread(
            target=self.httpd.serve_forever,
            daemon=True
        )

        self.thread.start()

        url = (
            f"http://{self.host}:{self.port}"
        )

        print(
            f"[VLIBRAS_SERVER] Servidor iniciado em {url}"
        )

        if self.auto_open_browser:

            webbrowser.open(
                url
            )

    def stop(
        self
    ):

        if not self.running:
            return

        self.running = False

        if self.httpd:

            self.httpd.shutdown()

            self.httpd.server_close()

        print(
            "[VLIBRAS_SERVER] Servidor encerrado"
        )