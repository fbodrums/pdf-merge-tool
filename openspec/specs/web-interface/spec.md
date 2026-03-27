# web-interface

## Purpose

Interface web (upload, lista, reordenação, merge, responsivo). Sincronizado a partir do change `pdf-merge-tool` e atualizado pelo change `melhorar-layout` (shell e padronização shadcn/ui), pelo change `changelog-follow-app` (entrada ao changelog no cabeçalho), pelo change `upload-wizard-flow` (fluxo em assistente multi-etapas), pelo change `add-restart-process-button` (reinício do fluxo a qualquer etapa) e pelo change `enable-ldap-login` (tela de login quando a autenticação estiver obrigatória).

## Requirements

### Requirement: Assistente multi-etapas (wizard)

A interface DEVE organizar o fluxo de merge em um assistente com pelo menos quatro etapas lógicas: (1) seleção de arquivos; (2) envio ao servidor com feedback visual; (3) configuração de páginas, ordem e nome de saída; (4) resultado com download do PDF gerado. DEVE haver indicador visual do passo atual (por exemplo passos numerados ou breadcrumb) e ações **Voltar** / **Próximo** (ou equivalentes acessíveis) quando fizer sentido, sem perder a sessão de upload ao voltar da etapa de resultado para a de configuração quando a API permitir reutilizar `session_id`.

#### Scenario: Ordem esperada das etapas

- **WHEN** o usuário inicia a ferramenta
- **THEN** a primeira etapa exibe apenas a seleção de PDFs e a ação para avançar após escolher arquivos

#### Scenario: Navegação após seleção

- **WHEN** o usuário escolhe um ou mais PDFs e confirma o avanço
- **THEN** a interface entra na etapa de envio e inicia o upload dos arquivos selecionados

#### Scenario: Etapa de configuração após envio

- **WHEN** o upload conclui com sucesso
- **THEN** a interface apresenta a etapa em que constam a lista de arquivos, campos de páginas, reordenação e nome de saída

#### Scenario: Etapa de download após merge

- **WHEN** o usuário confirma a geração a partir da etapa de configuração
- **THEN** a interface apresenta a etapa de resultado com estado de processamento e, em caso de sucesso, a ação de download do PDF

### Requirement: Barra de progresso durante o upload

Na etapa em que os arquivos são enviados ao backend, a interface DEVE exibir uma barra de progresso (ou indicador equivalente) refletindo o andamento do envio. Se o ambiente não permitir medir progresso por byte, DEVE exibir estado de carregamento indeterminado claramente identificável.

#### Scenario: Feedback visível durante o envio

- **WHEN** o upload está em andamento
- **THEN** o usuário vê a barra de progresso ou spinner de progresso indeterminado associado à etapa de envio

#### Scenario: Conclusão do envio

- **WHEN** o upload de todos os arquivos da fila conclui com sucesso
- **THEN** a interface deixa de exibir o estado de progresso de envio e permite prosseguir para a configuração

### Requirement: Upload drag & drop

A interface web DEVE permitir, na **primeira etapa do assistente**, escolha de PDFs via drag & drop e via clique para seleção de arquivos. DEVE aceitar múltiplos arquivos simultaneamente. O envio ao backend DEVE ocorrer na **etapa seguinte**, após o usuário confirmar com **Próximo** (ou equivalente), e não automaticamente ao soltar ou ao fechar o seletor de arquivos.

#### Scenario: Upload via drag & drop

- **WHEN** o usuário arrasta 3 PDFs para a área de upload na primeira etapa e confirma o avanço
- **THEN** o fluxo entra na etapa de envio e os 3 arquivos são transmitidos ao backend; após sucesso, os arquivos passam a ser exibidos na etapa de configuração com nome e total de páginas quando disponível

#### Scenario: Upload via clique

- **WHEN** o usuário clica na área de upload na primeira etapa, seleciona arquivos no seletor e confirma o avanço
- **THEN** os arquivos selecionados são enviados na etapa de envio e, após sucesso, aparecem na etapa de configuração

#### Scenario: Upload de arquivo não-PDF

- **WHEN** o usuário tenta adicionar um arquivo que não é PDF na primeira etapa
- **THEN** a interface exibe mensagem "Apenas arquivos PDF são aceitos" e rejeita o arquivo

### Requirement: Lista de arquivos com configuração

A interface DEVE exibir a lista de PDFs enviados **na etapa de configuração** (após upload bem-sucedido), com: nome do arquivo, total de páginas, campo de configuração de páginas e botão para remover.

#### Scenario: Exibição da lista após upload

- **WHEN** 3 PDFs são carregados com sucesso
- **THEN** na etapa de configuração a interface exibe uma lista com 3 itens, cada um mostrando nome, total de páginas, e campo de páginas preenchido com "1,2" (padrão)

#### Scenario: Editar configuração de páginas

- **WHEN** o usuário altera o campo de páginas do arquivo B de "1,2" para "1-5"
- **THEN** a configuração é atualizada e validada em tempo real (feedback se inválida)

#### Scenario: Remover arquivo da lista

- **WHEN** o usuário clica no botão remover do arquivo B
- **THEN** o arquivo B é removido da lista e não será incluído no merge

### Requirement: Reordenação visual de arquivos

A interface DEVE permitir reordenação dos arquivos via drag & drop na lista **na etapa de configuração**.

#### Scenario: Arrastar arquivo para nova posição

- **WHEN** o usuário arrasta o arquivo C da posição 3 para a posição 1 na etapa de configuração
- **THEN** a lista é reordenada: C, A, B e o merge respeitará esta nova ordem

### Requirement: Botão de gerar PDF

A interface DEVE permitir, a partir da **etapa de configuração**, disparar o merge e avançar para a **etapa de resultado/download**, onde o usuário obtém o PDF final.

#### Scenario: Gerar PDF com sucesso

- **WHEN** o usuário confirma a geração na etapa de configuração com 3 arquivos configurados
- **THEN** a interface avança para a etapa de resultado, mostra indicador de progresso durante o processamento
- **AND** após conclusão, na etapa de resultado, exibe botão "Baixar PDF" com o nome do arquivo resultante

#### Scenario: Gerar PDF sem arquivos

- **WHEN** o usuário tenta gerar sem ter arquivos na sessão na etapa de configuração
- **THEN** a ação está desabilitada ou exibe mensagem "Adicione ao menos 1 PDF"

#### Scenario: Erro durante processamento

- **WHEN** ocorre erro no backend durante o merge
- **THEN** a interface exibe mensagem de erro clara na etapa de resultado e permite o usuário tentar novamente

### Requirement: Configuração do nome do arquivo de saída

A interface DEVE permitir que o usuário defina o nome do PDF final **na etapa de configuração**, antes de disparar a geração.

#### Scenario: Nome padrão

- **WHEN** o usuário não altera o campo de nome na etapa de configuração
- **THEN** o arquivo é gerado com nome "merged.pdf"

#### Scenario: Nome customizado

- **WHEN** o usuário digita "relatorio-marco-2026" no campo de nome na etapa de configuração
- **THEN** o arquivo é gerado como "relatorio-marco-2026.pdf" (extensão adicionada automaticamente se ausente)

### Requirement: Shell da aplicação com shadcn/ui

A interface DEVE organizar a página em regiões claras (cabeçalho, conteúdo principal, rodapé) usando HTML semântico (`header`, `main`, `footer` ou equivalente acessível) e componentes do conjunto shadcn/ui (por exemplo `Card` e utilitários de layout) de forma que o espaçamento, bordas e tipografia sigam os tokens de tema definidos nas variáveis CSS do projeto.

#### Scenario: Estrutura visual consistente

- **WHEN** o usuário carrega qualquer tela principal da ferramenta
- **THEN** o cabeçalho, o conteúdo e o rodapé são distinguíveis visualmente e alinhados a um container de largura máxima coerente entre breakpoints

### Requirement: Ponto de entrada ao changelog no cabeçalho

A interface DEVE oferecer, na região do cabeçalho do shell, um controle dedicado (botão ou link com aparência de ação secundária) para abrir o changelog do produto, posicionado de forma consistente com o layout de largura máxima existente e visível em desktop e tablet. O controle DEVE usar componentes de `components/ui` (por exemplo `Button` com variante outline ou ghost) e possuir rótulo acessível (texto ou `aria-label`).

#### Scenario: Cabeçalho com ação secundária

- **WHEN** o usuário visualiza a tela principal da ferramenta
- **THEN** o cabeçalho exibe o título e a descrição existentes e, na mesma faixa, o controle para abrir o changelog sem obscurecer o fluxo principal de merge de PDFs

#### Scenario: Uso em viewport estreita

- **WHEN** o usuário acessa em largura reduzida (tablet ou janela estreita)
- **THEN** o controle permanece utilizável (sem sobreposição ilegível com o título; empilhamento ou quebra de linha aceitável conforme o design responsivo atual)

### Requirement: Configuração explícita do projeto shadcn

O repositório do frontend DEVE incluir arquivo `components.json` (configuração do shadcn/ui) coerente com o bundler (Vite), aliases de importação (por exemplo `@/`) e estilos Tailwind usados pelo projeto, permitindo adicionar novos componentes via CLI oficial sem divergência de caminhos.

#### Scenario: Adicionar componente via CLI

- **WHEN** um desenvolvedor executa o comando de adição de componente shadcn apontando para o diretório do frontend
- **THEN** o componente é gerado nos caminhos esperados (`components/ui`, `lib`, etc.) e compila sem ajuste manual de alias

### Requirement: Controles interativos padronizados

Elementos interativos da interface principal (botões, campos de texto em blocos de configuração, cartões de seção, **passos do assistente**) DEVEM usar os componentes em `components/ui` derivados do shadcn (por exemplo `Button`, `Input`, `Card`) em vez de elementos HTML brutos com estilos únicos, salvo exceções justificadas (por exemplo integração com biblioteca de terceiros).

#### Scenario: Ação primária na área de upload

- **WHEN** o usuário vê a primeira etapa do fluxo de envio de PDFs
- **THEN** o botão de avanço e os campos de formulário associados usam os componentes padronizados e as classes de tema compartilhadas

### Requirement: Interface responsiva

A interface DEVE ser utilizável em desktop e tablet. O layout responsivo DEVE usar Tailwind CSS em conjunto com tokens de tema (variáveis CSS) e componentes shadcn/ui para manter consistência visual entre breakpoints. O **assistente multi-etapas** DEVE permanecer legível e utilizável (passos e ações principais acessíveis) em larguras estreitas.

#### Scenario: Uso em tela de desktop (1920px)

- **WHEN** o usuário acessa em tela larga
- **THEN** a interface apresenta o assistente com área de conteúdo confortável (por exemplo seleção e lista em layout que aproveita a largura sem esconder o indicador de etapas)

#### Scenario: Uso em tablet (768px)

- **WHEN** o usuário acessa em tablet
- **THEN** as etapas do assistente e os controles empilham ou adaptam-se verticalmente mantendo usabilidade e contraste dos botões de navegação

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

### Requirement: Fluxo de login quando autenticação obrigatória

Quando o backend indicar que a autenticação é obrigatória (por exemplo via endpoint público de configuração), a interface DEVE apresentar uma **tela de login** antes do assistente de merge de PDFs. A tela DEVE coletar credenciais compatíveis com o provedor ativo (para LDAP: identificador de usuário e senha), DEVE exibir mensagens de erro claras em português em caso de falha e DEVE permitir tentar novamente. Após autenticação bem-sucedida, a interface DEVE prosseguir para o fluxo principal existente e DEVE incluir a sessão (cookie ou header, conforme implementação) em todas as chamadas à API da ferramenta.

#### Scenario: Usuário não autenticado vê apenas login

- **WHEN** a autenticação está obrigatória e o usuário ainda não possui sessão válida
- **THEN** a interface exibe a tela de login e não exibe o assistente de PDFs até que o login seja bem-sucedido

#### Scenario: Sessão válida acessa o assistente

- **WHEN** o usuário conclui o login com sucesso
- **THEN** a interface apresenta o assistente de merge como hoje, com chamadas autenticadas à API

#### Scenario: Falha de login

- **WHEN** o servidor rejeita as credenciais
- **THEN** a interface mantém o usuário na tela de login e exibe feedback de erro sem vazar detalhes internos do servidor
