from dataclasses import dataclass, asdict, field


@dataclass
class NotaFiscal:
    chave_acesso: str
    numero: str
    serie: str
    data_emissao: str
    emitente_cnpj: str
    emitente_nome: str
    destinatario_cnpj: str
    destinatario_nome: str
    valor_total: float
    tipo: str
    arquivo_original: str
    arquivo_organizado: str = ''
    duplicata: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> 'NotaFiscal':
        campos = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**campos)
