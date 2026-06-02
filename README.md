# Organizador de NF-e

Ferramenta que lê XMLs de notas fiscais eletrônicas (NF-e), extrai os dados principais e organiza tudo em um relatório Excel. Tem interface web (Streamlit) para uso por pessoas não técnicas e também funciona via terminal.

## O que faz

- Lê arquivos XML de NF-e (upload na interface ou pasta local)
- Extrai chave de acesso, número, data, CNPJ e nome do emitente, e valor total
- Guarda tudo em um banco SQLite, sem duplicar notas já processadas
- Gera um relatório Excel com duas abas: todas as notas e o total por mês

## Como funciona por dentro

- **Banco como fonte de verdade.** Os dados ficam em SQLite. O Excel é só uma saída gerada a partir do banco, descartável.
- **Idempotente.** A chave de acesso da NF-e (44 dígitos) é a chave primária. Reprocessar os mesmos arquivos não duplica nada: usa INSERT OR IGNORE, então rodar uma vez ou dez vezes dá o mesmo resultado.
- **Tratamento de erro observável.** Um XML corrompido no meio do lote não derruba os outros. O arquivo problemático é reportado com o motivo, e o processamento continua.
- **Valor em centavos.** Valores monetários são guardados como inteiro (centavos), evitando erro de arredondamento de float. A conversão para reais acontece só na exibição.

## Stack

Python, Streamlit, pandas, xmltodict, SQLite, openpyxl

## Como rodar

Clone o repositório:

\```bash
git clone https://github.com/VanthuirMaia/Organizador-NFe
cd organizador-nfe
\```

Crie o ambiente e instale as dependências:

\```bash
python -m venv .venv
.venv\Scripts\activate # Windows

# source .venv/bin/activate # Linux/Mac

pip install -r requirements.txt
\```

Rode a interface web:

\```bash
streamlit run app_streamlit.py
\```

Ou processe via terminal, colocando os XMLs na pasta `notas/`:

\```python
from db import processa_pasta, exporta_excel
processa_pasta()
exporta_excel()
\```

## Observação

Os XMLs incluídos na pasta `notas/` são fictícios, gerados apenas para teste e demonstração.
