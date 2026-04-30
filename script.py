import xml.etree.ElementTree as ET
import pandas as pd

# Nome do XML
arquivo_xml = 'nota.xml'

# Ler XML
tree = ET.parse(arquivo_xml)
root = tree.getroot()

# Namespace
ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

dados = []

for det in root.findall('.//nfe:det', ns):

    prod = det.find('nfe:prod', ns)
    imposto = det.find('nfe:imposto', ns)

    codigo = prod.findtext('nfe:cProd', default='', namespaces=ns)
    descricao = prod.findtext('nfe:xProd', default='', namespaces=ns)
    ncm = prod.findtext('nfe:NCM', default='', namespaces=ns)
    cfop = prod.findtext('nfe:CFOP', default='', namespaces=ns)

    quantidade = float(prod.findtext('nfe:qCom', default='0', namespaces=ns))
    valor_unitario = float(prod.findtext('nfe:vUnCom', default='0', namespaces=ns))
    valor_total = float(prod.findtext('nfe:vProd', default='0', namespaces=ns))

    # IPI
    v_ipi = 0.0
    p_ipi = 0.0

    ipi = imposto.find('.//nfe:IPI', ns)
    if ipi is not None:
        v_ipi = float(ipi.findtext('.//nfe:vIPI', default='0', namespaces=ns))
        p_ipi = float(ipi.findtext('.//nfe:pIPI', default='0', namespaces=ns))

    # ICMS ST
    v_st = 0.0
    icms_st = imposto.find('.//nfe:ICMSST', ns)
    if icms_st is not None:
        v_st = float(icms_st.findtext('nfe:vST', default='0', namespaces=ns))

    # Cálculo do custo
    if v_st == 0:
        custo = valor_unitario + (valor_unitario * (p_ipi / 100))
    else:
        custo = (valor_total + v_st + v_ipi) / quantidade if quantidade > 0 else 0

    dados.append({
        'Código': codigo,
        'Descrição': descricao,
        'NCM': ncm,
        'CFOP': cfop,
        'Quantidade': quantidade,
        'Valor Unitário': valor_unitario,
        'Valor Total': valor_total,
        'ICMS ST': v_st,
        'Valor IPI': v_ipi,
        '% IPI': p_ipi,
        'Custo': round(custo, 2)
    })

df = pd.DataFrame(dados)
df.to_excel('resultado.xlsx', index=False)

print("Planilha criada com sucesso!")