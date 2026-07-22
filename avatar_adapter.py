import threading
import queue
import time
import json
import os

from avatar.signal_map import (
    SIGNAL_MAP,
    COMPOUND_SIGNAL_MAP
)

from avatar.token_cleaner import TokenCleaner


class AvatarAdapter:

    def __init__(
        self,
        avatar_queue,
        missing_file="missing_signals.json",
        coverage_file="coverage_report.json"
    ):

        self.avatar_queue = avatar_queue

        self.running = False
        self.thread = None

        self.missing_file = missing_file
        self.coverage_file = coverage_file

        self.cleaner = TokenCleaner()

        self.session_stats = {
            "glosas_processadas": 0,
            "tokens_totais": 0,
            "tokens_validos": 0,
            "tokens_mapeados": 0,
            "tokens_sem_mapeamento": 0,
            "tokens_ignorados_ruido": 0
        }

        self.missing_tokens = self.load_missing_tokens()

    # ==================================================
    # CARREGA TOKENS FALTANTES
    # ==================================================

    def load_missing_tokens(
        self
    ):

        if not os.path.exists(
            self.missing_file
        ):
            return {}

        try:

            with open(
                self.missing_file,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(
                    file
                )

        except Exception:

            return {}

    # ==================================================
    # SALVA TOKENS FALTANTES
    # ==================================================

    def save_missing_tokens(
        self
    ):

        sorted_missing = dict(
            sorted(
                self.missing_tokens.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

        with open(
            self.missing_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                sorted_missing,
                file,
                ensure_ascii=False,
                indent=2
            )

    # ==================================================
    # SALVA RELATÓRIO DE COBERTURA
    # ==================================================

    def save_coverage_report(
        self
    ):

        valid_total = self.session_stats[
            "tokens_validos"
        ]

        mapped = self.session_stats[
            "tokens_mapeados"
        ]

        if valid_total > 0:

            coverage = (
                mapped / valid_total
            ) * 100

        else:

            coverage = 0

        report = {
            **self.session_stats,
            "cobertura_percentual_real": round(
                coverage,
                2
            ),
            "tokens_faltantes_unicos": len(
                self.missing_tokens
            ),
            "missing_signals_file": self.missing_file
        }

        with open(
            self.coverage_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                ensure_ascii=False,
                indent=2
            )

    # ==================================================
    # REGISTRA TOKEN SEM SINAL
    # ==================================================

    def register_missing_token(
        self,
        token
    ):

        if not token:
            return

        self.missing_tokens[token] = (
            self.missing_tokens.get(
                token,
                0
            )
            + 1
        )

        self.save_missing_tokens()

    # ==================================================
    # TOKENIZA COM SUPORTE A SINAIS COMPOSTOS
    # ==================================================

    def tokenize_with_compounds(
        self,
        glosa
    ):

        words = glosa.split()

        result = []

        i = 0

        while i < len(words):

            # tenta composto de 3 tokens
            if i + 2 < len(words):

                three = (
                    words[i]
                    + " "
                    + words[i + 1]
                    + " "
                    + words[i + 2]
                )

                if three in COMPOUND_SIGNAL_MAP:

                    result.append(
                        three
                    )

                    i += 3

                    continue

            # tenta composto de 2 tokens
            if i + 1 < len(words):

                two = (
                    words[i]
                    + " "
                    + words[i + 1]
                )

                if two in COMPOUND_SIGNAL_MAP:

                    result.append(
                        two
                    )

                    i += 2

                    continue

            result.append(
                words[i]
            )

            i += 1

        return result

    # ==================================================
    # CONVERTE GLOSA EM SINAIS
    # ==================================================

    def glosa_to_signals(
        self,
        glosa
    ):

        clean_glosa, ignored_tokens = self.cleaner.clean_glosa(
            glosa
        )

        tokens = self.tokenize_with_compounds(
            clean_glosa
        )

        signals = []

        for token in tokens:

            token = token.strip()

            if not token:
                continue

            if token in COMPOUND_SIGNAL_MAP:

                signal = COMPOUND_SIGNAL_MAP.get(
                    token
                )

            else:

                signal = SIGNAL_MAP.get(
                    token
                )

            if signal:

                signals.append({
                    "token": token,
                    "signal": signal,
                    "found": True
                })

            else:

                signals.append({
                    "token": token,
                    "signal": None,
                    "found": False
                })

        return signals, ignored_tokens

    # ==================================================
    # EXECUTA UM SINAL
    # ==================================================

    def execute_signal(
        self,
        item
    ):

        token = item.get(
            "token"
        )

        signal = item.get(
            "signal"
        )

        found = item.get(
            "found",
            False
        )

        if found:

            print(
                f"[AVATAR] Executando sinal: {token} -> {signal}"
            )

        else:

            print(
                f"[AVATAR][SEM SINAL] Token sem mapeamento: {token}"
            )

            self.register_missing_token(
                token
            )

        time.sleep(
            0.2
        )

    # ==================================================
    # EXIBE ESTATÍSTICAS DA GLOSA
    # ==================================================

    def show_stats(
        self,
        signals,
        ignored_tokens
    ):

        valid_total = len(
            signals
        )

        found = sum(
            1
            for item in signals
            if item.get("found")
        )

        missing = valid_total - found

        ignored = len(
            ignored_tokens
        )

        coverage = (
            found / valid_total * 100
            if valid_total > 0
            else 0
        )

        print()
        print("-" * 80)
        print(
            f"[AVATAR] Tokens válidos: {valid_total}"
        )
        print(
            f"[AVATAR] Sinais encontrados: {found}"
        )
        print(
            f"[AVATAR] Sinais sem mapeamento: {missing}"
        )
        print(
            f"[AVATAR] Tokens ignorados como ruído: {ignored}"
        )

        if ignored_tokens:

            print(
                f"[AVATAR] Ruídos ignorados: {ignored_tokens}"
            )

        print(
            f"[AVATAR] Cobertura real: {coverage:.1f}% ({found}/{valid_total})"
        )
        print("-" * 80)

    # ==================================================
    # ATUALIZA ESTATÍSTICAS DA SESSÃO
    # ==================================================

    def update_session_stats(
        self,
        signals,
        ignored_tokens,
        original_token_count
    ):

        valid_total = len(
            signals
        )

        found = sum(
            1
            for item in signals
            if item.get("found")
        )

        missing = valid_total - found

        ignored = len(
            ignored_tokens
        )

        self.session_stats[
            "glosas_processadas"
        ] += 1

        self.session_stats[
            "tokens_totais"
        ] += original_token_count

        self.session_stats[
            "tokens_validos"
        ] += valid_total

        self.session_stats[
            "tokens_mapeados"
        ] += found

        self.session_stats[
            "tokens_sem_mapeamento"
        ] += missing

        self.session_stats[
            "tokens_ignorados_ruido"
        ] += ignored

        self.save_coverage_report()

    # ==================================================
    # EXIBE ESTATÍSTICAS DA SESSÃO
    # ==================================================

    def show_session_stats(
        self
    ):

        valid_total = self.session_stats[
            "tokens_validos"
        ]

        mapped = self.session_stats[
            "tokens_mapeados"
        ]

        missing = self.session_stats[
            "tokens_sem_mapeamento"
        ]

        ignored = self.session_stats[
            "tokens_ignorados_ruido"
        ]

        coverage = (
            mapped / valid_total * 100
            if valid_total > 0
            else 0
        )

        print()
        print("=" * 80)
        print("[AVATAR] ESTATÍSTICAS DA SESSÃO")
        print("=" * 80)
        print(
            f"Glosas processadas: {self.session_stats['glosas_processadas']}"
        )
        print(
            f"Tokens totais recebidos: {self.session_stats['tokens_totais']}"
        )
        print(
            f"Tokens válidos: {valid_total}"
        )
        print(
            f"Tokens mapeados: {mapped}"
        )
        print(
            f"Tokens sem mapeamento: {missing}"
        )
        print(
            f"Tokens ignorados como ruído: {ignored}"
        )
        print(
            f"Cobertura real: {coverage:.1f}%"
        )
        print(
            f"Tokens faltantes únicos: {len(self.missing_tokens)}"
        )
        print("=" * 80)

    # ==================================================
    # PROCESSA GLOSA COMPLETA
    # ==================================================

    def process_glosa(
        self,
        payload
    ):

        item_id = payload.get(
            "id"
        )

        timestamp = payload.get(
            "timestamp"
        )

        texto_original = payload.get(
            "texto_original",
            ""
        )

        glosa = payload.get(
            "glosa",
            ""
        ).strip()

        if not glosa:

            print(
                "[AVATAR] Glosa vazia ignorada."
            )

            return

        print()
        print("=" * 80)
        print(
            f"[AVATAR] Processando glosa ID={item_id}"
        )

        if timestamp:

            print(
                f"[AVATAR] Timestamp: {timestamp}"
            )

        if texto_original:

            print(
                f"[AVATAR] Texto original: {texto_original}"
            )

        print(
            f"[AVATAR] GLOSA ORIGINAL: {glosa}"
        )
        print("=" * 80)

        original_token_count = len(
            glosa.split()
        )

        signals, ignored_tokens = self.glosa_to_signals(
            glosa
        )

        if not signals and ignored_tokens:

            print(
                "[AVATAR] Glosa continha apenas ruídos. Ignorada para cobertura."
            )

            self.update_session_stats(
                signals=[],
                ignored_tokens=ignored_tokens,
                original_token_count=original_token_count
            )

            self.show_stats(
                signals=[],
                ignored_tokens=ignored_tokens
            )

            self.show_session_stats()

            return

        if not signals:

            print(
                "[AVATAR] Nenhum token válido encontrado na glosa."
            )

            return

        for item in signals:

            self.execute_signal(
                item
            )

        self.show_stats(
            signals,
            ignored_tokens
        )

        self.update_session_stats(
            signals,
            ignored_tokens,
            original_token_count
        )

        self.show_session_stats()

        print(
            f"[AVATAR] Glosa ID={item_id} finalizada"
        )

    # ==================================================
    # LOOP
    # ==================================================

    def worker(
        self
    ):

        print(
            "[AVATAR] Worker iniciado"
        )

        while self.running:

            try:

                payload = self.avatar_queue.get(
                    timeout=1
                )

                self.process_glosa(
                    payload
                )

            except queue.Empty:

                continue

            except Exception as e:

                print(
                    "[AVATAR][ERRO]",
                    e
                )

        self.save_missing_tokens()
        self.save_coverage_report()
        self.show_session_stats()

        print(
            "[AVATAR] Worker encerrado"
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
            "[AVATAR] Adapter iniciado"
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
            "[AVATAR] Encerrando adapter..."
        )