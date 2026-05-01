import xml.etree.ElementTree as ET
import pandas as pd
import glob
import os

def processar_xml(caminho_xml):
    try:
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
    except Exception as e:
        print(f"Erro ao ler {caminho_xml}: {e}")
        return []

    def get_text(element, tag, default='0'):
        # Procura a tag recursivamente dentro do elemento
        for val in element.iter():
            if val.tag.endswith(tag):
                return val.text
        return default

    dados_xml = []

    # Busca todos os elementos 'det' (detalhes do produto)
    for det in root.iter():
        if not det.tag.endswith('det'):
            continue
            
        # Extração flexível dos campos
        prod = next((c for c in det if c.tag.endswith('prod')), det)
        imposto = next((c for c in det if c.tag.endswith('imposto')), det)

        codigo = get_text(prod, 'cProd', '')
        descricao = get_text(prod, 'xProd', '')
        ncm = get_text(prod, 'NCM', '')
        cfop = get_text(prod, 'CFOP', '')

        quantidade = float(get_text(prod, 'qCom', '0'))
        valor_unitario = float(get_text(prod, 'vUnCom', '0'))
        valor_total = float(get_text(prod, 'vProd', '0'))

        # IPI
        v_ipi = 0.0
        p_ipi = 0.0
        ipi = next((c for c in imposto.iter() if c.tag.endswith('IPI')), None)
        if ipi is not None:
            v_ipi = float(get_text(ipi, 'vIPI', '0'))
            p_ipi = float(get_text(ipi, 'pIPI', '0'))

        # ICMS ST (Pode ser vICMSST ou vST)
        v_st = 0.0
        icms = next((c for c in imposto.iter() if c.tag.endswith('ICMS')), None)
        if icms is not None:
            # Tenta vICMSST primeiro, depois vST
            v_st_text = get_text(icms, 'vICMSST', None)
            if v_st_text is None:
                v_st_text = get_text(icms, 'vST', '0')
            
            try:
                v_st = float(v_st_text)
            except (ValueError, TypeError):
                v_st = 0.0

        # Cálculo do custo
        if v_st == 0:
            custo = valor_unitario + (valor_unitario * (p_ipi / 100))
        else:
            custo = (valor_total + v_st + v_ipi) / quantidade if quantidade > 0 else 0

        dados_xml.append({
            'Arquivo': os.path.basename(caminho_xml),
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
    
    return dados_xml

# --- Interface Principal ---

pasta_xml = 'xml'
if not os.path.exists(pasta_xml):
    os.makedirs(pasta_xml)
    print(f"Pasta '{pasta_xml}' criada. Mova seus XMLs para lá.")

# Lista arquivos na pasta xml
arquivos = glob.glob(os.path.join(pasta_xml, '*.xml'))

if not arquivos:
    print(f"\n[!] Nenhum arquivo XML encontrado na pasta '{pasta_xml}'.")
    print("Por favor, coloque os arquivos na pasta e tente novamente.")
else:
    print("\n" + "="*50)
    print(" ARQUIVOS XML DISPONÍVEIS ".center(50, "="))
    print("="*50)
    for i, arquivo in enumerate(arquivos, 1):
        print(f"[{i}] {os.path.basename(arquivo)}")
    print("-" * 50)
    
    entrada = input("\nDigite os números desejados (ex: 1,3) ou 'T' para TODOS: ").strip().upper()
    
    arquivos_selecionados = []
    if entrada == 'T':
        arquivos_selecionados = arquivos
    else:
        try:
            indices = [int(x.strip()) - 1 for x in entrada.split(',')]
            arquivos_selecionados = [arquivos[i] for i in indices if 0 <= i < len(arquivos)]
        except Exception:
            print("\n[Erro] Entrada inválida. Use números separados por vírgula.")

    if arquivos_selecionados:
        todos_dados = []
        print("\nIniciando processamento...")
        
        for arquivo in arquivos_selecionados:
            print(f" -> Lendo: {os.path.basename(arquivo)}")
            dados = processar_xml(arquivo)
            todos_dados.extend(dados)

        if todos_dados:
            df = pd.DataFrame(todos_dados)
            # Reorganiza as colunas para que 'Arquivo' seja a primeira
            cols = ['Arquivo'] + [c for c in df.columns if c != 'Arquivo']
            df = df[cols]
            
            try:
                df.to_excel('resultado.xlsx', index=False)
                print(f"\n[Sucesso] {len(todos_dados)} itens exportados para 'resultado.xlsx'.")
            except PermissionError:
                print("\n[Erro] Não foi possível salvar. O arquivo 'resultado.xlsx' está aberto.")
        else:
            print("\n[Aviso] Nenhum dado válido encontrado nos arquivos selecionados.")