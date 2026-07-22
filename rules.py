"""
Regras heurísticas para organização de glosa Libras.

Este módulo não tenta resolver toda a gramática da Libras.
Ele aplica transformações simples e controladas para melhorar a saída:

1. Colocar marcadores temporais no início.
2. Evitar duplicações próximas.
3. Reposicionar negação de forma previsível.
4. Simplificar verbos comuns do português para forma base.
5. Remover tokens vazios e ruídos de pontuação.
"""

from libras.lexicon import (
    TEMPORAL_MARKERS,
    NEGATION_MARKERS
)


class GlosaRules:

    def clean_tokens(self, words):

        result = []

        for word in words:

            if not word:
                continue

            word = str(word).strip()

            if not word:
                continue

            result.append(word)

        return result

    # ==========================================
    # HOJE -> início da frase
    # ==========================================

    def move_temporal_to_start(
        self,
        words
    ):

        temporal = []
        others = []

        for word in words:

            if word in TEMPORAL_MARKERS:

                temporal.append(word)

            else:

                others.append(word)

        return temporal + others

    # ==========================================
    # NÃO NÃO NÃO -> NÃO
    # ==========================================

    def normalize_negation(
        self,
        words
    ):

        result = []

        previous_negation = False

        for word in words:

            is_negation = (
                word in NEGATION_MARKERS
            )

            if (
                is_negation
                and previous_negation
            ):
                continue

            result.append(word)

            previous_negation = (
                is_negation
            )

        return result

    # ==========================================
    # remove verbos auxiliares
    # ==========================================

    def remove_auxiliary_noise(
        self,
        words
    ):

        auxiliaries = {

            "SER",
            "ESTAR",

            "FOI",
            "FORAM",

            "SEJA",
            "SEJAM"
        }

        result = []

        for word in words:

            if word in auxiliaries:
                continue

            result.append(word)

        return result

    # ==========================================
    # VAMOS ESTUDAR
    # ↓
    # ESTUDAR
    # ==========================================

    def simplify_motion_verbs(
        self,
        words
    ):

        result = []

        skip_next = False

        targets = {

            "ESTUDAR",
            "ORAR",
            "LOUVAR",
            "ADORAR",
            "LER",
            "PREGAR",
            "FALAR"
        }

        for i, word in enumerate(words):

            if skip_next:

                skip_next = False
                continue

            if (
                word == "IR"
                and (i + 1) < len(words)
            ):

                next_word = words[
                    i + 1
                ]

                if next_word in targets:

                    result.append(
                        next_word
                    )

                    skip_next = True

                    continue

            result.append(word)

        return result

    # ==========================================
    # ESPÍRITO + SANTO
    # ↓
    # ESPÍRITO-SANTO
    # ==========================================

    def theological_patterns(
        self,
        words
    ):

        result = []

        i = 0

        while i < len(words):

            if (
                i + 1 < len(words)
                and words[i] == "ESPÍRITO"
                and words[i + 1] == "SANTO"
            ):

                result.append(
                    "ESPÍRITO-SANTO"
                )

                i += 2
                continue

            result.append(
                words[i]
            )

            i += 1

        return result

    # ==========================================
    # remove duplicações
    # ==========================================

    def remove_near_duplicates(
        self,
        words
    ):

        result = []

        previous = None

        for word in words:

            if word == previous:
                continue

            result.append(word)

            previous = word

        return result

    # ==========================================
    # pipeline principal
    # ==========================================

    def apply(
        self,
        words
    ):

        words = self.clean_tokens(
            words
        )

        words = self.normalize_negation(
            words
        )

        words = self.remove_auxiliary_noise(
            words
        )

        words = self.move_temporal_to_start(
            words
        )

        words = self.simplify_motion_verbs(
            words
        )

        words = self.theological_patterns(
            words
        )

        words = self.remove_near_duplicates(
            words
        )

        return words