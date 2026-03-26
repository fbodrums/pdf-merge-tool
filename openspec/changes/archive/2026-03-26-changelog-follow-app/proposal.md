## Why

Usuários e equipe interna precisam acompanhar novidades e correções documentadas no `CHANGELOG.md` sem sair do contexto da ferramenta nem abrir o repositório. Outras aplicações Spot (por exemplo Frotas) expõem um acesso explícito a esse tipo de informação no shell; esta ferramenta ainda não oferece esse atalho.

## What Changes

- Incluir no **cabeçalho** da interface um controle visível (botão ou link estilizado como botão secundário) para **abrir o changelog** do produto.
- Exibir o conteúdo do changelog **na própria aplicação** (painel sobreposto ou página dedicada), com leitura confortável em desktop e tablet, alinhado ao padrão visual shadcn/ui já usado no projeto.
- A fonte de verdade do texto continua sendo o arquivo de changelog do repositório (evitar divergência manual entre “changelog da web” e o arquivo versionado).

## Capabilities

### New Capabilities

- `app-changelog`: leitura do changelog do produto dentro da interface (conteúdo derivado do markdown oficial), com apresentação estruturada e acessível.

### Modified Capabilities

- `web-interface`: acrescentar requisito de **ponto de entrada no shell** (cabeçalho) para o changelog, coerente com o layout existente e com controles padronizados (shadcn).

## Impact

- **Frontend**: `AppLayout` (ou equivalente), possivelmente novo componente de painel/diálogo, dependência opcional para renderização de Markdown, import ou cópia do texto do changelog no build.
- **Backend**: nenhuma alteração obrigatória se o conteúdo for empacotado no frontend ou servido como asset estático.
- **Documentação**: manter `CHANGELOG.md` na raiz como fonte; processo de release continua atualizando esse arquivo.
