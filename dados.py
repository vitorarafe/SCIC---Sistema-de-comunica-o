import pandas as pd


def carregar_dados():
    df = pd.read_csv("scic.csv")
    return df


def cadastrar_registro(modulo, latencia_observada, latencia_prevista, status):
    df = carregar_dados()
    df.loc[len(df)] = [modulo, latencia_observada, latencia_prevista, status]
    df.to_csv("scic.csv", index=False)
    print("Registro cadastrado!")


def consultar_registros(campo, valor):
    df = carregar_dados()
    resultado = df[df[campo] == valor]
    if len(resultado) == 0:
        print("Nenhum registro encontrado")
    else:
        print(resultado)
    return resultado