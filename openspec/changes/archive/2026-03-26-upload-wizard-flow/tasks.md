## 1. Estado e navegação do assistente

- [x] 1.1 Introduzir estado de etapa (wizard) e enum ou constantes dos passos (seleção → envio → configuração → resultado) no `App` ou hook dedicado, preservando `sessionId`, `rows` e `pendingFiles` conforme o design.
- [x] 1.2 Implementar indicador visual do passo atual (passos numerados ou componente de steps do shadcn, se disponível) alinhado à spec de `web-interface`.

## 2. Etapa de seleção e disparo do upload

- [x] 2.1 Ajustar o fluxo para que o upload **não** seja disparado no `onDrop`/seleção imediata; apenas acumular arquivos em `pendingFiles` até **Próximo** na etapa de seleção.
- [x] 2.2 Na etapa de envio, chamar `uploadFiles` com os pendentes e, em sucesso, preencher `sessionId`/`rows` e avançar para a etapa de configuração (ou conforme decisão de avanço automático no `design.md`).

## 3. Barra de progresso no upload

- [x] 3.1 Estender `useUpload` (ou camada equivalente) para reportar progresso de envio (por exemplo via `XMLHttpRequest`/`upload.onprogress`) e expor estado numérico `0–100` ou indeterminado.
- [x] 3.2 Na UI da etapa de envio, exibir `Progress` (shadcn) ou spinner indeterminado quando não houver medição, conforme spec.

## 4. Etapas de configuração e resultado

- [x] 4.1 Renderizar lista de arquivos, campos de páginas, desbloqueio por senha, reordenação e nome de saída **somente** na etapa de configuração, reutilizando `FileList`, `OutputConfig` e lógica existente.
- [x] 4.2 Substituir o fluxo “Gerar PDF na mesma tela” por avanço para etapa de resultado: ao confirmar, executar `merge` e mostrar loading; em sucesso, exibir botão de download na etapa de resultado.
- [x] 4.3 Implementar **Voltar** da etapa de resultado para a de configuração sem novo upload quando `session_id` ainda for válido.

## 5. UX, responsividade e regressão

- [x] 5.1 Garantir navegação acessível (rótulos, foco, botões desabilitados quando inválido) e mensagens de erro nas etapas corretas.
- [x] 5.2 Verificar layout em desktop e tablet (wizard e áreas principais não colapsam de forma ilegível).
- [x] 5.3 Testar regressão: PDF inválido, senha, merge com erro, lista vazia.
