## ADDED Requirements

### Requirement: Reinício completo do assistente

A interface DEVE oferecer uma ação explícita para **reiniciar o processo** **em qualquer etapa** do assistente (incluindo seleção de arquivos, envio, configuração e resultado), sempre visível de forma consistente (por exemplo abaixo do indicador de passos). Ao acionar, a interface DEVE retornar à **primeira etapa** (seleção de arquivos), DEVE limpar o identificador de sessão de upload, a lista de arquivos e respectivas configurações de páginas, senhas informadas para desbloqueio, nome do arquivo de saída (restaurando o padrão definido pela aplicação) e qualquer URL de objeto do PDF gerado (revogando-a antes de descartar a referência). Se houver **envio** ou **merge** em andamento, a interface DEVE **cancelar** essas operações no cliente (por exemplo abortar a requisição de upload e a de merge) antes de aplicar o estado inicial, de modo que conclusões tardias não atualizem a tela após o reinício.

#### Scenario: Reinício a partir da configuração

- **WHEN** o usuário está na etapa de configuração com uma sessão carregada e aciona "Reiniciar processo" (ou rótulo equivalente)
- **THEN** a interface volta à etapa de seleção de PDFs sem arquivos pendentes nem sessão ativa e sem reter dados da execução anterior no cliente

#### Scenario: Reinício a partir do resultado

- **WHEN** o usuário está na etapa de resultado com download disponível e aciona "Reiniciar processo"
- **THEN** a interface revoga o blob local do PDF gerado, volta à etapa de seleção e apresenta o fluxo como novo processo

#### Scenario: Reinício na seleção ou durante envio

- **WHEN** o usuário está na primeira etapa com arquivos na fila ou na etapa de envio e aciona "Reiniciar processo"
- **THEN** o envio em curso é interrompido se existir, a fila local é limpa e a interface permanece na etapa de seleção sem dados residuais

#### Scenario: Reinício durante a geração do PDF

- **WHEN** a geração do PDF está em andamento e o usuário aciona "Reiniciar processo"
- **THEN** a requisição de merge é cancelada no cliente e o estado volta ao início sem aplicar o resultado após o cancelamento
