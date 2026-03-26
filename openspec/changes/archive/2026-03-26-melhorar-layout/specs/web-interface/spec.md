# web-interface (delta)

## ADDED Requirements

### Requirement: Shell da aplicação com shadcn/ui

A interface DEVE organizar a página em regiões claras (cabeçalho, conteúdo principal, rodapé) usando HTML semântico (`header`, `main`, `footer` ou equivalente acessível) e componentes do conjunto shadcn/ui (por exemplo `Card` e utilitários de layout) de forma que o espaçamento, bordas e tipografia sigam os tokens de tema definidos nas variáveis CSS do projeto.

#### Scenario: Estrutura visual consistente

- **WHEN** o usuário carrega qualquer tela principal da ferramenta
- **THEN** o cabeçalho, o conteúdo e o rodapé são distinguíveis visualmente e alinhados a um container de largura máxima coerente entre breakpoints

### Requirement: Configuração explícita do projeto shadcn

O repositório do frontend DEVE incluir arquivo `components.json` (configuração do shadcn/ui) coerente com o bundler (Vite), aliases de importação (por exemplo `@/`) e estilos Tailwind usados pelo projeto, permitindo adicionar novos componentes via CLI oficial sem divergência de caminhos.

#### Scenario: Adicionar componente via CLI

- **WHEN** um desenvolvedor executa o comando de adição de componente shadcn apontando para o diretório do frontend
- **THEN** o componente é gerado nos caminhos esperados (`components/ui`, `lib`, etc.) e compila sem ajuste manual de alias

### Requirement: Controles interativos padronizados

Elementos interativos da interface principal (botões, campos de texto em blocos de configuração, cartões de seção) DEVEM usar os componentes em `components/ui` derivados do shadcn (por exemplo `Button`, `Input`, `Card`) em vez de elementos HTML brutos com estilos únicos, salvo exceções justificadas (por exemplo integração com biblioteca de terceiros).

#### Scenario: Ação primária na área de upload

- **WHEN** o usuário vê o fluxo de envio de PDFs
- **THEN** o botão de envio e os campos de formulário associados usam os componentes padronizados e as classes de tema compartilhadas

## MODIFIED Requirements

### Requirement: Interface responsiva

A interface DEVE ser utilizável em desktop e tablet. O layout responsivo DEVE usar Tailwind CSS em conjunto com tokens de tema (variáveis CSS) e componentes shadcn/ui para manter consistência visual entre breakpoints.

#### Scenario: Uso em tela de desktop (1920px)

- **WHEN** o usuário acessa em tela larga
- **THEN** a interface usa layout amplo com área de upload e lista lado a lado

#### Scenario: Uso em tablet (768px)

- **WHEN** o usuário acessa em tablet
- **THEN** a interface empilha os componentes verticalmente mantendo usabilidade
