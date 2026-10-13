import heapq
from dispositivos import CODIGOS
import unicodedata

# Tira os acentos: "Comunicação" vira "Comunicacao".
def remover_acentos(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn")

CRITICIDADE = {"ativo": 1, "manutencao": 3, "alerta": 5}

def calcular_pontos(criticidade, erro_percentual):
    # Criticidade pesa 10 por nível; cada 1% de erro do modelo soma 2 pontos.
    return criticidade * 10 + erro_percentual * 2


# Monta o heap a partir da tabela (DataFrame). Cada linha vira um alerta com sua nota.
def montar_heap(df):
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
    return alertas

def analisar_alertas(df, limite=5):
    alertas = montar_heap(df)

    print(f"\n=== TOP {limite} ALERTAS POR PRIORIDADE ===")
    for _ in range(min(limite, len(alertas))):
        neg, modulo, mensagem = heapq.heappop(alertas)
        print(f"[{-neg:.1f} pts] {modulo}: {mensagem}")

# Devolve só o alerta mais urgente (nota, módulo, mensagem), ou None se não há dados.
def alerta_mais_urgente(df):
    alertas = montar_heap(df)
    if not alertas:
        return None
    neg, modulo, mensagem = heapq.heappop(alertas)
    return -neg, modulo, mensagem

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
    prefixo = remover_acentos(input("Digite o prefixo do nome do módulo: "))
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
