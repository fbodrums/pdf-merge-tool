# pdf-merge

## Purpose

Merge de páginas extraídas na ordem dos arquivos, download e processamento efêmero. Sincronizado a partir do change `pdf-merge-tool`.

## Requirements

### Requirement: Merge de páginas em PDF único
O sistema DEVE combinar todas as páginas extraídas dos múltiplos PDFs em um único arquivo PDF final. A ordem dos arquivos DEVE ser respeitada: todas as páginas do arquivo 1 primeiro, depois do arquivo 2, e assim por diante.

#### Scenario: Merge de 3 PDFs com configuração padrão
- **WHEN** o usuário faz upload de 3 PDFs (A com 5 páginas, B com 3 páginas, C com 10 páginas) sem configuração de páginas
- **THEN** o sistema gera um PDF final com 6 páginas: A-p1, A-p2, B-p1, B-p2, C-p1, C-p2

#### Scenario: Merge com configurações diferentes por arquivo
- **WHEN** o usuário configura A="1-3", B="1", C="2,4"
- **THEN** o sistema gera um PDF com 6 páginas na ordem: A-p1, A-p2, A-p3, B-p1, C-p2, C-p4

#### Scenario: Merge de apenas 1 arquivo
- **WHEN** o usuário faz upload de apenas 1 PDF e configura as páginas "1,3"
- **THEN** o sistema gera um PDF com 2 páginas (p1 e p3 do original)

### Requirement: Reordenação de arquivos
O sistema DEVE permitir que o usuário altere a ordem dos arquivos antes do merge. A ordem final define a sequência das páginas no PDF resultante.

#### Scenario: Reordenar arquivos
- **WHEN** o usuário faz upload de A, B, C e reordena para C, A, B
- **THEN** o merge gera: páginas de C primeiro, depois A, depois B

### Requirement: Download do PDF final
O sistema DEVE disponibilizar o PDF final para download imediato após o merge. O arquivo DEVE ter nome configurável com padrão "merged.pdf".

#### Scenario: Download com nome padrão
- **WHEN** o merge é concluído e o usuário não define nome
- **THEN** o sistema disponibiliza download com nome "merged.pdf"

#### Scenario: Download com nome customizado
- **WHEN** o usuário define o nome "contratos-jan-2026.pdf" antes do merge
- **THEN** o sistema disponibiliza download com o nome informado

### Requirement: Processamento efêmero
O sistema NÃO DEVE persistir os PDFs (originais ou resultado) em disco permanente. Todos os arquivos DEVEM ser descartados após o download ou após timeout de sessão.

#### Scenario: Limpeza após download
- **WHEN** o usuário faz download do PDF final
- **THEN** os dados em memória são liberados e não há rastro dos arquivos no servidor

#### Scenario: Timeout sem download
- **WHEN** o merge é concluído mas o usuário não faz download em 30 minutos
- **THEN** os dados em memória são liberados automaticamente
