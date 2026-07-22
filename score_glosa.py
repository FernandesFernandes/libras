import sys
import os

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

print("ROOT_DIR =", ROOT_DIR)

import csv

from libras.glosa_generator import GlosaGenerator
from libras.lexicon import (
    STOPWORDS,
    LEXICON
)


generator = GlosaGenerator()


TEST_PHRASES = [
    # Cole aqui as 50 frases
    "O propósito supremo do homem é glorificar a Deus e desfrutá-lo para sempre.",

    "Deus é o único ser absolutamente perfeito em seu ser e em seus atributos.",

    "A Palavra de Deus é a única regra infalível de fé e prática.",

    "Toda verdadeira sabedoria começa no conhecimento de Deus.",

    "Nada acontece fora da providência do Senhor.",

    "Deus criou todas as coisas para manifestar a sua glória.",

    "A criação testemunha o poder, a sabedoria e a bondade de Deus.",

    "O homem foi criado à imagem de Deus em conhecimento, justiça e santidade.",

    "O pecado entrou no mundo pela queda de Adão.",

    "Em Adão todos pecaram e necessitam de redenção.",

    "O salário do pecado é a morte, mas a graça oferece vida em Cristo.",

    "Somente Cristo é o Mediador entre Deus e os homens.",

    "Jesus Cristo é verdadeiro Deus e verdadeiro homem em uma só pessoa.",

    "A obediência perfeita de Cristo é imputada aos que creem.",

    "A justificação é um ato da livre graça de Deus.",

    "Somos aceitos por Deus somente pela justiça de Cristo.",

    "A fé é o instrumento pelo qual recebemos Cristo e seus benefícios.",

    "As boas obras são fruto da salvação, nunca sua causa.",

    "A santificação é obra contínua do Espírito Santo.",

    "O Espírito Santo habita em todo verdadeiro crente.",

    "A adoção nos torna filhos e herdeiros de Deus.",

    "A comunhão com Cristo transforma toda a vida do cristão.",

    "Os sacramentos confirmam as promessas da aliança de Deus.",

    "O batismo aponta para a purificação realizada por Cristo.",

    "A Ceia do Senhor fortalece espiritualmente os que participam com fé.",

    "A oração é um privilégio concedido aos filhos de Deus.",

    "Toda oração deve ser feita em nome de Cristo.",

    "A vontade de Deus é perfeita, santa e imutável.",

    "Os Dez Mandamentos revelam o padrão moral de Deus.",

    "Amar a Deus acima de todas as coisas é o maior dever do homem.",

    "Amar o próximo é expressão da verdadeira fé.",

    "A idolatria começa quando qualquer coisa ocupa o lugar de Deus.",

    "O nome de Deus deve ser tratado com reverência.",

    "O Dia do Senhor foi separado para adoração e descanso santo.",

    "Honrar pai e mãe é honrar a autoridade estabelecida por Deus.",

    "Deus exige pureza tanto nas ações quanto nos pensamentos.",

    "A mentira contradiz o caráter do Deus da verdade.",

    "A cobiça revela a insatisfação do coração humano.",

    "A lei de Deus revela o pecado e conduz o pecador a Cristo.",

    "O evangelho anuncia aquilo que a lei não pode conceder.",

    "Cristo reina como Profeta, Sacerdote e Rei do seu povo.",

    "Deus preserva todos aqueles que verdadeiramente pertencem a Cristo.",

    "A perseverança dos santos depende da fidelidade de Deus.",

    "A esperança cristã repousa nas promessas eternas do Senhor.",

    "A morte do crente é a entrada para a presença de Cristo.",

    "A ressurreição gloriosa será a vitória final sobre a morte.",

    "O juízo final manifestará perfeitamente a justiça de Deus.",

    "Os salvos desfrutarão eternamente da presença gloriosa do Senhor.",

    "Toda a história caminha para a plena manifestação do Reino de Deus.",

    "Toda honra, toda glória e todo louvor pertencem somente a Deus para sempre."
]


# =====================================================
# SCORE
# =====================================================

def score_glosa(
    phrase,
    glosa
):

    score = 0

    original_words = [
        x.lower()
        for x in phrase.split()
    ]

    glosa_words = glosa.split()

    # -----------------------------------
    # 1. Tamanho mínimo
    # -----------------------------------

    if len(glosa_words) >= 2:
        score += 1

    # -----------------------------------
    # 2. Stopwords removidas
    # -----------------------------------

    stopword_found = False

    for word in glosa_words:

        if word.lower() in STOPWORDS:

            stopword_found = True

            break

    if not stopword_found:
        score += 1

    # -----------------------------------
    # 3. Cobertura do léxico
    # -----------------------------------

    recognized = 0
    total = 0

    for word in original_words:

        word = (
            word
            .replace(".", "")
            .replace(",", "")
            .replace(";", "")
            .replace(":", "")
            .lower()
        )

        if word in STOPWORDS:
            continue

        total += 1

        if word in LEXICON:
            recognized += 1

    coverage = 0

    if total > 0:
        coverage = recognized / total

    if coverage >= 0.80:
        score += 2

    elif coverage >= 0.50:
        score += 1

    # -----------------------------------
    # 4. Conceitos teológicos
    # -----------------------------------

    theology_words = {

        "DEUS",
        "CRISTO",
        "JESUS",

        "ESPÍRITO-SANTO",

        "SALVAÇÃO",

        "GRAÇA",

        "FÉ",

        "IGREJA",

        "EVANGELHO",

        "GLÓRIA",

        "REINO"
    }

    found = False

    for word in glosa_words:

        if word in theology_words:

            found = True
            break

    if found:
        score += 1

    return min(score, 5)


# =====================================================
# EXECUÇÃO
# =====================================================

results = []

for phrase in TEST_PHRASES:

    glosa = generator.translate(
        phrase
    )

    score = score_glosa(
        phrase,
        glosa
    )

    results.append({
        "frase": phrase,
        "glosa": glosa,
        "nota": score
    })


# =====================================================
# CSV
# =====================================================

with open(
    "glosa_report.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "frase",
            "glosa",
            "nota"
        ]
    )

    writer.writeheader()

    writer.writerows(
        results
    )


# =====================================================
# RELATÓRIO
# =====================================================

results_sorted = sorted(
    results,
    key=lambda x: x["nota"]
)

media = (
    sum(
        x["nota"]
        for x in results
    )
    / len(results)
)

print()
print("=" * 100)
print("RELATÓRIO DE QUALIDADE DAS GLOSAS")
print("=" * 100)

print()
print(
    f"TOTAL DE FRASES: {len(results)}"
)

print(
    f"MÉDIA GERAL: {media:.2f}/5"
)

print()

# -----------------------------------------------------
# Distribuição
# -----------------------------------------------------

for nota in range(0, 6):

    quantidade = sum(
        1
        for x in results
        if x["nota"] == nota
    )

    print(
        f"NOTA {nota}: {quantidade}"
    )

print()

# -----------------------------------------------------
# Piores 10
# -----------------------------------------------------

print("=" * 100)
print("10 PIORES RESULTADOS")
print("=" * 100)

for item in results_sorted[:10]:

    print()
    print(
        f"NOTA: {item['nota']}/5"
    )

    print(
        f"FRASE: {item['frase']}"
    )

    print(
        f"GLOSA: {item['glosa']}"
    )

# -----------------------------------------------------
# Melhores 10
# -----------------------------------------------------

print()
print("=" * 100)
print("10 MELHORES RESULTADOS")
print("=" * 100)

for item in reversed(
    results_sorted[-10:]
):

    print()

    print(
        f"NOTA: {item['nota']}/5"
    )

    print(
        f"FRASE: {item['frase']}"
    )

    print(
        f"GLOSA: {item['glosa']}"
    )

print()

print(
    "Arquivo gerado: glosa_report.csv"
)