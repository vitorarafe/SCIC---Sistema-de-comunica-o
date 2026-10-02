import heapq

# CRIAÇÃO DE UMA LISTA QUE VÃO FICAR ARMAZENADOS OS ALERTAS
alertas = []

# CRIAÇÃO DE UMA FUNÇÃO PARA REGISTRAR ALERTAS
def registrar_alerta(modulo, mensagem, criticidade):
    # heappush significa que o item será adicionado à lista de alertas, mantendo a propriedade de heap.
    # criticidade maior = mais urgente. O sinal negativo faz o mais crítico virar "o menor". Enganando o heapq a tratar o item como mais urgente.
    heapq.heappush(alertas, (-criticidade, modulo, mensagem))

# CADA ITEM É UMA TUPLA (TUPLA É UMA ESTRUTURA DE DADOS IMUTÁVEL, OU SEJA, NÃO PODE SER ALTERADA APÓS SUA CRIAÇÃO)
# Dados propositalmente FORA de ordem
dados = [
    ("Agricultura",           "Bateria do sensor em 30%",              1),
    ("Suporte Médico",        "Enlace de comunicação caiu",            5),
    ("Habitação",             "Temperatura interna oscilando",         3),
    ("Laboratório",           "Latência levemente alta",               2),
    ("Comunicação",           "Latência acima do previsto",            4),
    ("Armazenamento de Dados","Sincronização atrasada em 2 minutos",   2),
    ("Comunicação",           "Antena principal fora de alinhamento",  5),
    ("Habitação",             "Iluminação com consumo acima da média", 1),
    ("Agricultura",           "Sensor de umidade sem resposta",        3),
    ("Habitação",             "Queda de tensão no bloco B",            4),
    ("Comunicação",           "Pacote perdido isolado",                1),
    ("Suporte Médico",        "Monitor de sinais vitais sem resposta", 5),
    ("Laboratório",           "Calibração de sensor pendente",         2),
    ("Armazenamento de Dados","Disco de backup com 95% de uso",        4),
    ("Agricultura",           "Bomba de irrigação com corrente alta",  3),
]

print("=== ORDEM DE ENTRADA (bagunçada) ===")
for modulo, mensagem, criticidade in dados:
    print(f"[Criticidade {criticidade}] {modulo}: {mensagem}")
    registrar_alerta(modulo, mensagem, criticidade)

print("\n=== ORDEM DE SAÍDA (pelo heap) ===")
while alertas:
    neg_crit, modulo, mensagem = heapq.heappop(alertas)
    print(f"[Criticidade {-neg_crit}] {modulo}: {mensagem}")