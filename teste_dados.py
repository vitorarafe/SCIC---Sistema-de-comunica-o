from dados import *

print(carregar_dados())
cadastrar_registro("Energia", 140, 24, 0.9, 82.0, "ativo")
consultar_registros("status", "alerta")
consultar_registros("modulo", "Energia")