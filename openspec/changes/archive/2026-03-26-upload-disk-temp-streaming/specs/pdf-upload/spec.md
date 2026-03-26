## ADDED Requirements

### Requirement: Persistência de upload em arquivo temporário

O sistema DEVE persistir o conteúdo de cada PDF aceito em um arquivo no sistema de arquivos sob um diretório dedicado da aplicação (por exemplo subdiretório do diretório temporário do SO). O estado interno do arquivo carregado NÃO DEVE depender exclusivamente de um único objeto `bytes` em memória como representação primária entre o fim do upload e o processamento subsequente.

#### Scenario: Arquivo em disco após upload válido

- **WHEN** o upload de um PDF passa na validação e é associado à sessão
- **THEN** a representação guardada inclui um caminho para um arquivo legível em disco contendo os bytes do PDF

### Requirement: Cópia em streaming a partir do UploadFile

O sistema DEVE copiar cada `UploadFile` recebido para o ficheiro temporário usando cópia por chunks (por exemplo `shutil.copyfileobj`), sem carregar o upload inteiro de uma só vez na rota como um único `bytes` intermédio.

#### Scenario: Upload até ao limite configurado

- **WHEN** o cliente envia um PDF cujo tamanho está dentro do limite máximo permitido
- **THEN** a operação de cópia do stream de upload para disco não exige manter o ficheiro completo em memória como um único buffer na rota de upload

### Requirement: Limpeza de arquivos temporários

O sistema DEVE remover do disco os arquivos temporários associados a uma sessão quando a sessão expira ou deixa de ser retida, de forma análoga à liberação de memória quando os dados viviam só em RAM.

#### Scenario: Expiração de sessão

- **WHEN** uma sessão é expulsa por TTL ou deixa de existir no armazenamento de sessões
- **THEN** os arquivos temporários dessa sessão são apagados do disco (ou o sistema tenta apagá-los de forma segura)
