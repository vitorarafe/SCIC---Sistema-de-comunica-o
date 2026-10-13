import heapq

CRITICIDADE = {"ativo": 1, "manutencao": 3, "alerta": 5}

# Heap só sabe comparar um número com outros números, ele precisa de uma única "nota" por alerta.
# Agora o erro vem do MODELO, já em porcentagem (ex.: 5.9 significa 5,9%).
def calcular_pontos(criticidade, erro_percentual):
    # Criticidade pesa 10 por nível; cada 1% de erro do modelo soma 2 pontos.
    return criticidade * 10 + erro_percentual * 2


def analisar_alertas(df, limite=5):
    alertas = []

    # iterrows entrega uma linha da tabela por vez.
    for _, linha in df.iterrows():
        criticidade = CRITICIDADE[linha["status"]]
        pontos = calcular_pontos(criticidade, linha["erro_relativo_percentual"])
        mensagem = (f"status {linha['status']} | carga {linha['carga_requisicoes']} req/min | "
                    f"latência {linha['latencia_observada']} ms "
                    f"(prevista {linha['latencia_prevista']:.1f} ms)")
        # Guarda com a nota negativa: a maior nota vira o menor valor e sai primeiro.
        heapq.heappush(alertas, (-pontos, linha["modulo"], mensagem))

    print(f"\n=== TOP {limite} ALERTAS POR PRIORIDADE ===")
    # Tira só os 'limite' primeiros do heap (ou menos, se houver menos alertas).
    for _ in range(min(limite, len(alertas))):
        neg, modulo, mensagem = heapq.heappop(alertas)
        print(f"[{-neg:.1f} pts] {modulo}: {mensagem}")

def inserir(trie, palavra, registro):

    no = trie
    # Percorre cada letra da palavra em minúsculo, só para montar o caminho.
    for letra in palavra.lower():
        if letra not in no:
            no[letra] = {}
        no = no[letra]
    if "*" not in no:
        no["*"] = []
    no["*"].append(registro)

# Função para buscar um prefixo no trie.
def achar_prefixo(trie, prefixo):
    no = trie
    for letra in prefixo.lower():
        if letra not in no:
            return None
        no = no[letra]
    return no

# Função para coletar todas as palavras que começam com um determinado prefixo. Retorna uma lista de palavras.
# NO = nó do trie onde o prefixo termina, RESULTADO = lista de palavras completas.
def coletar_palavras(no, resultado):
    for chave in no:
        if chave == "*":
            resultado.extend(no["*"])
        else:
            coletar_palavras(no[chave], resultado)

# Função para buscar todas as palavras que começam com um determinado prefixo. Retorna uma lista de palavras.
def buscar_por_prefixo(trie, prefixo):
    no = achar_prefixo(trie, prefixo)
    if no is None:
        return []
    resultado = []
    coletar_palavras(no, resultado)
    return resultado

CODIGOS = {
    "Comunicacao":    "SNS-0A1",
    "Energia":        "SNS-0B2",
    "Comando":        "SNS-0C3",
    "Laboratorio":    "SNS-1D4",
    "Agricultura":    "SNS-2A1",
    "Habitacao":      "SNS-2B2",
    "Suporte Medico": "SNS-3C1",
    "Armazenamento":  "SNS-3D2",
}

def construir_tries(df):
    trie_nomes = {}
    trie_codigos = {}
    ultimos = df.drop_duplicates(subset="modulo", keep="last")
    for _, linha in ultimos.iterrows():
        registro = {
            "nome": linha["modulo"],
            "status": linha["status"],
            "codigo": CODIGOS.get(linha["modulo"], "SEM-CODIGO"),
        }
        inserir(trie_nomes, registro["nome"], registro)
        inserir(trie_codigos, registro["codigo"], registro)
    return trie_nomes, trie_codigos

# busca de módulo por prefixo do nome.
def buscar_modulo(trie_nomes):
    prefixo = input("Digite o prefixo do nome do módulo: ")
    achados = buscar_por_prefixo(trie_nomes, prefixo)
    if len(achados) == 0:
        print("Nenhum módulo encontrado.")
    else:
        for r in achados:
            print(f"{r['nome']} | status: {r['status']} | código: {r['codigo']}")

# busca de sensor por prefixo do código.
def buscar_sensor(trie_codigos):
    prefixo = input("Digite o prefixo do código do sensor: ")
    achados = buscar_por_prefixo(trie_codigos, prefixo)
    if len(achados) == 0:
        print("Nenhum sensor encontrado.")
    else:
        for r in achados:
            print(f"{r['codigo']} -> {r['nome']} ({r['status']})")

def menu(df):
    trie_nomes, trie_codigos = construir_tries(df)
    while True:
        print("\n=== SCIC - AURORA SIGER ===")
        print("1 - Analisar alertas (heap)")
        print("2 - Buscar módulo por nome (trie)")
        print("3 - Buscar sensor por código (trie)")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            analisar_alertas(df)
        elif opcao == "2":
            buscar_modulo(trie_nomes)
        elif opcao == "3":
            buscar_sensor(trie_codigos)
        elif opcao == "0":
            print("Encerrando o SCIC. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")