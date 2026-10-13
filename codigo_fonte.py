import pandas as pd
from sklearn.model_selection import train_test_split

from dados import carregar_dados, cadastrar_registro, consultar_registros
from modelo import treinar_modelo, prever, avaliar_modelo
from error import (calcular_erro_absoluto, calcular_erro_relativo,
                   analisar_precisao_flutuante, classificar_erro)
from estruturas import (analisar_alertas, alerta_mais_urgente, construir_tries,
                        buscar_modulo, buscar_sensor)
from dispositivos import calcular_potencia, mostrar_dispositivos

# Mostra todas as colunas das tabelas no terminal, sem cortar com "...".
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

STATUS_VALIDOS = ("ativo", "manutencao", "alerta")


# ------------------------------------------------------------
# Preparação: carrega o CSV, treina o modelo e calcula tudo
# ------------------------------------------------------------
def preparar_sistema():
    df = carregar_dados()

    # Modelo: carga (X) e latência (y)
    X = df["carga_requisicoes"]
    y = df["latencia_observada"]
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    modelo = treinar_modelo(X_treino, y_treino)
    metricas = avaliar_modelo(modelo, X_teste, y_teste)

    # Previsões, erros e indicadores
    df["latencia_prevista"] = prever(modelo, X)
    df["erro_absoluto"] = calcular_erro_absoluto(df["latencia_observada"], df["latencia_prevista"])
    df["erro_relativo_percentual"] = calcular_erro_relativo(
        df["latencia_observada"], df["latencia_prevista"]
    ) * 100
    df["classificacao_erro"] = df["erro_relativo_percentual"].apply(classificar_erro)
    df["potencia_w"] = calcular_potencia(df["tensao_v"], df["corrente_a"])
    return df, modelo, metricas


# ------------------------------------------------------------
# Opções do menu
# ------------------------------------------------------------
# cadastra um registro novo. Devolve True se cadastrou.
def cadastrar_pelo_menu():
    try:
        modulo = input("Nome do módulo: ").strip()
        carga = float(input("Carga (req/min): "))
        tensao = float(input("Tensão (V): "))
        corrente = float(input("Corrente (A): "))
        latencia = float(input("Latência observada (ms): "))
    except ValueError:
        print("Valor numérico inválido. Cadastro cancelado.")
        return False

    status = input("Status (ativo/manutencao/alerta): ").strip().lower()
    if status not in STATUS_VALIDOS:
        print("Status inválido. Cadastro cancelado.")
        return False

    cadastrar_registro(modulo, carga, tensao, corrente, latencia, status)
    return True


# consulta registros por módulo ou status.
def consultar_pelo_menu():
    campo = input("Consultar por (digite modulo ou status): ").strip().lower()
    if campo not in ("modulo", "status"):
        print("Campo inválido.")
        return
    valor = remover_acentos(input("Valor (ex.: Comunicacao ou alerta): ").strip())

    # Padroniza maiúsculas/minúsculas para bater com o CSV.
    valor = valor.title() if campo == "modulo" else valor.lower()
    consultar_registros(campo, valor)


# indicadores e erros numéricos.
def mostrar_indicadores(df):
    print("\n--- Tabela de Erros por Módulo ---")
    print(df[["modulo", "carga_requisicoes", "latencia_observada", "latencia_prevista",
              "erro_absoluto", "erro_relativo_percentual", "classificacao_erro"]].round(3))
    print("\n--- Indicador: potência por módulo (P = V x I) ---")
    print(df[["modulo", "tensao_v", "corrente_a", "potencia_w"]])
    analisar_precisao_flutuante(df.loc[0, "latencia_observada"], df.loc[0, "latencia_prevista"])


# previsão de latência para uma carga digitada.
def prever_pelo_menu(modelo):
    try:
        carga = float(input("Carga do módulo (req/min): "))
    except ValueError:
        print("Valor numérico inválido.")
        return
    latencia = prever(modelo, [carga])[0]
    print(f"Latência prevista para {carga:.0f} req/min: {latencia:.1f} ms")


# métricas do modelo com interpretação.
def mostrar_metricas(modelo, metricas):
    print("\n--- Modelo: latência = a x carga + b ---")
    print(f"a (coeficiente): {modelo.coef_[0]:.4f} ms por requisição")
    print(f"b (intercepto): {modelo.intercept_:.4f} ms")
    print("\n--- Métricas (dados de teste) ---")
    for nome, valor in metricas.items():
        print(f"{nome}: {valor:.4f}")
    razao = metricas["RMSE"] / metricas["MAE"]
    print(f"\nRMSE / MAE = {razao:.2f}  (quanto maior, mais os erros grandes se concentram em poucos registros)")
    print("Atenção: R² alto não prova que o modelo é perfeito. Os dados são simulados e quase lineares.")

# análise final
LIMITE_TENDENCIA = 30.0

def ultimos_por_modulo(df):
    return df.drop_duplicates(subset="modulo", keep="last")

def calcular_tendencias(df):
    tendencias = []
    for modulo, grupo in df.groupby("modulo"):
        if len(grupo) < 2:
            continue
        primeira = grupo.iloc[0]
        ultima = grupo.iloc[-1]
        if primeira["potencia_w"] == 0 or primeira["latencia_observada"] == 0:
            continue
        var_potencia = (ultima["potencia_w"] - primeira["potencia_w"]) / primeira["potencia_w"] * 100
        var_latencia = (ultima["latencia_observada"] - primeira["latencia_observada"]) / primeira["latencia_observada"] * 100
        tendencias.append((modulo, var_potencia, var_latencia))
    return tendencias


def exibir_analise_final(df, metricas):
    ultimos = ultimos_por_modulo(df)

    print("\n==================== ANÁLISE FINAL DO SCIC ====================")

    # Resumo da operação
    print("\n1) RESUMO DA OPERAÇÃO")
    print(f"Registros: {len(df)} | Módulos: {df['modulo'].nunique()} | "
          f"Latência média observada: {df['latencia_observada'].mean():.1f} ms")
    contagem = df["status"].value_counts()
    print("Status dos registros: " + ", ".join(f"{s}: {n}" for s, n in contagem.items()))

    # Monitoramento contínuo: anomalias
    print("\n2) MONITORAMENTO CONTÍNUO (detecção de anomalias)")
    anomalias = df[df["classificacao_erro"] != "aceitavel"]
    if len(anomalias) == 0:
        print("Nenhum registro com erro fora do aceitável.")
    else:
        print(f"{len(anomalias)} de {len(df)} registros com erro relativo acima do aceitável:")
        for _, linha in anomalias.iterrows():
            print(f"  - {linha['modulo']} (carga {linha['carga_requisicoes']:.0f}): "
                  f"erro {linha['erro_relativo_percentual']:.1f}% -> {linha['classificacao_erro']}")

    # Automação: decisão rápida com o heap
    print("\n3) AUTOMAÇÃO (decisão rápida com o heap)")
    urgente = alerta_mais_urgente(df)
    if urgente is not None:
        pontos, modulo, mensagem = urgente
        print(f"Alerta mais urgente: {modulo} com {pontos:.1f} pts ({mensagem}).")
        print("Ação sugerida: acionar a equipe de infraestrutura para verificar este módulo primeiro.")

    # Redundância e microrrede
    print("\n4) REDUNDÂNCIA E MICRORREDE (consumo elétrico)")
    total = ultimos["potencia_w"].sum()
    maior = ultimos.loc[ultimos["potencia_w"].idxmax()]
    parte = maior["potencia_w"] / total * 100
    print(f"Potência total (medições mais recentes): {total:.1f} W.")
    print(f"{maior['modulo']} consome {maior['potencia_w']:.1f} W ({parte:.0f}% do total).")
    em_alerta = ultimos[ultimos["status"] == "alerta"]["modulo"].tolist()
    if em_alerta:
        print("Módulos em alerta na medição mais recente: " + ", ".join(em_alerta) + ".")
        print("Sugestão: enlace redundante (rota alternativa de comunicação) para esses módulos, "
              "e backup dos dados deles em outro módulo de armazenamento.")

    # Manutenção preditiva
    print("\n5) MANUTENÇÃO PREDITIVA (tendência entre a 1ª e a última medição)")
    tendencias = calcular_tendencias(df)
    if len(tendencias) == 0:
        print("Poucos registros para calcular tendência.")
    for modulo, var_pot, var_lat in tendencias:
        sinal = "ATENÇÃO" if var_pot >= LIMITE_TENDENCIA else "estável"
        print(f"  - {modulo}: potência {var_pot:+.1f}%, latência {var_lat:+.1f}% -> {sinal}")
    print(f"(Sugerimos inspeção preventiva quando a potência sobe {LIMITE_TENDENCIA:.0f}% ou mais.)")

    # Limites e supervisão humana
    print("\n6) LIMITES E SUPERVISÃO HUMANA")
    print(f"Modelo: R² = {metricas['R2']:.4f}, MAE = {metricas['MAE']:.2f} ms, RMSE = {metricas['RMSE']:.2f} ms.")
    print("Os dados são simulados e a amostra é pequena; por isso as métricas servem como demonstração.")
    print("Este sistema apoia a decisão, mas a validação final é da equipe humana da colônia.")
    print("===============================================================")

# ------------------------------------------------------------
# Menu principal
# ------------------------------------------------------------
def menu():
    df, modelo, metricas = preparar_sistema()
    trie_nomes, trie_codigos = construir_tries(df)

    while True:
        print("\n=== SCIC - AURORA SIGER ===")
        print("1 - Cadastrar registro")
        print("2 - Consultar registros")
        print("3 - Indicadores e erros numéricos")
        print("4 - Prever latência")
        print("5 - Métricas do modelo")
        print("6 - Priorizar alertas (heap)")
        print("7 - Buscar módulo por nome (trie)")
        print("8 - Buscar sensor por código (trie)")
        print("9 - Dispositivos, bases numéricas e eletricidade")
        print("10 - Análise final (gerenciamento inteligente)")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            if cadastrar_pelo_menu():
                # Dados mudaram: refaz modelo, erros e tries.
                df, modelo, metricas = preparar_sistema()
                trie_nomes, trie_codigos = construir_tries(df)
        elif opcao == "2":
            consultar_pelo_menu()
        elif opcao == "3":
            mostrar_indicadores(df)
        elif opcao == "4":
            prever_pelo_menu(modelo)
        elif opcao == "5":
            mostrar_metricas(modelo, metricas)
        elif opcao == "6":
            analisar_alertas(df)
        elif opcao == "7":
            buscar_modulo(trie_nomes)
        elif opcao == "8":
            buscar_sensor(trie_codigos)
        elif opcao == "9":
            mostrar_dispositivos(df)
        elif opcao == "10":
            exibir_analise_final(df, metricas)
        elif opcao == "0":
            print("Encerrando o SCIC. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()