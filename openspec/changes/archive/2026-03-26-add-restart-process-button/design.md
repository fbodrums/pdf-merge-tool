## Context

O fluxo principal vive em `frontend/src/App.tsx`: estado local (`wizardStep`, `sessionId`, `rows`, `pendingFiles`, `outputName`, `unlockPwd`, `resultBlobUrl`). Já existe `handleBackToConfigure`, que apenas volta da etapa de resultado para `configure` e revoga o blob; não há ação que zere a sessão e retorne à etapa 1.

## Goals / Non-Goals

**Goals:**

- Expor uma ação **Reiniciar processo** (ou rótulo equivalente em português) que retorne o assistente ao estado inicial e limpe todos os dados da execução atual.
- Revogar `URL.createObjectURL` do PDF gerado antes de descartar a referência, alinhado ao padrão já usado no componente.
- Permitir o reinício **a qualquer momento**: cancelar upload (XHR `abort`) e merge (`AbortController` + `fetch`) antes de limpar o estado, para que promessas concluídas depois não reescrevam a UI.

**Non-Goals:**

- Invalidar sessão no backend (limpeza server-side, TTL ou endpoint dedicado).
- Diálogo de confirmação obrigatório na primeira versão (pode ser iterado depois se houver feedback de usuários).

## Decisions

1. **Estado resetado em um único handler (`handleRestartProcess`)**  
   Centraliza `setWizardStep('select')`, limpeza de `sessionId`, `rows`, `pendingFiles`, `unlockPwd`, `outputName` para o padrão (`merged.pdf`), `resultFilename`, revogação de `resultBlobUrl`. Evita esquecer um campo ao duplicar lógica em vários botões.

2. **Onde exibir o botão**  
   - Uma única ação global (por exemplo logo abaixo do `WizardStepper`), visível em **todas** as etapas, para satisfazer “reiniciar a qualquer momento” sem duplicar lógica em cada card.

3. **Sem confirmação modal na v1**  
   Reduz escopo; o rótulo “Reiniciar processo” já comunica efeito destrutivo. Documentar como melhoria futura se necessário.

4. **Testes**  
   Preferir teste de integração leve (RTL) que monta `App`, avança estado com mocks de hooks se já existir padrão no projeto; caso contrário, tarefa manual + vitest unitário do handler se extraído.

## Risks / Trade-offs

- **[Risco]** Usuário clica em reiniciar por engano e perde a sessão. **Mitigação:** copy clara; evolução futura com `AlertDialog` de confirmação.
- **[Trade-off]** Sessões órfãs no servidor até expirarem. **Mitigação:** aceito no escopo; backend já trata armazenamento temporário.

## Migration Plan

Deploy apenas do frontend; sem migração de dados ou flags.

## Open Questions

- Nenhuma bloqueante para a v1.
