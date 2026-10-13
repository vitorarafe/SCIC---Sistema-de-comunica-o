# SCIC - Sistema de Comunicação Interplanetária da Colônia

Protótipo em Python desenvolvido para a Atividade Integradora da Aurora Siger.
O sistema organiza dados operacionais e de comunicação dos módulos da colônia,
avalia a confiabilidade de uma previsão simples de latência, prioriza alertas
críticos, permite buscas eficientes e gera uma análise final de apoio à decisão.

> Os dados são **simulados**. As métricas do modelo servem como demonstração.

## Arquivos da entrega

| Arquivo | Função |
|---|---|
| `codigo_fonte.py` | **Arquivo principal.** Menu do sistema, cálculo de indicadores e análise final. |
| `dados.py` | Leitura, cadastro e consulta de registros no CSV (Pandas). |
| `error.py` | Erro absoluto, erro relativo, métricas (MAE, MSE, RMSE, R²) e ponto flutuante. |
| `modelo.py` | Regressão linear: carga (req/min) → latência (ms). |
| `estruturas.py` | Heap (priorização de alertas) e trie (busca por prefixo). |
| `dispositivos.py` | Códigos de sensor em hexadecimal/decimal/binário, potência e lei de Ohm. |
| `dados_aurora_siger.csv` | Base de dados simulada da Aurora Siger. |
| `relatorio_tecnico.pdf` | Relatório técnico do projeto. |
| `link_video.txt` | Link do vídeo de apresentação (YouTube, não listado). |

## Dependências

- Python 3
- pandas
- numpy
- scikit-learn

Instalação:

```bash
python -m pip install pandas numpy scikit-learn
```

```bash
python codigo_fonte.py
```

O menu abre direto no terminal.

## Dados

O arquivo `dados_aurora_siger.csv` contém 14 medições de 8 módulos da colônia:

| Coluna | Significado |
|---|---|
| `modulo` | Nome do módulo (Comando, Comunicacao, Energia, etc.) |
| `carga_requisicoes` | Requisições por minuto atendidas pelo módulo (**entrada X do modelo**) |
| `tensao_v` | Tensão elétrica medida (V) |
| `corrente_a` | Corrente elétrica medida (A) |
| `latencia_observada` | Latência medida (ms) (**saída y do modelo**) |
| `status` | `ativo`, `manutencao` ou `alerta` |

## Menu do sistema

| Opção | O que faz |
|---|---|
| 1 | Cadastra um novo registro no CSV (com validação de entrada). |
| 2 | Consulta registros por módulo ou status. |
| 3 | Mostra erro absoluto, erro relativo, classificação do erro (aceitável, atenção, preocupante), potência (P = V × I) e a análise de ponto flutuante. |
| 4 | Prevê a latência para uma carga digitada. |
| 5 | Mostra o modelo e as métricas MAE, MSE, RMSE e R², com interpretação. |
| 6 | Prioriza alertas com **heap** (top 5 do mais urgente ao menos urgente). |
| 7 | Busca módulo por prefixo do nome com **trie**. |
| 8 | Busca sensor por prefixo do código com **trie**. |
| 9 | Dispositivos de entrada e saída, conversão de bases numéricas e cálculos de eletricidade. |
| 10 | Análise final: gerenciamento inteligente da comunicação, calculado a partir dos dados. |
| 0 | Sai do sistema. |

## Como o sistema funciona

1. **Modelo:** uma regressão linear aprende `latência = a × carga + b`.
   Os dados são divididos em treino (70%) e teste (30%), e as métricas são
   calculadas nos dados de teste.
2. **Erros:** a diferença entre a latência prevista pelo modelo e a observada
   gera o erro absoluto e o erro relativo (%). Erros abaixo de 3% são
   aceitáveis, entre 3% e 5% pedem atenção e a partir de 5% são preocupantes.
3. **Heap:** cada registro vira um alerta com nota
   `criticidade × 10 + erro relativo (%) × 2`. O heap entrega sempre o mais
   urgente primeiro, sem precisar ordenar a lista inteira.
4. **Trie:** guarda nomes de módulos e códigos de sensores, e encontra todos
   os registros que começam com um prefixo digitado.
5. **Dispositivos:** o código do sensor (ex.: `SNS-0A1`) termina em um número
   hexadecimal, convertido para decimal e binário. A potência de cada módulo
   é calculada por `P = V × I`.
6. **Análise final:** resume anomalias, o alerta mais urgente, o consumo
   elétrico (microrrede), a tendência por módulo (manutenção preditiva) e os
   limites do sistema.

## Exemplos de execução

- Opção 4 com `250` → `Latência prevista para 250 req/min: 144.7 ms`
- Opção 6 → o primeiro alerta é `Agricultura` (57.7 pts)
- Opção 7 com `co` → `Comando` e `Comunicacao`
- Opção 8 com `sns-0c3` → `SNS-0C3 -> Comando (ativo)`

## Autor

```bash
Integrantes
Nome: ANA CAROLINA FREIRE MAFRA – rm573650
Nome: Daniel Guimarães Barreto – rm573425
Nome: Paulo Henrique da Silva Gola – rm572992
Nome: Vinicius Daniel de Borba – rm572091
Nome: Vitor de Araujo Ferreira – rm572838

---

Projeto desenvolvido para fins acadêmicos.
