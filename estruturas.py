import heapq
# Lista de alertas, cada alerta é uma tupla com a nota negativa, o módulo e a mensagem.
alertas = []

# Lista de tuplas representando os alertas, cada tupla contém:
# (criticidade, descricao, tempo ocorrido, valor previsto, valor observado
dados = [
    ("Agricultura",    "Bateria do sensor em 30%",      1, 200, 210),
    ("Suporte Médico", "Enlace de comunicação caiu",    5, 250, 500),
    ("Habitação",      "Temperatura interna oscilando", 3, 175, 200),
    ("Laboratório",    "Latência levemente alta",       2, 400, 440),
    ("Comunicação",    "Latência acima do previsto",    4, 300, 480),
    ("Comunicação",    "Antena fora de alinhamento",    5, 300, 360),
]

# Função para calcular os pontos de cada alerta com base na criticidade e no erro relativo
# Heap só sabe comparar um número com outros números, ele precisa de uma única "nota" por alerta, para decidir qual é o mais crítico.
def calcular_pontos(criticidade, previsto, observado):
    # abs tira o sinal da diferença, garantindo que o erro relativo seja sempre positivo
    erro_relativo= abs(previsto - observado) / previsto
    # Atribui pesos diferentes à criticidade e ao erro relativo para calcular os pontos
    pontos = criticidade * 10 + erro_relativo *20
    # Retorna os pontos calculados
    return pontos 

# O for pega uma tupla de dados por vez, desempacota os valores e separa nas 5 variáveis.
for modulo, mensagem, criticidade, previsto, observado in dados:
    # Chama a função anterior para calcular os pontos do alerta
    pontos = calcular_pontos(criticidade, previsto, observado)
    # Guarda no heap com a nota negativa, a maior nota vira o menor valor e sai primeiro.
    heapq.heappush(alertas, (-pontos, modulo, mensagem))

# O while vai desempilhar os alertas, imprimindo a nota positiva, o módulo e a mensagem.
while alertas:
    neg, modulo, mensagem = heapq.heappop(alertas)
    # :.1f formata o número com uma casa decimal, o sinal de menos inverte a nota negativa para positiva.
    print(f"[{-neg:.1f} pts] {modulo}: {mensagem}")

# CRIANDO O TRIE

# Criando um dicionário vazio para armazenar os nós do trie.
trie = {}

# Função para inserir uma palavra no trie.
def inserir(trie, palavra):
    # Define o lugar onde está. O "no" começa no dicionário raiz do trie.
    no = trie
    # Pega cada letra da palavra, se a letra não estiver no dicionário do nó atual, cria um novo dicionário para ela.
    for letra in palavra:
        # pergunta "a letra atual já existe nesse nível?"
        if letra not in no:
            # Se não existir, cria um novo dicionário para a letra atual.
            no[letra] = {}
        # Desce um nível, para dentro daquela letra. Na volta seguinte do for, vamos procurar a próxima letra dentro do dicionário da letra atual.
        no = no[letra]
    # Marca o final da palavra com um asterisco, indicando que a palavra termina aqui.
    no["*"] = True

# Função para buscar um prefixo no trie. Retorna o nó correspondente ao último caractere do prefixo, ou None se o prefixo não existir.
def achar_prefixo(trie, prefixo):
    # Começa no INÍCIO da árvore.
    no = trie
    # Pega uma letra do prefixo por vez, descendo na árvore. Se a letra não existir, retorna None.
    for letra in prefixo:
        # Pergunta se a letra existe nesse nível.
        if letra not in no:
            # Se não existir, retorna None, indicando que o prefixo não foi encontrado.
            return None
        # Se existir, desce um nível na árvore, indo para o dicionário da letra atual.
        no = no[letra]
    # Se o for terminou, todas as letras do prefixo existem.
    return no

# Função para coletar todas as palavras que começam com um determinado prefixo. Retorna uma lista de palavras.
# NO = nó do trie onde o prefixo termina, TEXTO = letras que juntaram até o momento, RESULTADO = lista de palavras completas.
def coletar_palavras(no, texto, resultado):
    # Percorre as chavé do nível. Cada chave é uma letra ou o '*' que indica o final de uma palavra.
    for chave in no:
        # Se a chave for '*', significa que chegamos ao final de uma palavra, então adicionamos o texto acumulado à lista de resultados.
        if chave == "*":
            # Guarda o texto acumulado como palavra completa.
            resultado.append(texto)
        # Se for uma letra, ainda tem um caminho a percorrer.
        else:
            # Chama a função recursivamente, descendo um nível na árvore, adicionando a letra atual ao texto acumulado.
            coletar_palavras(no[chave], texto + chave, resultado)

# Função para buscar todas as palavras que começam com um determinado prefixo. Retorna uma lista de palavras.
def buscar_por_prefixo(trie, prefixo):
    # Puxa a função, para descer até o prefixo.
    no = achar_prefixo(trie, prefixo)
    # Se o prefixo não existir, retorna None.
    if no is None:
        # Então foi respondido com uma lista vazia.
        return []
    # Cria a lista vazia que a função recursiva vai preencher com as palavras encontradas.
    resultado = []
    # Começa a coleta, com o prefixo como texto inicial.
    coletar_palavras(no, prefixo, resultado)
    # Devolve as palavras encontradas, que começam com o prefixo.
    return resultado