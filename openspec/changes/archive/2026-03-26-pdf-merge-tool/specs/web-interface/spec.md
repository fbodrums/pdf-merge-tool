## ADDED Requirements

### Requirement: Upload drag & drop
A interface web DEVE permitir upload de PDFs via drag & drop e via clique para seleção de arquivos. DEVE aceitar múltiplos arquivos simultaneamente.

#### Scenario: Upload via drag & drop
- **WHEN** o usuário arrasta 3 PDFs para a área de upload
- **THEN** os 3 arquivos são enviados ao backend e exibidos na lista com nome e total de páginas

#### Scenario: Upload via clique
- **WHEN** o usuário clica na área de upload e seleciona arquivos no file picker
- **THEN** os arquivos selecionados são enviados e exibidos na lista

#### Scenario: Upload de arquivo não-PDF
- **WHEN** o usuário tenta fazer upload de um arquivo .docx
- **THEN** a interface exibe mensagem "Apenas arquivos PDF são aceitos" e rejeita o arquivo

### Requirement: Lista de arquivos com configuração
A interface DEVE exibir a lista de PDFs uploaded com: nome do arquivo, total de páginas, campo de configuração de páginas e botão para remover.

#### Scenario: Exibição da lista após upload
- **WHEN** 3 PDFs são carregados com sucesso
- **THEN** a interface exibe uma lista com 3 itens, cada um mostrando nome, total de páginas, e campo de páginas preenchido com "1,2" (padrão)

#### Scenario: Editar configuração de páginas
- **WHEN** o usuário altera o campo de páginas do arquivo B de "1,2" para "1-5"
- **THEN** a configuração é atualizada e validada em tempo real (feedback se inválida)

#### Scenario: Remover arquivo da lista
- **WHEN** o usuário clica no botão remover do arquivo B
- **THEN** o arquivo B é removido da lista e não será incluído no merge

### Requirement: Reordenação visual de arquivos
A interface DEVE permitir reordenação dos arquivos via drag & drop na lista.

#### Scenario: Arrastar arquivo para nova posição
- **WHEN** o usuário arrasta o arquivo C da posição 3 para a posição 1
- **THEN** a lista é reordenada: C, A, B e o merge respeitará esta nova ordem

### Requirement: Botão de gerar PDF
A interface DEVE ter um botão "Gerar PDF" que inicia o merge e apresenta o resultado para download.

#### Scenario: Gerar PDF com sucesso
- **WHEN** o usuário clica em "Gerar PDF" com 3 arquivos configurados
- **THEN** a interface mostra indicador de progresso durante o processamento
- **AND** após conclusão, exibe botão "Baixar PDF" com o nome do arquivo resultante

#### Scenario: Gerar PDF sem arquivos
- **WHEN** o usuário clica em "Gerar PDF" sem ter feito upload de nenhum arquivo
- **THEN** o botão está desabilitado ou exibe mensagem "Adicione ao menos 1 PDF"

#### Scenario: Erro durante processamento
- **WHEN** ocorre erro no backend durante o merge
- **THEN** a interface exibe mensagem de erro clara e permite o usuário tentar novamente

### Requirement: Configuração do nome do arquivo de saída
A interface DEVE permitir que o usuário defina o nome do PDF final antes de gerar.

#### Scenario: Nome padrão
- **WHEN** o usuário não altera o campo de nome
- **THEN** o arquivo é gerado com nome "merged.pdf"

#### Scenario: Nome customizado
- **WHEN** o usuário digita "relatorio-marco-2026" no campo de nome
- **THEN** o arquivo é gerado como "relatorio-marco-2026.pdf" (extensão adicionada automaticamente se ausente)

### Requirement: Interface responsiva
A interface DEVE ser utilizável em desktop e tablet. Layout responsivo com Tailwind CSS.

#### Scenario: Uso em tela de desktop (1920px)
- **WHEN** o usuário acessa em tela larga
- **THEN** a interface usa layout amplo com área de upload e lista lado a lado

#### Scenario: Uso em tablet (768px)
- **WHEN** o usuário acessa em tablet
- **THEN** a interface empilha os componentes verticalmente mantendo usabilidade
