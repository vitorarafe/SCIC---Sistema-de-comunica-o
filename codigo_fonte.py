from sklearn.model_selection import train_test_split
from estruturas import menu
from dados import carregar_dados
from modelo import treinar_modelo, prever, avaliar_modelo
from error import (calcular_erro_absoluto, calcular_erro_relativo,
                   analisar_precisao_flutuante)

import pandas as pd
pd.set_option("display.max_columns", None)  # mostra todas as colunas
pd.set_option("display.width", 200)         # não quebra a linha cedo


# Carregar dados do CSV
df = carregar_dados()
print("--- Dados carregados ---")
print(df)

# Treinar o modelo:Sendo a carga (X) e a latência (y)
X = df["carga_requisicoes"]
y = df["latencia_observada"]
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.3, random_state=42
)
modelo = treinar_modelo(X_treino, y_treino)

print("\n--- Modelo ---")
print(f"Coeficiente: {modelo.coef_[0]:.4f} ms por requisição")
print(f"Intercepto: {modelo.intercept_:.4f} ms")

metricas = avaliar_modelo(modelo, X_teste, y_teste)
print("\n--- Métricas (dados de teste) ---")
for nome, valor in metricas.items():
    print(f"{nome}: {valor:.4f}")

# Gerar previsões e calcular os erros
df["latencia_prevista"] = prever(modelo, X)
df["erro_absoluto"] = calcular_erro_absoluto(df["latencia_observada"], df["latencia_prevista"])
df["erro_relativo_percentual"] = calcular_erro_relativo(
    df["latencia_observada"], df["latencia_prevista"]
) * 100

print("\n--- Tabela de Erros por Módulo ---")
print(df[["modulo", "carga_requisicoes", "latencia_observada",
          "latencia_prevista", "erro_absoluto", "erro_relativo_percentual"]].round(3))

# Ponto flutuante
analisar_precisao_flutuante(df.loc[0, "latencia_observada"], df.loc[0, "latencia_prevista"])
menu(df)