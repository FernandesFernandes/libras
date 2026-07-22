"""
Dicionários léxicos para geração de glosa Libras.

Este módulo centraliza vocabulário e equivalências usadas pelo
GlosaGenerator, evitando que o dicionário fique misturado com a lógica.

Observação:
- Esta é uma versão heurística inicial.
- A glosa gerada ainda não substitui uma tradução humana em Libras.
- O objetivo é criar uma base evolutiva para o domínio de culto/igreja.
"""


# Palavras normalmente removidas da glosa por não carregarem sinal central.


# ======================================================
# STOPWORDS
# ======================================================

STOPWORDS = {

    "o", "a", "os", "as",

    "um", "uma", "uns", "umas",

    "de", "da", "do", "das", "dos",

    "em", "no", "na", "nos", "nas",

    "para", "por", "com",

    "que",

    "e", "ou", "mas",

    "ao", "aos",

    "à", "às",

    "se",

    "como",

    "porque",

    "pois",

    "há",

    "já",

    "também",

    "todo",
    "toda",

    "todos",
    "todas",

    "é",
    "são",
    "foi",
    "será",
    "serao",
    "serão",

    "seu",
    "sua",
    "seus",
    "suas",

    "pelo",
    "pela",
    "pelos",
    "pelas",

    "entre",

    "somente",

    "qualquer",

    "quando",

    "quanto",

    "tanto",

    "aquilo",

    "aquele",
    "aqueles",

    "essa",
    "esse",
    "isso",

    "lhe",

    "lo",
    "la",
    "los",
    "las"
}

# ======================================================
# TEMPORAIS
# ======================================================

TEMPORAL_MARKERS = {

    "HOJE",

    "AMANHÃ",

    "ONTEM",

    "AGORA",

    "ANTES",

    "DEPOIS",

    "SEMPRE",

    "NUNCA",

    "ETERNAMENTE"
}

# ======================================================
# NEGAÇÃO
# ======================================================

NEGATION_MARKERS = {

    "NÃO",

    "NUNCA",

    "JAMAIS"
}

# ======================================================
# PRONOMES
# ======================================================

PRONOUNS = {

    "eu": "EU",

    "você": "VOCÊ",
    "voce": "VOCÊ",

    "nós": "NÓS",
    "nos": "NÓS",

    "eles": "ELES",

    "elas": "ELAS",

    "ele": "ELE",

    "ela": "ELA"
}

# ======================================================
# LÉXICO TEOLÓGICO
# ======================================================

THEOLOGY_LEXICON = {

    # --------------------------------------------------
    # TRINDADE
    # --------------------------------------------------

    "deus": "DEUS",

    "senhor": "SENHOR",

    "pai": "PAI",

    "filho": "FILHO",

    "jesus": "JESUS",

    "cristo": "CRISTO",

    "messias": "MESSIAS",

    "salvador": "SALVADOR",

    "mediador": "MEDIADOR",

    "espírito": "ESPÍRITO",
    "espirito": "ESPÍRITO",

    "santo": "SANTO",

    # --------------------------------------------------
    # BÍBLIA
    # --------------------------------------------------

    "bíblia": "BÍBLIA",
    "biblia": "BÍBLIA",

    "palavra": "PALAVRA",

    "evangelho": "EVANGELHO",

    "lei": "LEI",

    "mandamento": "MANDAMENTO",
    "mandamentos": "MANDAMENTO",

    "versículo": "VERSÍCULO",
    "versiculo": "VERSÍCULO",

    "salmo": "SALMO",
    "salmos": "SALMO",

    # --------------------------------------------------
    # SALVAÇÃO
    # --------------------------------------------------

    "salvação": "SALVAÇÃO",
    "salvacao": "SALVAÇÃO",

    "redenção": "REDENÇÃO",
    "redencao": "REDENÇÃO",

    "justificação": "JUSTIFICAÇÃO",
    "justificacao": "JUSTIFICAÇÃO",

    "santificação": "SANTIFICAÇÃO",
    "santificacao": "SANTIFICAÇÃO",

    "adoção": "ADOÇÃO",
    "adocao": "ADOÇÃO",

    "graça": "GRAÇA",
    "graca": "GRAÇA",

    "fé": "FÉ",
    "fe": "FÉ",

    # --------------------------------------------------
    # PECADO
    # --------------------------------------------------

    "pecado": "PECADO",
    "pecados": "PECADO",

    "queda": "QUEDA",

    "adão": "ADÃO",
    "adao": "ADÃO",

    "morte": "MORTE",

    "pecador": "PECADOR",

    # --------------------------------------------------
    # ATRIBUTOS DIVINOS
    # --------------------------------------------------

    "glória": "GLÓRIA",
    "gloria": "GLÓRIA",

    "santidade": "SANTIDADE",

    "justiça": "JUSTIÇA",
    "justica": "JUSTIÇA",

    "bondade": "BONDADE",

    "sabedoria": "SABEDORIA",

    "fidelidade": "FIDELIDADE",

    "amor": "AMOR",

    "verdade": "VERDADE",

    "providência": "PROVIDÊNCIA",
    "providencia": "PROVIDÊNCIA",

    "imutável": "IMUTÁVEL",
    "imutavel": "IMUTÁVEL",

    "perfeito": "PERFEITO",
    "perfeita": "PERFEITO",

    # --------------------------------------------------
    # IGREJA
    # --------------------------------------------------

    "igreja": "IGREJA",

    "culto": "CULTO",

    "oração": "ORAR",
    "oracao": "ORAR",

    "orar": "ORAR",

    "louvor": "LOUVOR",

    "adoração": "ADORAR",
    "adoracao": "ADORAR",

    "adorar": "ADORAR",

    "pregação": "PREGAR",
    "pregacao": "PREGAR",

    "pregar": "PREGAR",

    "sermão": "PREGAR",
    "sermao": "PREGAR",

    "batismo": "BATISMO",

    "ceia": "CEIA",

    "sacramento": "SACRAMENTO",
    "sacramentos": "SACRAMENTO",

    # --------------------------------------------------
    # ESCATOLOGIA
    # --------------------------------------------------

    "ressurreição": "RESSURREIÇÃO",
    "ressurreicao": "RESSURREIÇÃO",

    "juízo": "JUÍZO",
    "juizo": "JUÍZO",

    "céu": "CÉU",
    "ceu": "CÉU",

    "inferno": "INFERNO",

    "reino": "REINO",

    # --------------------------------------------------
    # VERBOS
    # --------------------------------------------------

    "amar": "AMAR",
    "ama": "AMAR",

    "glorificar": "GLORIFICAR",

    "honrar": "HONRAR",

    "obedecer": "OBEDECER",

    "servir": "SERVIR",

    "estudar": "ESTUDAR",

    "aprender": "APRENDER",

    "ler": "LER",

    "falar": "FALAR",

    "orar": "ORAR",

    "louvar": "LOUVAR",

    "adorar": "ADORAR",

    "pregar": "PREGAR",

    "habita": "HABITAR",

    "transforma": "TRANSFORMAR",

    "fortalece": "FORTALECER",

    "reina": "REINAR",

    "preserva": "PRESERVAR",

    "revela": "REVELAR",

    "conduz": "CONDUZIR",

    "manifesta": "MANIFESTAR",

    "ocupa": "OCUPAR",

    "pertencem": "PERTENCER",

    "caminha": "CAMINHAR",

    "depende": "DEPENDER",

    # --------------------------------------------------
    # CONCEITOS
    # --------------------------------------------------

    "homem": "HOMEM",
    "homens": "HOMEM",

    "imagem": "IMAGEM",

    "vida": "VIDA",

    "obra": "OBRA",
    "obras": "OBRA",

    "coração": "CORAÇÃO",
    "coracao": "CORAÇÃO",

    "esperança": "ESPERANÇA",
    "esperanca": "ESPERANÇA",

    "aliança": "ALIANÇA",
    "alianca": "ALIANÇA",

    "promessa": "PROMESSA",
    "promessas": "PROMESSA",

    "crente": "CRENTE",

    "cristão": "CRISTÃO",
    "cristao": "CRISTÃO",

    "santos": "SANTO",

    "próximo": "PRÓXIMO",
    "proximo": "PRÓXIMO",

    "idolatria": "IDOLATRIA",

    "autoridade": "AUTORIDADE",

    "mentira": "MENTIRA",

    "cobiça": "COBIÇA",
    "cobica": "COBIÇA",

    "pureza": "PUREZA",

    "reverência": "REVERÊNCIA",
    "reverencia": "REVERÊNCIA",

    "propósito": "PROPÓSITO",
    "proposito": "PROPÓSITO",

    "comunhão": "COMUNHÃO",
    "comunhao": "COMUNHÃO",

    "herdeiros": "HERDEIRO",

    "presença": "PRESENÇA",
    "presenca": "PRESENÇA",

    "história": "HISTÓRIA",
    "historia": "HISTÓRIA",

    "honra": "HONRA",

    "vitória": "VITÓRIA",
    "vitoria": "VITÓRIA",

    # --------------------------------------------------
    # COMPLEMENTOS IDENTIFICADOS PELO SCORE_GLOSA
    # --------------------------------------------------

    "atributo": "ATRIBUTO",
    "atributos": "ATRIBUTO",

    "regra": "REGRA",

    "infalível": "INFALÍVEL",
    "infalivel": "INFALÍVEL",

    "prática": "PRÁTICA",
    "pratica": "PRÁTICA",

    "único": "ÚNICO",
    "unico": "ÚNICO",

    "conhecimento": "CONHECIMENTO",

    "acontece": "ACONTECER",
    "acontecer": "ACONTECER",

    "fora": "FORA",

    "criou": "CRIAR",
    "criar": "CRIAR",
    "criado": "CRIAR",
    "criada": "CRIAR",

    "criação": "CRIAÇÃO",
    "criacao": "CRIAÇÃO",

    "testemunha": "TESTEMUNHAR",
    "testemunhar": "TESTEMUNHAR",

    "poder": "PODER",

    "entrou": "ENTRAR",
    "entrar": "ENTRAR",

    "pecaram": "PECAR",
    "pecar": "PECAR",

    "necessitam": "PRECISAR",
    "necessitar": "PRECISAR",

    "salário": "SALÁRIO",
    "salario": "SALÁRIO",

    "oferece": "OFERECER",
    "oferecer": "OFERECER",

    "verdadeiro": "VERDADEIRO",
    "verdadeira": "VERDADEIRO",

    "obediência": "OBEDIÊNCIA",
    "obediencia": "OBEDIÊNCIA",

    "imputada": "IMPUTAR",
    "imputado": "IMPUTAR",
    "imputar": "IMPUTAR",

    "creem": "CRER",
    "crer": "CRER",

    "aceitos": "ACEITAR",
    "aceito": "ACEITAR",
    "aceitar": "ACEITAR",

    "instrumento": "INSTRUMENTO",

    "recebemos": "RECEBER",
    "receber": "RECEBER",

    "benefícios": "BENEFÍCIO",
    "beneficios": "BENEFÍCIO",

    "fruto": "FRUTO",

    "causa": "CAUSA",

    "contínua": "CONTÍNUO",
    "continua": "CONTÍNUO",
    "contínuo": "CONTÍNUO",
    "continuo": "CONTÍNUO",

    "purificação": "PURIFICAR",
    "purificacao": "PURIFICAR",
    "purificar": "PURIFICAR",

    "participam": "PARTICIPAR",
    "participar": "PARTICIPAR",

    "privilégio": "PRIVILÉGIO",
    "privilegio": "PRIVILÉGIO",

    "concedido": "CONCEDER",
    "concedida": "CONCEDER",
    "conceder": "CONCEDER",

    "vontade": "VONTADE",

    "dez": "DEZ",

    "padrão": "PADRÃO",
    "padrao": "PADRÃO",

    "moral": "MORAL",

    "dever": "DEVER",

    "expressão": "EXPRESSAR",
    "expressao": "EXPRESSAR",

    "começa": "COMEÇAR",
    "comeca": "COMEÇAR",
    "começar": "COMEÇAR",

    "lugar": "LUGAR",

    "tratado": "TRATAR",
    "tratar": "TRATAR",

    "separado": "SEPARAR",
    "separar": "SEPARAR",

    "descanso": "DESCANSAR",

    "estabelecida": "ESTABELECER",
    "estabelecido": "ESTABELECER",
    "estabelecer": "ESTABELECER",

    "exige": "EXIGIR",
    "exigir": "EXIGIR",

    "ações": "AÇÃO",
    "acoes": "AÇÃO",
    "ação": "AÇÃO",
    "acao": "AÇÃO",

    "pensamentos": "PENSAMENTO",
    "pensamento": "PENSAMENTO",

    "caráter": "CARÁTER",
    "carater": "CARÁTER",

    "insatisfação": "INSATISFAÇÃO",
    "insatisfacao": "INSATISFAÇÃO",

    "humano": "HUMANO",

    "anuncia": "ANUNCIAR",
    "anunciar": "ANUNCIAR",

    "povo": "POVO",

    "verdadeiramente": "VERDADEIRO",

    "repousa": "REPOUSAR",
    "repousar": "REPOUSAR",

    "eternas": "ETERNO",
    "eterna": "ETERNO",
    "eterno": "ETERNO",

    "entrada": "ENTRADA",

    "gloriosa": "GLÓRIA",
    "glorioso": "GLÓRIA",

    "final": "FINAL",

    "salvos": "SALVO",
    "salvo": "SALVO",

    "desfrutarão": "DESFRUTAR",
    "desfrutarao": "DESFRUTAR",
    "desfrutar": "DESFRUTAR",

    "plena": "PLENO",
    "pleno": "PLENO",

    "manifestação": "MANIFESTAR",
    "manifestacao": "MANIFESTAR",

    # verbos de movimento (importante para rules.py)

    "vamos": "IR",
    "vou": "IR",
    "vai": "IR",
    "iremos": "IR"
}

# ======================================================
# EXPRESSÕES COMPOSTAS
# ======================================================

PHRASE_LEXICON = {

    "espírito santo":
        "ESPÍRITO-SANTO",

    "espirito santo":
        "ESPÍRITO-SANTO",

    "palavra de deus":
        "PALAVRA DEUS",

    "reino de deus":
        "REINO DEUS",

    "justiça de deus":
        "JUSTIÇA DEUS",

    "graça de deus":
        "GRAÇA DEUS",

    "dia do senhor":
        "DIA SENHOR",

    "ceia do senhor":
        "CEIA SENHOR",

    "filhos de deus":
        "FILHO DEUS",

    "imagem de deus":
        "IMAGEM DEUS",

    "boas obras":
        "OBRA BOM",

    "boa obra":
        "OBRA BOM",

    "salário do pecado":
        "SALÁRIO PECADO",

    "livre graça":
        "LIVRE GRAÇA",

    "vida eterna":
        "VIDA ETERNA",

    "espírito santo habita":
        "ESPÍRITO-SANTO HABITAR",

    "espirito santo habita":
        "ESPÍRITO-SANTO HABITAR",

    "reino de deus":
        "REINO DEUS"
}

# ======================================================
# CONSOLIDADO
# ======================================================

LEXICON = {

    **PRONOUNS,

    **THEOLOGY_LEXICON
}