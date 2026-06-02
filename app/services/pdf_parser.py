import hashlib
import re
from datetime import datetime
from typing import Optional

from ..models.nota_fiscal import NotaFiscal

try:
    import pdfplumber
    _PDF_DISPONIVEL = True
except ImportError:
    _PDF_DISPONIVEL = False

_CNPJ_RE = re.compile(r'\d{2}[.\s]?\d{3}[.\s]?\d{3}[/\s]?\d{4}[-\s]?\d{2}')
_DATE_RE = re.compile(r'\b(\d{2})/(\d{2})/(\d{4})\b')
_VALOR_RE = re.compile(r'(?:valor\s+total|total\s+da\s+nota|valor\s+total\s+da\s+nf)[\s:R$]*?([\d.]+,\d{2})', re.IGNORECASE)
_NF_NUM_RE = re.compile(r'(?:N[º°\s.]|NF[\s-]?N[º°]?)[\s.:]*0*(\d+)', re.IGNORECASE)
_SERIE_RE = re.compile(r'S[ÉE]RIE[\s.:]*(\d+)', re.IGNORECASE)


def _limpar_cnpj(raw: str) -> str:
    return re.sub(r'\D', '', raw)


def _parse_valor(text: str) -> float:
    m = _VALOR_RE.search(text)
    if m:
        v = m.group(1).replace('.', '').replace(',', '.')
        try:
            return float(v)
        except ValueError:
            pass
    return 0.0


def parse_pdf(filepath: str) -> Optional[NotaFiscal]:
    if not _PDF_DISPONIVEL:
        return None
    try:
        with pdfplumber.open(filepath) as pdf:
            text = '\n'.join(page.extract_text() or '' for page in pdf.pages)

        if not text.strip():
            return None

        cnpjs = [_limpar_cnpj(m) for m in _CNPJ_RE.findall(text)]
        emit_cnpj = cnpjs[0] if cnpjs else ''
        dest_cnpj = cnpjs[1] if len(cnpjs) > 1 else ''

        date_m = _DATE_RE.search(text)
        if date_m:
            try:
                data_emissao = datetime(
                    int(date_m.group(3)), int(date_m.group(2)), int(date_m.group(1))
                ).isoformat()
            except ValueError:
                data_emissao = datetime.now().isoformat()
        else:
            data_emissao = datetime.now().isoformat()

        nf_m = _NF_NUM_RE.search(text)
        numero = nf_m.group(1) if nf_m else '0'

        serie_m = _SERIE_RE.search(text)
        serie = serie_m.group(1) if serie_m else '1'

        valor = _parse_valor(text)

        chave = hashlib.sha256(text.encode()).hexdigest()[:44]

        return NotaFiscal(
            chave_acesso=chave,
            numero=numero,
            serie=serie,
            data_emissao=data_emissao,
            emitente_cnpj=emit_cnpj,
            emitente_nome='',
            destinatario_cnpj=dest_cnpj,
            destinatario_nome='',
            valor_total=valor,
            tipo='pdf',
            arquivo_original=filepath,
        )
    except Exception:
        return None
