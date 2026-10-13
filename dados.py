import os
import pandas as pd

CAMINHO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scic.csv")


def carregar_dados():
    df = pd.read_csv(CAMINHO_CSV)
    return df


def cadastrar_registro(modulo, carga_requisicoes, latencia_observada, status):
    df = carregar_dados()
    df.loc[len(df)] = [modulo, carga_requisicoes, latencia_observada, status]
    df.to_csv(CAMINHO_CSV, index=False)
    print("Registro cadastrado!")


def consultar_registros(campo, valor):
    df = carregar_dados()
    resultado = df[df[campo] == valor]
    if len(resultado) == 0:
        print("Nenhum registro encontrado")
    else:
        print(resultado)
    return resultado