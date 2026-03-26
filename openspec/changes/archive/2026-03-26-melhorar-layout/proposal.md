## Why

A interface web já funciona, mas o layout mistura estilos ad hoc e não aproveita de forma consistente o ecossistema shadcn/ui previsto no projeto. Isso dificulta manutenção, acessibilidade e aparência uniforme. Padronizar o shell da aplicação com shadcn melhora consistência visual, reutilização de componentes e alinhamento com as convenções do frontend.

## What Changes

- Garantir configuração explícita do shadcn/ui no frontend (`components.json`, aliases, tema) quando ainda ausente ou incompleta.
- Refatorar o layout raiz (App shell): container, espaçamento, tipografia e hierarquia visual usando componentes shadcn (por exemplo Card, Button, Input, Separator, etc., conforme necessário).
- Substituir marcação e classes soltas por composição com componentes da biblioteca e tokens de tema (CSS variables / Tailwind alinhados ao shadcn).
- Manter textos e fluxos em português; **sem** alterar contratos da API ou regras de negócio do merge de PDF.

## Capabilities

### New Capabilities

_(Nenhuma capability nova — o escopo é padronização de UI sobre a capability existente.)_

### Modified Capabilities

- `web-interface`: Incluir requisitos de layout e shell baseados em shadcn/ui (estrutura da página, componentes padronizados, responsividade mantida com o design system).

## Impact

- **Frontend**: `frontend/` — `App.tsx`, layouts, componentes de página, possivelmente `index.css` / tema; adição ou ajuste de dependências shadcn (Radix + `class-variance-authority`, etc.) e arquivos gerados pelo CLI shadcn.
- **Backend / API**: nenhuma alteração esperada.
- **Testes**: possíveis ajustes em testes de componente ou snapshot do Vitest se existirem para a UI.
