## Why

Hoje upload, configuração de páginas, nome de saída e geração aparecem na mesma tela, o que confunde a ordem mental do fluxo (escolher → enviar → configurar → obter o PDF). Um assistente em etapas deixa explícito o que já foi feito e o que falta, com barra de progresso no envio e uma tela final dedicada ao download.

## What Changes

- Substituir o fluxo linear único por um **wizard** com etapas claras: (1) seleção de arquivos e confirmação com **Próximo**; (2) **upload** com **barra de progresso** visível; (3) **lista dos PDFs** com configuração de páginas, reordenação e nome de saída, com **Próximo**; (4) tela de **download** do PDF gerado (e estado de processamento/erro).
- Manter drag & drop, validação de PDF, desbloqueio por senha, merge e contratos de API existentes; mudança concentrada na **organização da UI** e na **navegação entre passos**.

## Capabilities

### New Capabilities

- (nenhuma — o comportamento de domínio permanece o mesmo.)

### Modified Capabilities

- `web-interface`: exigir fluxo em etapas (wizard) com indicador de passo, progresso no upload, separação entre configuração pós-upload e etapa final de download do resultado.

## Impact

- **Frontend**: `App.tsx`, possivelmente novos componentes de passo/wizard, hooks de upload/merge e layout; uso de componentes shadcn já adotados.
- **Backend**: sem alteração obrigatória de contrato se o merge continuar sendo chamado nos mesmos endpoints.
- **Especificação**: delta em `web-interface` alinhado aos novos requisitos de UX.
