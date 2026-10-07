from dados import *

print(carregar_dados())
cadastrar_registro("Energia", 200.0, 210.0, "ativo")
consultar_registros("status", "alerta")
consultar_registros("modulo", "Energia")