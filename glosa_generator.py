import re

from libras.lexicon import (
    STOPWORDS,
    LEXICON,
    PHRASE_LEXICON
)

from libras.rules import (
    GlosaRules
)


class GlosaGenerator:

    def __init__(self):

        self.stopwords = STOPWORDS

        self.lexicon = LEXICON

        self.phrase_lexicon = (
            PHRASE_LEXICON
        )

        self.rules = GlosaRules()

    # =====================================================
    # NORMALIZA TEXTO
    # =====================================================

    def normalize_text(
        self,
        text
    ):

        text = text.lower().strip()

        text = re.sub(
            r"[^\w\sáéíóúâêôãõçàü\-]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # =====================================================
    # EXPRESSÕES COMPOSTAS
    # =====================================================

    def apply_phrase_lexicon(
        self,
        text
    ):

        normalized = self.normalize_text(
            text
        )

        for (
            phrase,
            replacement
        ) in self.phrase_lexicon.items():

            candidate = (
                self.normalize_text(
                    phrase
                )
            )

            if candidate in normalized:

                normalized = (
                    normalized.replace(
                        candidate,
                        replacement.lower()
                    )
                )

        return normalized

    # =====================================================
    # TOKENIZAÇÃO
    # =====================================================

    def tokenize(
        self,
        text
    ):

        text = self.apply_phrase_lexicon(
            text
        )

        if not text:
            return []

        return text.split()

    # =====================================================
    # STOPWORDS
    # =====================================================

    def remove_stopwords(
        self,
        words
    ):

        result = []

        for word in words:

            if (
                word.lower()
                in self.stopwords
            ):
                continue

            result.append(
                word
            )

        return result

    # =====================================================
    # MAPEAMENTO DE PALAVRAS
    # =====================================================

    def map_word(
        self,
        word
    ):

        word = (
            word.strip()
            .lower()
        )

        if not word:

            return ""

        # Caso especial:
        # expressão composta já convertida

        if "-" in word:

            return word.upper()

        if word in self.lexicon:

            return self.lexicon[
                word
            ]

        # singular simples

        if (
            word.endswith("s")
            and len(word) > 3
        ):

            singular = word[:-1]

            if singular in self.lexicon:

                return self.lexicon[
                    singular
                ]

        return word.upper()

    def map_words(
        self,
        words
    ):

        result = []

        for word in words:

            mapped = self.map_word(
                word
            )

            if mapped:

                result.append(
                    mapped
                )

        return result

    # =====================================================
    # LIMPEZA FINAL
    # =====================================================

    def cleanup(
        self,
        words
    ):

        result = []

        previous = None

        for word in words:

            if not word:
                continue

            if word == previous:
                continue

            result.append(
                word
            )

            previous = word

        return result

    # =====================================================
    # TRADUÇÃO PRINCIPAL
    # =====================================================

    def translate(
        self,
        text
    ):

        if not text:

            return ""

        words = self.tokenize(
            text
        )

        words = self.remove_stopwords(
            words
        )

        words = self.map_words(
            words
        )

        words = self.rules.apply(
            words
        )

        words = self.cleanup(
            words
        )

        if not words:

            return ""

        return " ".join(
            words
        )

    # =====================================================
    # DEBUG
    # =====================================================

    def debug_translate(
        self,
        text
    ):

        print()
        print("=" * 80)
        print("ENTRADA")
        print(text)

        step1 = self.tokenize(
            text
        )

        print()
        print("TOKENIZE")
        print(step1)

        step2 = self.remove_stopwords(
            step1
        )

        print()
        print("SEM STOPWORDS")
        print(step2)

        step3 = self.map_words(
            step2
        )

        print()
        print("LEXICON")
        print(step3)

        step4 = self.rules.apply(
            step3
        )

        print()
        print("RULES")
        print(step4)

        output = " ".join(
            step4
        )

        print()
        print("GLOSA")
        print(output)

        return output