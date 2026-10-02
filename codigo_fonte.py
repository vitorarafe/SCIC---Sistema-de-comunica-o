import pandas as pd
import numpy as np
from error import calcular_erro_absoluto, calcular_erro_relativo, avaliar_performance_modelo, analisar_precisao_flutuante

# 1. Simulação de carregamento de dados (Item 1.1)

dados = {
    'modulo': ['Habitacao', 'Laboratorio', 'Comando', 'Agricultura'],
    'latencia_observada': [45.2, 120.5, 12.1, 85.0],
    'latencia_prevista': [45.0, 115.0, 12.100000000000001, 90.0]
}
df = pd.DataFrame(dados)

# 2. Aplicação das funções de erro (Item 1.2)
df['erro_absoluto'] = calcular_erro_absoluto(df['latencia_observada'], df['latencia_prevista'])
df['erro_relativo'] = calcular_erro_relativo(df['latencia_observada'], df['latencia_prevista'])
df['erro_relativo_percentual'] = df['erro_relativo'] * 100

print("--- Tabela de Erros por Módulo ---")
print(df[['modulo', 'erro_absoluto', 'erro_relativo_percentual']])

# 3. Avaliação Global do Modelo (Item 1.3)
metricas = avaliar_performance_modelo(df['latencia_observada'], df['latencia_prevista'])
print("\n--- Métricas de Performance do Modelo ---")
for metrica, valor in metricas.items():
    print(f"{metrica}: {valor:.4f}")

# 4. Demonstração de ponto flutuante com o módulo Comando
lat_obs_comando = df.loc[2, 'latencia_observada']
lat_prev_comando = df.loc[2, 'latencia_prevista']
analisar_precisao_flutuante(lat_obs_comando, lat_prev_comando)