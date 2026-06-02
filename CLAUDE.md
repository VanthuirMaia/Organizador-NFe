# CLAUDE.md — Organizador NF-e

## Como rodar

```powershell
# Ativar venv
.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Rodar (quando houver entry point)
python organizador.py
```

## Estrutura atual

```
db.py            Camada de banco de dados (SQLite)
organizador.py   Entry point futuro da aplicação
requirements.txt flask, pdfplumber, openpyxl
```

## Regra de ouro

**Não aumentar a complexidade sem autorização.** Sugestões são bem-vindas, mas nenhuma decisão deliberada de design ou adição de código fora do escopo pedido sem aprovação explícita.

## Convenções

- **Banco de dados:** SQLite via `sqlite3` da stdlib, sem ORM
- **Valores monetários:** sempre em **centavos** (INTEGER) — ex: R$ 1.540,50 = `154050`
- **Chave de acesso:** 44 dígitos da NF-e, sem o prefixo `"NFe"`
- **Datas:** formato `YYYY-MM-DD` (TEXT no SQLite)
- **Comentários:** em português, diretos ao ponto
- **Funções simples:** sem classes desnecessárias, sem over-engineering

## Banco de dados (`db.py`)

| Coluna                | Tipo    | Descrição                         |
|-----------------------|---------|-----------------------------------|
| `chave_acesso`        | TEXT PK | 44 dígitos, sem prefixo "NFe"     |
| `numero`              | TEXT    | Número da NF-e                    |
| `data_emissao`        | TEXT    | YYYY-MM-DD                        |
| `cnpj_emitente`       | TEXT    | Só dígitos, sem formatação        |
| `nome_emitente`       | TEXT    | Razão social do emitente          |
| `valor_total_centavos`| INTEGER | Valor total em centavos           |

## O que ainda não existe

- Parser de XML NF-e
- Interface web / CLI
- Leitura e inserção de notas no banco
