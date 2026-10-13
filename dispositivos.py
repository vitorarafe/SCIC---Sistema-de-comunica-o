# ============================================================
# Dispositivos, bases numéricas e eletricidade básica (item 1.6)
# ============================================================

# Código de sensor de cada módulo. A parte depois do "-" é um número em HEXADECIMAL.
CODIGOS = {
    "Comunicacao":    "SNS-0A1",
    "Energia":        "SNS-0B2",
    "Comando":        "SNS-0C3",
    "Laboratorio":    "SNS-1D4",
    "Agricultura":    "SNS-2A1",
    "Habitacao":      "SNS-2B2",
    "Suporte Medico": "SNS-3C1",
    "Armazenamento":  "SNS-3D2",
}

# ---------- Eletricidade básica ----------

# Potência elétrica: P = V * I  (watts = volts * ampères)
def calcular_potencia(tensao, corrente):
    return tensao * corrente

# Lei de Ohm: R = V / I  (ohms = volts / ampères)
def calcular_resistencia(tensao, corrente):
    if corrente == 0:
        return None
    return tensao / corrente

# ---------- Bases numéricas ----------

# Recebe "SNS-0A1" e devolve só a parte hexadecimal: "0A1".
def extrair_hex(codigo):
    return codigo.split("-")[1]

# Converte o código hexadecimal para decimal e binário.
def converter_bases(codigo_hex):
    valor = int(codigo_hex, 16)
    binario = format(valor, "012b")
    return {"hex": codigo_hex.upper(), "decimal": valor, "binario": binario}


def mostrar_mapa_es():
    print("\n--- Entrada e saída de dados do SCIC ---")
    print("ENTRADA: medidor de carga (req/min), medidor de tensão e corrente, sensor de latência (simulados no CSV)")
    print("SAÍDA:   terminal (menu e tabelas), relatório técnico, arquivo CSV atualizado")
    print("INTERFACES (conceito): rede/Wi-Fi para telemetria dos módulos, USB para coleta manual de dados")


def mostrar_dispositivos(df):
    mostrar_mapa_es()
    print("\n--- Sensores e eletricidade por módulo (medição mais recente) ---")
    ultimos = df.drop_duplicates(subset="modulo", keep="last")
    for _, linha in ultimos.iterrows():
        codigo = CODIGOS.get(linha["modulo"])
        if codigo is None:
            print(f"{linha['modulo']}: sem código de sensor cadastrado")
            continue
        bases = converter_bases(extrair_hex(codigo))
        potencia = calcular_potencia(linha["tensao_v"], linha["corrente_a"])
        resistencia = calcular_resistencia(linha["tensao_v"], linha["corrente_a"])
        print(f"\n{linha['modulo']} | sensor {codigo}")
        print(f"  Código: hex {bases['hex']} = decimal {bases['decimal']} = binário {bases['binario']}")
        print(f"  {linha['tensao_v']} V x {linha['corrente_a']} A = {potencia:.1f} W | R = {resistencia:.2f} ohms")