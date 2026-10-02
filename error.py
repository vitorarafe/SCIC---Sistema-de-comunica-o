import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def calcular_erro_absoluto(valor_real, valor_previsto):
    """
    Calcula o erro absoluto entre o valor observado e o previsto.
    Fórmula: | real - previsto |
    """
    return np.abs(valor_real - valor_previsto)

def calcular_erro_relativo(valor_real, valor_previsto):
    """
    Calcula o erro relativo, útil para comparar módulos com escalas diferentes.
    Fórmula: | real - previsto | / | real |
    """
    erro_absoluto = calcular_erro_absoluto(valor_real, valor_previsto)
    # Evita divisão por zero caso o valor real seja exatamente 0
    erro_relativo = np.where(valor_real != 0, erro_absoluto / np.abs(valor_real), 0.0)
    return erro_relativo

def avaliar_performance_modelo(y_real, y_previsto):
    """
    Retorna um dicionário com as métricas de regressão exigidas no item 1.3.
    """
    mae = mean_absolute_error(y_real, y_previsto)
    mse = mean_squared_error(y_real, y_previsto)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_real, y_previsto)
    
    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    }

def analisar_precisao_flutuante(valor_real, valor_previsto):
    """
    Demonstra as diferenças numéricas causadas por representação em ponto flutuante,
    atendendo ao requisito 1.2 da rubrica.
    """
    diff_exata = valor_real - valor_previsto
    
    print("\n--- Análise de Ponto Flutuante ---")
    print(f"Diferença bruta no Python (ponto flutuante): {diff_exata}")
    print(f"Diferença arredondada (3 casas decimais): {round(diff_exata, 3)}")
    if diff_exata != round(diff_exata, 3):
        print("Nota: A diferença entre o valor bruto e o arredondado demonstra "
              "a limitação de precisão numérica em cálculos de máquina.")