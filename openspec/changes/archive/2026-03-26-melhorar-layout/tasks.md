## 1. Configuração shadcn

- [x] 1.1 Adicionar `components.json` no frontend com paths, estilo e aliases alinhados ao Vite/Tailwind existentes
- [x] 1.2 Validar que `npx shadcn@latest add` (ou equivalente) resolve `@/` e gera arquivos nos diretórios esperados

## 2. Shell e layout

- [x] 2.1 Criar componente de layout (por exemplo `AppLayout`) com `header`, `main` e `footer`, container `max-w-6xl` e espaçamento consistente
- [x] 2.2 Refatorar `App.tsx` para usar o layout, mantendo toda a lógica de estado e hooks inalterada

## 3. Padronização de UI

- [x] 3.1 Onde fizer sentido, substituir `div` decorativos por `Card`/`Separator`/`Label` shadcn (lista, upload, PDFs protegidos, estado vazio)
- [x] 3.2 Garantir que botões e inputs fora de `components/ui` passem a usá-lo quando não houver conflito com libs de terceiros

## 4. Verificação

- [x] 4.1 Rodar build do frontend e testes (Vitest) se existirem; checar layout em largura desktop e ~768px
