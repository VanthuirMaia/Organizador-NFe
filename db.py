import sqlite3
from contextlib import closing


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
