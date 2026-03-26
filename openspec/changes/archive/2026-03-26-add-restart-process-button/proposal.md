## Why

Depois de concluir o merge ou durante a configuração, o usuário pode querer começar do zero (nova seleção de arquivos) sem recarregar a página. Hoje só existe “Voltar para edição” na etapa de resultado, que mantém a sessão e não limpa o fluxo completo.

## What Changes

- Incluir um controle explícito na interface para **reiniciar o processo**: voltar à etapa inicial, limpar estado local da sessão (incluindo `session_id`, lista de arquivos, senhas, nome de saída e blob de resultado) e revogar URLs de objeto quando aplicável.
- O botão deve estar acessível **a qualquer momento** no fluxo (incluindo durante envio ou geração), com cancelamento das requisições em andamento no cliente quando necessário; rótulo e feedback claros em português.

## Capabilities

### New Capabilities

- _(nenhuma capability nova em arquivo separado; o comportamento é extensão do assistente já descrito em `web-interface`.)_

### Modified Capabilities

- `web-interface`: acrescentar requisito de **reinício do fluxo** (ação dedicada, efeitos no estado e cenários de teste).

## Impact

- **Frontend**: `frontend/src/App.tsx` (estado do wizard e handler de reset); possivelmente componentes de layout/cabeçalho ou cartões de etapa para expor o botão.
- **Backend**: nenhuma alteração obrigatória se o reset for apenas cliente (abandonar `session_id`; opcional futuro: endpoint para invalidar sessão no servidor — fora do escopo mínimo).
- **Dependências**: nenhuma nova dependência prevista.
