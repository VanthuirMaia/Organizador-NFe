import glob
import os
import sqlite3
from contextlib import closing

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
