# cli-interface

## Purpose

Interface de linha de comando (`pdftools merge`, globs, JSON, tolerante). Sincronizado a partir do change `pdf-merge-tool`.

## Requirements

### Requirement: Comando principal de merge
A CLI DEVE oferecer um comando principal que recebe lista de arquivos PDF e gera o PDF final. Sintaxe: `pdftools merge <arquivos> [opções]`

#### Scenario: Merge básico com configuração padrão
- **WHEN** o usuário executa `pdftools merge arquivo1.pdf arquivo2.pdf`
- **THEN** o sistema extrai as páginas 1 e 2 de cada arquivo e gera "output.pdf"

#### Scenario: Merge com páginas customizadas
- **WHEN** o usuário executa `pdftools merge arquivo1.pdf arquivo2.pdf --pages "1,3-5"`
- **THEN** o sistema extrai as páginas 1, 3, 4, 5 de cada arquivo e gera "output.pdf"

#### Scenario: Merge com nome de saída customizado
- **WHEN** o usuário executa `pdftools merge *.pdf --output resultado.pdf`
- **THEN** o sistema gera o arquivo "resultado.pdf"

### Requirement: Suporte a glob patterns
A CLI DEVE expandir glob patterns para seleção de múltiplos arquivos.

#### Scenario: Glob pattern
- **WHEN** o usuário executa `pdftools merge contratos/*.pdf`
- **THEN** o sistema processa todos os PDFs na pasta "contratos/" em ordem alfabética

#### Scenario: Nenhum arquivo encontrado
- **WHEN** o usuário executa `pdftools merge inexistente/*.pdf`
- **THEN** o sistema exibe erro "Nenhum arquivo PDF encontrado no caminho informado"

### Requirement: Opções de configuração
A CLI DEVE suportar as seguintes opções: `--pages` (configuração de páginas), `--output` (nome do arquivo de saída), `--verbose` (modo detalhado).

#### Scenario: Modo verbose
- **WHEN** o usuário executa `pdftools merge *.pdf --verbose`
- **THEN** o sistema exibe log detalhado: arquivos processados, páginas extraídas de cada um, tamanho do resultado

#### Scenario: Help
- **WHEN** o usuário executa `pdftools merge --help`
- **THEN** o sistema exibe help em português com descrição de todos os argumentos e opções

### Requirement: Feedback visual no terminal
A CLI DEVE exibir progresso colorido e mensagens de erro claras usando rich (via typer).

#### Scenario: Progresso durante processamento
- **WHEN** o merge está em andamento com 10 arquivos
- **THEN** o terminal exibe barra de progresso com porcentagem e nome do arquivo atual

#### Scenario: Erro de arquivo inválido
- **WHEN** um dos arquivos não é um PDF válido
- **THEN** o terminal exibe mensagem de erro em vermelho com o nome do arquivo inválido
- **AND** os demais arquivos são processados normalmente (modo tolerante)

### Requirement: Configuração por arquivo via JSON
A CLI DEVE aceitar opcionalmente um arquivo JSON de configuração para definir páginas por arquivo individualmente.

#### Scenario: Configuração via JSON
- **WHEN** o usuário executa `pdftools merge --config config.json` com JSON contendo `{"arquivo1.pdf": "1-3", "arquivo2.pdf": "1"}`
- **THEN** o sistema aplica a configuração individual de cada arquivo

#### Scenario: JSON inválido
- **WHEN** o arquivo JSON tem sintaxe inválida
- **THEN** o sistema exibe erro "Arquivo de configuração inválido: erro de sintaxe na linha X"
