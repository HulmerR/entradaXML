# 📊 Automação de Leitura de NFe para Excel

## 🧠 Descrição

Este projeto tem como objetivo automatizar a leitura de arquivos XML de Nota Fiscal Eletrônica (NFe) e extrair informações relevantes dos produtos para geração de uma planilha Excel.

A automação foi criada para auxiliar no lançamento manual de produtos em sistemas ERP, evitando retrabalho e reduzindo erros operacionais.

---

## ⚙️ Funcionalidades

- Leitura de arquivos XML de NFe
- Extração de dados dos produtos:
  - Código
  - Descrição
  - NCM
  - CFOP
  - Quantidade
  - Valor Unitário
  - Valor Total
  - Valor de ICMS ST
  - Valor do IPI
  - % do IPI
- Cálculo automático do **valor de custo**
- Geração de planilha Excel (`.xlsx`)

---

## 💰 Regra de Cálculo do Custo

### 📌 Sem ICMS ST:

Custo = Valor Unitário + (Valor Unitário * (% IPI / 100))

### 📌 Com ICMS ST:

Custo = (Valor Total + Valor ICMS ST + Valor IPI) / Quantidade

---

## 🛠️ Tecnologias Utilizadas

- Python 3
- xml.etree.ElementTree (leitura de XML)
- pandas (manipulação de dados)
- openpyxl (exportação para Excel)

---

## 🚀 Como Executar

### 1. Instalar Python
Baixar em: https://www.python.org/downloads/

> ⚠️ Marcar a opção **"Add Python to PATH"**

---

### 2. Instalar dependências

No terminal (CMD):
pip install pandas openpyxl

---

### 3. Estrutura do projeto
/NFe_Automacao
│
├── script.py
├── nota.xml
└── README.md

---

### 4. Executar o script

No terminal:
cd caminho/da/pasta
python script.py

---

### 5. Resultado

Será gerado um arquivo:
resultado.xlsx

---

## ⚠️ Observações Importantes

- O XML da NFe utiliza **namespace**, o que exige tratamento específico no código.
- Nem todas as NFe possuem ICMS ST — nesses casos, o valor será considerado como 0.
- Estruturas de ICMS podem variar (ICMS00, ICMS10, ICMS60, etc).

---

## 🧩 Possíveis Melhorias Futuras

- Processar múltiplos arquivos XML de uma vez
- Interface gráfica (sem necessidade de usar terminal)
- Validação de dados
- Exportação no formato específico para ERP
- Log de erros
- Tratamento de diferentes tipos de ICMS

---

## 📌 Versão

**v1.0 - Inicial**
- Leitura básica de NFe
- Extração de dados principais
- Geração de Excel com cálculo de custo

---

## 👨‍💻 Autor

Projeto desenvolvido por Rodrigo Hulmer como parte de estudos em automação com Python e aplicação prática em rotinas empresariais.
