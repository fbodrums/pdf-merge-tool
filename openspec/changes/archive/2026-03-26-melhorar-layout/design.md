## Context

O frontend já usa alguns padrões do shadcn/ui (`Button`, `Input`, `Card`, `cn()` em `lib/utils.ts`) e variáveis CSS de tema em `index.css`. Porém não há `components.json` no repositório, o `App.tsx` concentra todo o shell (header, main, footer) em um único arquivo com classes ad hoc, e blocos como o aviso de PDFs protegidos misturam `Card` com containers `div` estilizados manualmente. A change visa alinhar isso a um layout e a uma convenção de projeto shadcn mais explícitos e reproduzíveis.

## Goals / Non-Goals

**Goals:**

- Tornar o shell da aplicação (cabeçalho, área principal, rodapé) uma composição clara e reutilizável baseada em componentes shadcn e tokens de tema.
- Introduzir ou completar a configuração oficial do shadcn (`components.json`) compatível com Vite, aliases `@/` e Tailwind 4.
- Reduzir estilos soltos em favor de componentes da pasta `components/ui` (e novos adicionados via CLI, quando úteis: por exemplo `Separator`, `Label`, `Alert`).
- Manter acessibilidade e textos em português; preservar o comportamento atual de upload, lista, merge e toasts.

**Non-Goals:**

- Alterar contratos REST, hooks de dados ou lógica de merge.
- Trocar `sonner` por outro sistema de toast (a menos que surja necessidade pontual de integração com o pacote de toast do shadcn — pode ficar como decisão futura).
- Redesign completo de marca (novo logo, ilustrações) ou suporte a temas além de claro/escuro já previstos nas variáveis.

## Decisions

1. **Configuração `components.json`**
   - **Decisão**: Adicionar `components.json` na raiz do `frontend/` (ou na raiz do monorepo, se o time padronizar assim) com `style`, `tailwind`, `aliases` e `iconLibrary` alinhados ao projeto.
   - **Rationale**: Documenta o projeto como “projeto shadcn” e permite `npx shadcn@latest add <component>` sem adivinhar paths.
   - **Alternativa considerada**: Manter só cópia manual de componentes — rejeitada pela falta de rastreabilidade e drift entre devs.

2. **Componente de layout (App shell)**
   - **Decisão**: Extrair um componente `AppLayout` (ou `MainLayout`) em `src/components/layout/` que recebe `children` e opcionalmente título/descrição do header, aplicando `min-h-screen`, regiões semânticas e espaçamento consistente (`max-w-6xl`, `px-4`, gaps).
   - **Rationale**: Separa estrutura visual de fluxo de negócio em `App.tsx`, facilita testes e evolução do shell.
   - **Alternativa considerada**: Deixar tudo em `App.tsx` — rejeitada pela manutenção difícil.

3. **Substituição gradual de `div` estilizados**
   - **Decisão**: Onde houver cartões ou agrupamentos, preferir `Card` + `CardHeader`/`CardContent`; usar `Separator` entre seções quando fizer sentido; campos com rótulo explícito usando `Label` do shadcn.
   - **Rationale**: Aparência e foco/teclado mais previsíveis (Radix por baixo).
   - **Alternativa**: Tailwind puro — já usado em parte; manter só onde o shadcn não trouxer ganho.

4. **Tema**
   - **Decisão**: Continuar com variáveis em `:root` / `.dark` em `index.css`; garantir que novos componentes shadcn usem as mesmas variáveis (`background`, `foreground`, `card`, `border`, etc.).
   - **Rationale**: Evita migração grande para outro sistema de tema nesta change.

## Risks / Trade-offs

- **[Risco]** Versão do CLI shadcn vs Tailwind 4 — alguns snippets podem precisar de ajuste manual após `add`.
  - **Mitigação**: Seguir documentação atual do shadcn para Vite; após adicionar componente, rodar build e corrigir imports.
- **[Risco]** Diff visual pequeno mas perceptível (espaçamentos).
  - **Mitigação**: Revisar manualmente em desktop e largura ~768px; não mudar fluxos.

## Migration Plan

1. Merge da branch após revisão; deploy apenas do frontend (build estático).
2. **Rollback**: Reverter o commit ou redeploy do artefato anterior; sem migração de dados.

## Open Questions

- Se o time quiser `ThemeProvider` explícito (next-themes) para alternância claro/escuro na UI — fora do escopo mínimo desta change, pode vir depois.
