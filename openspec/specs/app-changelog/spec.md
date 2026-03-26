# app-changelog

## Purpose

Exibir o changelog oficial do produto na interface web, com acesso a partir do shell, alinhado ao arquivo `CHANGELOG.md` versionado na raiz do repositório. Sincronizado a partir do change `changelog-follow-app`.

## Requirements

### Requirement: Conteúdo do changelog na interface

O sistema DEVE exibir na interface web o texto do changelog oficial do produto, de forma que o usuário possa ler novidades e alterações documentadas sem depender de ferramentas externas ao aplicativo.

#### Scenario: Abertura a partir do cabeçalho

- **WHEN** o usuário aciona o controle de acesso ao changelog disponível no shell
- **THEN** o conteúdo do changelog é apresentado numa superfície de leitura (por exemplo painel lateral ou diálogo) com área rolável quando o texto for longo

#### Scenario: Estrutura legível

- **WHEN** o changelog é exibido
- **THEN** títulos e listas do markdown são renderizados de forma hierárquica e legível, usando o tema visual da aplicação (tipografia e cores coerentes com o restante da UI)

### Requirement: Consistência com a fonte versionada

O conteúdo apresentado DEVE corresponder ao arquivo de changelog versionado no repositório (`CHANGELOG.md` na raiz), sem exigir manutenção duplicada de texto em outro formato na aplicação, salvo mecanismos automáticos de build (import estático, cópia em build ou asset gerado).

#### Scenario: Atualização via release

- **WHEN** a equipe atualiza `CHANGELOG.md` para uma nova versão
- **THEN** o build do frontend incorpora esse conteúdo de forma que a interface mostre a versão atualizada após o deploy
