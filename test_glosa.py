from libras.glosa_generator import GlosaGenerator


generator = GlosaGenerator()

TEST_PHRASES = [

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

print()
print("=" * 100)
print("TESTE DE GLOSA - CORPUS TEOLÓGICO")
print("=" * 100)
print()

for index, frase in enumerate(TEST_PHRASES, start=1):

    glosa = generator.translate(frase)

    print("=" * 100)
    print(f"CASO #{index}")
    print("=" * 100)

    print()
    print("PORTUGUÊS")
    print("-" * 100)
    print(frase)

    print()
    print("GLOSA")
    print("-" * 100)
    print(glosa)

    print()