import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

from ..models.nota_fiscal import NotaFiscal

NS = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}


def parse_xml(filepath: str) -> Optional[NotaFiscal]:
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        inf_nfe = root.find('.//nfe:infNFe', NS)
        if inf_nfe is None:
            return None

        chave = inf_nfe.get('Id', '').replace('NFe', '')

        ide = inf_nfe.find('nfe:ide', NS)
        numero = ide.findtext('nfe:nNF', '', NS)
        serie = ide.findtext('nfe:serie', '', NS)
        dh_emi = ide.findtext('nfe:dhEmi', None, NS) or ide.findtext('nfe:dEmi', '', NS)
        try:
            data_emissao = datetime.fromisoformat(dh_emi[:19]).isoformat()
        except Exception:
            data_emissao = datetime.now().isoformat()

        emit = inf_nfe.find('nfe:emit', NS)
        emit_cnpj = emit.findtext('nfe:CNPJ', emit.findtext('nfe:CPF', '', NS), NS) if emit else ''
        emit_nome = emit.findtext('nfe:xNome', '', NS) if emit else ''

        dest = inf_nfe.find('nfe:dest', NS)
        dest_cnpj = dest.findtext('nfe:CNPJ', dest.findtext('nfe:CPF', '', NS), NS) if dest else ''
        dest_nome = dest.findtext('nfe:xNome', '', NS) if dest else ''

        total = inf_nfe.find('nfe:total/nfe:ICMSTot', NS)
        valor = float(total.findtext('nfe:vNF', '0', NS)) if total else 0.0

        return NotaFiscal(
            chave_acesso=chave,
            numero=numero,
            serie=serie,
            data_emissao=data_emissao,
            emitente_cnpj=emit_cnpj,
            emitente_nome=emit_nome,
            destinatario_cnpj=dest_cnpj,
            destinatario_nome=dest_nome,
            valor_total=valor,
            tipo='xml',
            arquivo_original=filepath,
        )
    except Exception:
        return None
