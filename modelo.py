import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def treinar_modelo(X, y):
    """
    Treina um modelo simples de regressão linear.

    X: variável de entrada
    y: variável que queremos prever
    """

    X = np.array(X).reshape(-1, 1)
    y = np.array(y)

    modelo = LinearRegression()
    modelo.fit(X, y)

    return modelo


def avaliar_modelo(modelo, X, y):
    """
    Avalia o modelo utilizando MAE, MSE, RMSE e R².
    """

    X = np.array(X).reshape(-1, 1)
    y = np.array(y)

    previsoes = modelo.predict(X)

    mae = mean_absolute_error(y, previsoes)
    mse = mean_squared_error(y, previsoes)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, previsoes)

    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    }