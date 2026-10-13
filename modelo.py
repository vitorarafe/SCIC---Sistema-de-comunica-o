import numpy as np
from sklearn.linear_model import LinearRegression
from error import avaliar_performance_modelo


def treinar_modelo(X, y):
    X = np.array(X).reshape(-1, 1)
    y = np.array(y)
    modelo = LinearRegression()
    modelo.fit(X, y)
    return modelo


def prever(modelo, X):
    X = np.array(X).reshape(-1, 1)
    return modelo.predict(X)


def avaliar_modelo(modelo, X, y):
    previsoes = prever(modelo, X)
    return avaliar_performance_modelo(y, previsoes)