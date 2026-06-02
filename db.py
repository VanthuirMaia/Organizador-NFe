import glob
import os
import sqlite3
from contextlib import closing

import pandas as pd

from extrator import extrai_dados_nota


def inicializa_banco(caminho_db="notas.db"):
    # closing garante o close(); with conn faz commit/rollback automático
    with closing(sqlite3.connect(caminho_db)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notas (
                    chave_acesso          TEXT PRIMARY KEY,
                    numero                TEXT,
                    data_emissao          TEXT,
                    cnpj_emitente         TEXT,
                    nome_emitente         TEXT,
                    valor_total_centavos  INTEGER
                )
            """)


def insere_nota(conn, dados):
    # INSERT OR IGNORE: ignora silenciosamente se a chave_acesso já existir
    conn.execute(
        """
        INSERT OR IGNORE INTO notas
            (chave_acesso, numero, data_emissao, cnpj_emitente, nome_emitente, valor_total_centavos)
        VALUES
            (?, ?, ?, ?, ?, ?)
        """,
        (
            dados["chave_acesso"],
            dados["numero"],
            dados["data_emissao"],
            dados["cnpj_emitente"],
            dados["nome_emitente"],
            dados["valor_total_centavos"],
        ),
    )


def processa_pasta(pasta="notas", caminho_db="notas.db"):
    # Garante que a tabela existe antes de qualquer coisa
    inicializa_banco(caminho_db)

    arquivos = glob.glob(os.path.join(pasta, "*.xml"))

    # Uma conexão, uma transação para todos os arquivos válidos
    with closing(sqlite3.connect(caminho_db)) as conn:
        with conn:
            for arquivo in arquivos:
                try:
                    dados = extrai_dados_nota(arquivo)
                    insere_nota(conn, dados)
                except Exception as e:
                    print(f"Falhou: {arquivo} -> {e}")

    print(f"{len(arquivos)} arquivo(s) encontrado(s) em '{pasta}'")


def exporta_excel(caminho_db="notas.db", caminho_saida="relatorio_nfe.xlsx"):
    with closing(sqlite3.connect(caminho_db)) as conn:
        df = pd.read_sql_query("SELECT * FROM notas ORDER BY data_emissao", conn)

    # Valor em reais e mês/ano extraídos do texto YYYY-MM-DD
    df["valor_reais"] = df["valor_total_centavos"] / 100
    df["mes_ano"] = df["data_emissao"].str[5:7] + "/" + df["data_emissao"].str[:4]

    colunas_notas = ["chave_acesso", "numero", "data_emissao", "cnpj_emitente", "nome_emitente", "valor_reais", "mes_ano"]
    resumo = df.groupby("mes_ano", sort=False)["valor_reais"].sum().reset_index()
    resumo.columns = ["mes_ano", "valor_reais"]

    with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
        df[colunas_notas].to_excel(writer, sheet_name="notas", index=False)
        resumo.to_excel(writer, sheet_name="resumo", index=False)

    print(caminho_saida)
