## Context

A aplicação web hoje concentra seleção de arquivos locais, disparo de upload, lista com páginas/reordenação, nome de saída e merge na mesma visão (`App.tsx` + componentes existentes). O backend expõe `/api/upload`, `/api/unlock`, `/api/merge` (via hooks) sem necessidade de mudança de contrato para este fluxo.

## Goals / Non-Goals

**Goals:**

- Introduzir um **wizard** com etapas explícitas e indicador de progresso (passos), alinhado ao fluxo mental: escolher arquivos → enviar com feedback → configurar páginas e ordem → obter o PDF.
- Na etapa de envio, exibir **barra de progresso** durante o upload (reutilizando ou estendendo `useUpload` / `XMLHttpRequest` / `fetch` com progresso, conforme já suportado ou a implementar).
- Na etapa final, dedicar a tela ao **download** (e estados de carregamento/erro do merge), em vez de misturar com a lista.

**Non-Goals:**

- Alterar regras de validação de PDF, limites de tamanho ou contratos REST do backend.
- Internacionalização ou novo design system além do shadcn/Tailwind já usados.

## Decisions

1. **Estado do wizard no cliente** — Manter um único estado de etapa atual (`0..n-1`) e dados compartilhados (`pendingFiles`, `sessionId`, `rows`, etc.) no componente raiz da ferramenta ou em um hook dedicado (`useWizard` opcional), evitando duplicar chamadas à API.

2. **Quando disparar o upload** — O upload só ocorre ao avançar da etapa de seleção (botão **Próximo**), não no `onDrop` imediato, para coincidir com a expectativa “escolheu → próximo → barra”.

3. **Progresso de upload** — Preferir expor progresso no hook de upload (ex.: callback `onProgress` ou estado `uploadProgress`) e ligar a um componente `Progress` (shadcn). Se o backend for multipart e o cliente usar `fetch` sem progresso nativo, usar `XMLHttpRequest` ou biblioteca compatível apenas neste fluxo.

4. **Transição após upload** — Ao concluir o upload com sucesso, avançar automaticamente para a etapa de configuração **ou** exibir botão “Continuar”; a spec delimita que a lista de arquivos e páginas fica **após** o upload (decisão de produto: avanço automático reduz cliques).

5. **Merge e etapa de download** — Na etapa de configuração, **Próximo** dispara o merge (equivalente ao “Gerar PDF” atual) e navega para a etapa de resultado; essa etapa mostra progresso do merge e, ao concluir, o botão de download (comportamento análogo ao atual, porém isolado visualmente).

6. **Alternativas consideradas** — Wizard com rotas (`/step/1`) foi descartado para manter SPA simples e estado já existente; pode ser evolução futura.

## Risks / Trade-offs

- **Mais cliques** para usuários experientes → Mitigação: manter ações claras e opcionalmente atalhos no futuro.
- **Progresso de upload** depende de capacidade do cliente de medir bytes enviados → Mitigação: documentar fallback (indeterminado) se não for possível medir.
- **PDFs protegidos** ainda exigem desbloqueio na etapa de configuração → Mitigação: manter UI de senha na mesma etapa que a lista.

## Migration Plan

- Deploy apenas do frontend; usuários veem o novo fluxo sem migração de dados.
- Rollback: reverter commit do `App`/componentes do wizard.

## Open Questions

- Avanço automático após upload bem-sucedido vs. botão “Continuar” (produto pode ajustar após testes).
- Se o merge deve permitir “Voltar” da etapa de download para alterar páginas sem novo upload (recomendado: sim, voltando à etapa 3 com mesma `session_id`).
