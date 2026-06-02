# Organizador NF-e

Ferramenta para organizar notas fiscais eletrônicas (NF-e) brasileiras a partir de arquivos XML.

## O que faz

- Lê arquivos XML de NF-e (padrão SEFAZ)
- Armazena as notas em banco SQLite local
- Detecta notas duplicadas pela chave de acesso
- (planejado) Exporta para CSV / Excel
- (planejado) Interface web para visualização

## Requisitos

- Python 3.11+
- Dependências listadas em `requirements.txt`

## Instalação

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Uso

```powershell
python organizador.py
```

## Tecnologias

- `sqlite3` (stdlib) — banco de dados local
- `xml.etree.ElementTree` (stdlib) — parser NF-e
- Flask — interface web (em desenvolvimento)
