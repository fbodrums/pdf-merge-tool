## 1. Dependências e conteúdo

- [x] 1.1 Adicionar `react-markdown` (e `remark-gfm` se necessário para listas/tabelas) ao `package.json` do frontend
- [x] 1.2 Garantir que o texto do `CHANGELOG.md` da raiz entra no bundle (import `?raw` com caminho permitido pelo Vite ou cópia/asset em `public/` com fallback documentado no código)

## 2. UI do shell

- [x] 2.1 Estender `AppLayout` (ou wrapper usado por `App`) com slot ou props para ações na área de cabeçalho à direita do título
- [x] 2.2 Incluir botão/link secundário com rótulo claro (ex.: “Changelog” ou “Novidades”) usando componentes shadcn/ui

## 3. Superfície de leitura

- [x] 3.1 Implementar componente que abre Sheet ou Dialog com o markdown renderizado e rolagem interna
- [x] 3.2 Aplicar classes de tema/prose (ou equivalente Tailwind) para hierarquia tipográfica legível

## 4. Qualidade

- [x] 4.1 Verificar teclado (Escape fecha o painel) e foco acessível conforme o primitivo Radix escolhido
- [x] 4.2 Rodar `npm run build` e `npm run lint` no frontend e corrigir regressões
