# pdf-upload

## Purpose

Upload e validação de múltiplos PDFs na API, incluindo metadados e desbloqueio por senha. Sincronizado a partir do change `pdf-merge-tool`.

## Requirements

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

### Requirement: Persistência de upload em arquivo temporário

O sistema DEVE persistir o conteúdo de cada PDF aceito em um arquivo no sistema de arquivos sob um diretório dedicado da aplicação (por exemplo subdiretório do diretório temporário do SO). O estado interno do arquivo carregado NÃO DEVE depender exclusivamente de um único objeto `bytes` em memória como representação primária entre o fim do upload e o processamento subsequente.

#### Scenario: Arquivo em disco após upload válido

- **WHEN** o upload de um PDF passa na validação e é associado à sessão
- **THEN** a representação guardada inclui um caminho para um arquivo legível em disco contendo os bytes do PDF

### Requirement: Cópia em streaming a partir do UploadFile

O sistema DEVE copiar cada `UploadFile` recebido para o arquivo temporário usando cópia por chunks (por exemplo `shutil.copyfileobj`), sem carregar o upload inteiro de uma só vez na rota como um único `bytes` intermédio.

#### Scenario: Upload até ao limite configurado

- **WHEN** o cliente envia um PDF cujo tamanho está dentro do limite máximo permitido
- **THEN** a operação de cópia do stream de upload para disco não exige manter o arquivo completo em memória como um único buffer na rota de upload

### Requirement: Limpeza de arquivos temporários

O sistema DEVE remover do disco os arquivos temporários associados a uma sessão quando a sessão expira ou deixa de ser retida, de forma análoga à liberação de memória quando os dados viviam só em RAM.

#### Scenario: Expiração de sessão

- **WHEN** uma sessão é expulsa por TTL ou deixa de existir no armazenamento de sessões
- **THEN** os arquivos temporários dessa sessão são apagados do disco (ou o sistema tenta apagá-los de forma segura)

### Requirement: Desbloqueio de PDF protegido
O sistema DEVE permitir que o usuário forneça a senha de um PDF protegido via endpoint dedicado.

#### Scenario: Senha correta fornecida
- **WHEN** o usuário envia a senha correta para um PDF protegido via POST /api/unlock
- **THEN** o sistema desbloqueia o PDF e retorna os metadados completos (incluindo total de páginas)

#### Scenario: Senha incorreta fornecida
- **WHEN** o usuário envia uma senha incorreta
- **THEN** o sistema retorna status 401 com mensagem "Senha incorreta"
