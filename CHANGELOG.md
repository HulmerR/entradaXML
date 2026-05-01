# Changelog - Sistema de Extração de XML (entradaXML)

## [1.1.0] - 2026-05-01
### Adicionado
- **Interface Interativa**: Implementado menu no console que lista os arquivos XML disponíveis e permite ao usuário selecionar quais deseja processar (por número ou a opção 'T' para todos).
- **Redirecionamento de Pasta**: O script agora busca arquivos exclusivamente dentro da subpasta `xml/`.
- **Criação Automática de Diretório**: O script verifica se a pasta `xml/` existe e a cria automaticamente caso contrário.
- **Coluna de Origem**: Adicionada a coluna "Arquivo" no Excel para identificar a origem de cada item processado.

### Melhorado
- **Robustez na Extração**: Substituída a busca estrita por uma busca flexível (`endswith`), permitindo que o script encontre as tags mesmo com diferentes namespaces ou versões de NF-e.
- **Tratamento de Erros**: Adicionado aviso específico caso o arquivo `resultado.xlsx` esteja aberto no momento da exportação (PermissionError).

### Adicionado
- **Processamento em Lote**: Capacidade de processar múltiplos arquivos XML de uma só vez e consolidar os dados em uma única planilha.

### Corrigido
- **ICMS ST**: Corrigida a tag de extração de `vST` para `vICMSST`, garantindo que os valores de substituição tributária sejam capturados corretamente em notas fiscais de diferentes fornecedores.

### Corrigido
- **Bug do Loop (Planilha em Branco)**: Removido um comando `break` que estava interrompendo o processamento logo no primeiro item, o que causava a geração de arquivos vazios.

## [1.0.0] - 2026-05-01
### Inicial
- Versão base do script para leitura de XML de NF-e e cálculo de custo unitário.
