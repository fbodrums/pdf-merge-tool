## Context

A interface usa Vite, React 19, Tailwind 4 e shadcn/ui. O shell está em `AppLayout` com `header`, `main` e `footer`. Não há roteador de múltiplas páginas no frontend atual; o fluxo principal é uma única tela. O changelog oficial está em `CHANGELOG.md` na raiz do repositório.

## Goals / Non-Goals

**Goals:**

- Botão ou link de ação secundária no cabeçalho (“Changelog”, “Novidades” ou label equivalente) que abre uma superfície de leitura (recomendado: **Sheet** ou **Dialog** do Radix/shadcn) com o conteúdo completo do changelog.
- Conteúdo alinhado ao markdown do repositório, com hierarquia de títulos e listas legíveis.
- Acessibilidade: foco preso no painel, fechamento por teclado (Escape) e rótulo compreensível no botão.

**Non-Goals:**

- Histórico versionado por release dentro da UI, comparação entre versões ou edição do changelog na web.
- API dedicada no backend só para o changelog (a menos que o build static falhe por política de caminho; nesse caso, avaliar asset em `public/`).

## Decisions

1. **Fonte do texto**  
   **Decisão**: importar o markdown da raiz com sufixo Vite `?raw` a partir de um módulo em `frontend/src` (caminho relativo até `CHANGELOG.md`), garantindo um único arquivo editado em releases.  
   **Alternativa**: copiar `CHANGELOG.md` para `frontend/public/changelog.md` e `fetch` em tempo de execução — útil se o import da raiz for rejeitado pela config do bundler; implica script ou disciplina de cópia no build.

2. **Renderização Markdown**  
   **Decisão**: adicionar `react-markdown` (e, se necessário, `remark-gfm` para tabelas/listas) para renderizar o texto com segurança, sem `dangerouslySetInnerHTML` com parser ad hoc.  
   **Alternativa**: exibir texto pré-formatado em `<pre>` — mínima dependência, porém pior UX.

3. **Posicionamento no shell**  
   **Decisão**: área à direita do bloco de título no `header`, em linha com o padrão “ferramenta Spot” (título à esquerda, ações secundárias à direita), responsivo (empilhar ou manter compacto em telas estreitas).  
   **Alternativa**: link apenas no rodapé — menos visível que o pedido “parecido com Frotas”.

4. **Componente de superfície**  
   **Decisão**: **Sheet** (painel lateral) se o changelog for longo — rolagem natural e leitura tipo documento. **Dialog** centralizado se o time preferir modal; a spec pode aceitar qualquer um desde que o requisito de leitura confortável seja atendido.

## Risks / Trade-offs

- [Import do arquivo fora de `frontend/`] → Mitigação: ajustar `vite.config` `server.fs.allow` ou mover uma cópia para `frontend/src/content/changelog.md` gerada no build.
- [Tamanho do bundle com react-markdown] → Mitigação: dependência pequena frente ao benefício; chunk lazy do componente do painel se necessário.
- [Drift entre branches] → Mitigação: uma única fonte `CHANGELOG.md`; CI pode validar que o import resolve.

## Migration Plan

1. Implementar UI e dependências no frontend.
2. Verificar build de produção (`npm run build`) e preview.
3. Atualizar `CHANGELOG.md` na próxima release mencionando o novo acesso (opcional, pode constar em `CHANGELOG_DEV.md` se aplicável).

## Open Questions

- Label exato do botão (“Changelog” vs “Novidades”) — alinhar à nomenclatura das outras ferramentas Spot no mesmo ecossistema.
