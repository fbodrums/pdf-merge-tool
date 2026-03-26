## 1. Estado e handler de reinício

- [x] 1.1 Em `frontend/src/App.tsx`, criar `handleRestartProcess` (ou nome alinhado ao código) que define `wizardStep` para a etapa inicial de seleção, zera `sessionId`, `rows`, `pendingFiles`, `unlockPwd`, restaura `outputName` e `resultFilename` aos padrões da aplicação e revoga `resultBlobUrl` antes de atribuir `null`.
- [x] 1.2 Em `useUpload` / `useMerge`, expor cancelamento (`abort` do XHR e `AbortController` no `fetch`) e invocar a partir do reinício; tratar `AbortError` nos `catch` de upload/merge para não exibir toast de erro.

## 2. Interface

- [x] 2.1 Expor um único botão "Reiniciar processo" visível em todas as etapas (por exemplo abaixo do stepper), sem depender de `busy` para habilitar.

## 3. Verificação

- [x] 3.1 Verificar manualmente: reinício na seleção (limpa fila), durante upload e durante merge; ausência de toast de erro após cancelamento; blob revogado no resultado.
  - **Checklist QA (ambiente local):** (1) Com PDFs na fila no passo 1, clicar *Reiniciar processo* → fila vazia e passo 1. (2) Durante envio, reiniciar → volta ao passo 1 sem toast de erro de falha. (3) Durante *Gerar PDF*, reiniciar → mesmo comportamento. (4) Após gerar, reiniciar → passo 1 e sem link de download ativo (blob revogado).
- [x] 3.2 Se o projeto já tiver testes RTL/Vitest para `App`, adicionar caso que cobre o reset de estado; caso contrário, documentar verificação manual no PR ou pular com justificativa breve.
  - **Justificativa:** o `frontend` não inclui Vitest nem Testing Library; a verificação fica pelo checklist 3.1 até haver infraestrutura de teste.

## 4. Changelog

- [x] 4.1 Atualizar `CHANGELOG.md` (linguagem amigável ao usuário final) com a nova opção de reiniciar o processo.
