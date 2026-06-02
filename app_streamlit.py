import os
import sqlite3
from contextlib import closing

import pandas as pd
import streamlit as st

from db import exporta_excel, inicializa_banco, processa_pasta

PASTA_NOTAS = "notas"
CAMINHO_DB = "notas.db"

st.title("Organizador de NF-e")

# Upload de múltiplos XMLs
arquivos = st.file_uploader(
    "Selecione os arquivos NF-e (.xml)",
    type=["xml"],
    accept_multiple_files=True,
)

if arquivos and st.button("Processar"):
    os.makedirs(PASTA_NOTAS, exist_ok=True)

    # Salva cada arquivo na pasta notas/ com o nome original
    for f in arquivos:
        destino = os.path.join(PASTA_NOTAS, f.name)
        with open(destino, "wb") as saida:
            saida.write(f.getbuffer())

    processa_pasta(pasta=PASTA_NOTAS, caminho_db=CAMINHO_DB)
    st.success(f"{len(arquivos)} arquivo(s) enviado(s) e processado(s).")

# Lê e exibe as notas do banco sempre que houver dados
inicializa_banco(CAMINHO_DB)
with closing(sqlite3.connect(CAMINHO_DB)) as conn:
    df = pd.read_sql_query("SELECT * FROM notas ORDER BY data_emissao", conn)

if not df.empty:
    st.subheader("Notas importadas")
    st.dataframe(df)

    exporta_excel(caminho_db=CAMINHO_DB)
    with open("relatorio_nfe.xlsx", "rb") as f:
        st.download_button(
            label="Baixar Excel",
            data=f.read(),
            file_name="relatorio_nfe.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
