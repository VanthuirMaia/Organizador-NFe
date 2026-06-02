import sqlite3


def cria_banco(caminho_db="notas.db"):
    # Abre conexão, cria tabela se não existir, fecha
    conn = sqlite3.connect(caminho_db)
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
    conn.commit()
    conn.close()
