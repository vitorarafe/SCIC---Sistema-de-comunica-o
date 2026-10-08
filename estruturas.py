import heapq

# Lista de tuplas representando os alertas, cada tupla contém:
# (módulo, mensagem, criticidade, valor previsto, valor observado)
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

# Função que monta o heap com os alertas e mostra do mais urgente ao menos urgente.
def analisar_alertas():
    # Lista de alertas, cada alerta é uma tupla com a nota negativa, o módulo e a mensagem.
    # Fica DENTRO da função porque o heappop remove os itens: assim ela é refeita a cada chamada.
    alertas = []

    # O for pega uma tupla de dados por vez, desempacota os valores e separa nas 5 variáveis.
    for modulo, mensagem, criticidade, previsto, observado in dados:
        # Chama a função anterior para calcular os pontos do alerta
        pontos = calcular_pontos(criticidade, previsto, observado)
        # Guarda no heap com a nota negativa, a maior nota vira o menor valor e sai primeiro.
        heapq.heappush(alertas, (-pontos, modulo, mensagem))

    print("\n=== ALERTAS POR PRIORIDADE ===")
    # O while vai desempilhar os alertas, imprimindo a nota positiva, o módulo e a mensagem.
    while alertas:
        neg, modulo, mensagem = heapq.heappop(alertas)
        # :.1f formata o número com uma casa decimal, o sinal de menos inverte a nota.
        print(f"[{-neg:.1f} pts] {modulo}: {mensagem}")

# CRIANDO O TRIE

# PALAVRA monta o caminho na árvore, REGISTRO é o dicionário com os dados do módulo.
def inserir(trie, palavra, registro):
    # Define o lugar onde está. O "no" começa na raiz da trie.
    no = trie
    # Percorre cada letra da palavra em minúsculo, só para montar o caminho.
    for letra in palavra.lower():
        # Se a letra não existe neste nível, cria um galho novo.
        if letra not in no:
            no[letra] = {}
        # Desce um nível, para dentro daquela letra.
        no = no[letra]
    # Se ainda não existe uma lista de registros neste ponto, cria uma vazia.
    if "*" not in no:
        no["*"] = []
    # Guarda o registro na lista.
    no["*"].append(registro)

# Função para buscar um prefixo no trie. Retorna o nó correspondente ao último caractere do prefixo, ou None se o prefixo não existir.
def achar_prefixo(trie, prefixo):
    # Começa no INÍCIO da árvore.
    no = trie
    # Pega uma letra do prefixo por vez, descendo na árvore. Se a letra não existir, retorna None.
    for letra in prefixo.lower():
        # Pergunta se a letra existe nesse nível.
        if letra not in no:
            # Se não existir, retorna None, indicando que o prefixo não foi encontrado.
            return None
        # Se existir, desce um nível na árvore, indo para o dicionário da letra atual.
        no = no[letra]
    # Se o for terminou, todas as letras do prefixo existem.
    return no

# Função para coletar todas as palavras que começam com um determinado prefixo. Retorna uma lista de palavras.
# NO = nó do trie onde o prefixo termina, RESULTADO = lista de palavras completas.
def coletar_palavras(no, resultado):
    # Percorre as chaves do nível. Cada chave é uma letra ou o '*'.
    for chave in no:
        # Se a chave for '*', chegamos ao final de uma palavra.
        if chave == "*":
            # Guarda a palavra original que estava na marca.
            resultado.extend(no["*"])
        # Se for uma letra, ainda tem um caminho a percorrer.
        else:
            # Chama a função recursivamente, descendo um nível na árvore.
            coletar_palavras(no[chave], resultado)

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
    coletar_palavras(no, resultado)
    # Devolve as palavras encontradas, que começam com o prefixo.
    return resultado

modulos = [
    {"nome": "Comunicação Principal", "status": "alerta", "codigo": "SNS-0A1"},
    {"nome": "Comando Central",       "status": "ativo",  "codigo": "SNS-0C3"},
    {"nome": "Controle de Energia",   "status": "ativo",  "codigo": "SNS-0B2"},
    {"nome": "Laboratório Alfa",      "status": "alerta", "codigo": "SNS-1D4"},
]

# Monta as duas tries UMA vez só: uma pelo nome do módulo, outra pelo código do sensor.
trie_nomes = {}
trie_codigos = {}

for m in modulos:
    # O mesmo módulo (registro inteiro) entra nas duas tries.
    inserir(trie_nomes, m["nome"], m)
    inserir(trie_codigos, m["codigo"], m)

# Opção 2 do menu: busca de módulo por prefixo do nome.
def buscar_modulo():
    # input() mostra a mensagem, espera o usuário digitar e devolve o texto.
    prefixo = input("Digite o prefixo do nome do módulo: ")
    achados = buscar_por_prefixo(trie_nomes, prefixo)

    # Se a lista veio vazia, avisa o usuário em vez de deixar a tela em branco.
    if len(achados) == 0:
        print("Nenhum módulo encontrado.")
    else:
        for r in achados:
            print(f"{r['nome']} | status: {r['status']} | código: {r['codigo']}")

# Opção 3 do menu: busca de sensor por prefixo do código.
def buscar_sensor():
    prefixo = input("Digite o prefixo do código do sensor: ")
    achados = buscar_por_prefixo(trie_codigos, prefixo)

    if len(achados) == 0:
        print("Nenhum sensor encontrado.")
    else:
        for r in achados:
            print(f"{r['codigo']} -> {r['nome']} ({r['status']})")

# Menu principal do sistema.
def menu():
    # while True repete até encontrar um break, por isso o menu volta após cada ação.
    while True:
        print("\n=== SCIC - AURORA SIGER ===")
        print("1 - Analisar alertas (heap)")
        print("2 - Buscar módulo por nome (trie)")
        print("3 - Buscar sensor por código (trie)")
        print("0 - Sair")

        # input() sempre devolve TEXTO, por isso comparamos com "1" entre aspas.
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            analisar_alertas()
        elif opcao == "2":
            buscar_modulo()
        elif opcao == "3":
            buscar_sensor()
        elif opcao == "0":
            print("Encerrando o SCIC. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Inicia o programa. Precisa ficar por último, depois de todas as funções definidas.
menu()