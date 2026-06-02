import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

from ..models.nota_fiscal import NotaFiscal


def _sanitizar(nome: str) -> str:
    return re.sub(r'[<>:"/\\|?*\s]', '_', nome).strip('_')


def gerar_nome(nota: NotaFiscal) -> str:
    try:
        data = datetime.fromisoformat(nota.data_emissao)
        data_str = data.strftime('%Y%m%d')
    except Exception:
        data_str = 'sem_data'

    emitente = _sanitizar(nota.emitente_nome[:30]) if nota.emitente_nome else nota.emitente_cnpj
    valor_str = f'{nota.valor_total:.2f}'.replace('.', ',')
    return f'{data_str}_{emitente}_NF{nota.numero}_R${valor_str}.{nota.tipo}'


def detectar_duplicatas(notas: List[NotaFiscal]) -> List[NotaFiscal]:
    vistas: set = set()
    for nota in notas:
        if nota.chave_acesso in vistas:
            nota.duplicata = True
        else:
            vistas.add(nota.chave_acesso)
            nota.duplicata = False
    return notas


def organizar_arquivos(notas: List[NotaFiscal], destino: str) -> List[NotaFiscal]:
    destino_path = Path(destino)
    for nota in notas:
        if nota.duplicata:
            continue
        try:
            data = datetime.fromisoformat(nota.data_emissao)
            pasta = destino_path / str(data.year) / f'{data.month:02d}'
        except Exception:
            pasta = destino_path / 'sem_data'
        pasta.mkdir(parents=True, exist_ok=True)

        nome_novo = gerar_nome(nota)
        destino_arquivo = pasta / nome_novo

        origem = Path(nota.arquivo_original)
        if origem.exists() and not destino_arquivo.exists():
            shutil.copy2(str(origem), str(destino_arquivo))

        nota.arquivo_organizado = str(destino_arquivo)
    return notas
