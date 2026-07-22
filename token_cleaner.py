import re


class TokenCleaner:

    def __init__(self):

        # Tokens claramente ruidosos ou pouco úteis para o avatar
        self.noise_tokens = {

            "AH",
            "Ã",
            "A",
            "É",
            "EH",
            "HÃ",
            "HUM",
            "UÉ",
            "UE",

            "SÓ",
            "SO",

            # ruídos observados no seu teste
            "MOICA",
            "CANTE",
            "CÂNTE",

            # pontuações ou resíduos
            ".",
            ",",
            "...",
            "!",
            "?",
            "-",
        }

        # Tokens muito curtos que normalmente são ruído.
        # Atenção: NÃO remove "FÉ" porque é teológico.
        self.allowed_short_tokens = {
            "FÉ",
            "FE",
            "NÃO",
            "NAO",
            "EU",
            "IR",
        }

    def normalize_token(
        self,
        token
    ):

        if token is None:
            return ""

        token = str(token).strip().upper()

        token = re.sub(
            r"\s+",
            " ",
            token
        )

        return token

    def is_noise(
        self,
        token
    ):

        token = self.normalize_token(
            token
        )

        if not token:
            return True

        if token in self.noise_tokens:
            return True

        # Remove token de 1 caractere, salvo exceções
        if (
            len(token) <= 1
            and token not in self.allowed_short_tokens
        ):
            return True

        return False

    def clean_tokens(
        self,
        tokens
    ):

        cleaned = []

        ignored = []

        for token in tokens:

            normalized = self.normalize_token(
                token
            )

            if self.is_noise(
                normalized
            ):

                ignored.append(
                    normalized
                )

                continue

            cleaned.append(
                normalized
            )

        return cleaned, ignored

    def clean_glosa(
        self,
        glosa
    ):

        if not glosa:
            return "", []

        tokens = glosa.split()

        cleaned, ignored = self.clean_tokens(
            tokens
        )

        return " ".join(
            cleaned
        ), ignored