from decimal import Decimal
import xmltodict


def extrai_dados_nota(caminho_xml):
    with open(caminho_xml, "rb") as f:
        doc = xmltodict.parse(f)

    inf = doc["nfeProc"]["NFe"]["infNFe"]

    # Converte para centavos com Decimal para evitar erro de arredondamento
    valor_centavos = int(Decimal(inf["total"]["ICMSTot"]["vNF"]) * 100)

    return {
        "chave_acesso":          inf["@Id"].replace("NFe", ""),
        "numero":                inf["ide"]["nNF"],
        "data_emissao":          inf["ide"]["dhEmi"][:10],
        "cnpj_emitente":         inf["emit"]["CNPJ"],
        "nome_emitente":         inf["emit"]["xNome"],
        "valor_total_centavos":  valor_centavos,
    }
