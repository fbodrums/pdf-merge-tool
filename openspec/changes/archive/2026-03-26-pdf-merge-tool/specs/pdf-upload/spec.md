## ADDED Requirements

### Requirement: Upload de múltiplos PDFs
O sistema DEVE aceitar upload de múltiplos arquivos PDF simultaneamente via API REST. Cada arquivo DEVE ser validado individualmente quanto ao tipo MIME (application/pdf), integridade (PDF legível) e tamanho máximo (50MB por arquivo).

#### Scenario: Upload bem-sucedido de múltiplos PDFs
- **WHEN** o usuário envia 3 arquivos PDF válidos via POST /api/upload
- **THEN** o sistema retorna status 200 com a lista dos 3 arquivos aceitos, incluindo nome original e total de páginas de cada um

#### Scenario: Upload com arquivo inválido no meio
- **WHEN** o usuário envia 3 arquivos, sendo o segundo um .txt renomeado para .pdf
- **THEN** o sistema retorna status 422 indicando que o arquivo 2 é inválido
- **AND** os arquivos válidos NÃO são processados (operação atômica)

#### Scenario: Upload de PDF acima do tamanho máximo
- **WHEN** o usuário envia um PDF de 60MB (acima do limite de 50MB)
- **THEN** o sistema retorna status 413 com mensagem "Arquivo excede o tamanho máximo de 50MB"

#### Scenario: Upload de PDF protegido por senha
- **WHEN** o usuário envia um PDF protegido por senha
- **THEN** o sistema retorna status 200 com flag `password_protected: true` no arquivo
- **AND** o total de páginas retorna como `null` até que a senha seja fornecida

### Requirement: Informações do PDF após upload
O sistema DEVE retornar metadados de cada PDF após o upload: nome do arquivo, total de páginas, tamanho em bytes e se é protegido por senha.

#### Scenario: Retorno de metadados após upload
- **WHEN** o upload é bem-sucedido
- **THEN** o sistema retorna para cada arquivo: `filename`, `total_pages`, `size_bytes`, `password_protected`

### Requirement: Desbloqueio de PDF protegido
O sistema DEVE permitir que o usuário forneça a senha de um PDF protegido via endpoint dedicado.

#### Scenario: Senha correta fornecida
- **WHEN** o usuário envia a senha correta para um PDF protegido via POST /api/unlock
- **THEN** o sistema desbloqueia o PDF e retorna os metadados completos (incluindo total de páginas)

#### Scenario: Senha incorreta fornecida
- **WHEN** o usuário envia uma senha incorreta
- **THEN** o sistema retorna status 401 com mensagem "Senha incorreta"
