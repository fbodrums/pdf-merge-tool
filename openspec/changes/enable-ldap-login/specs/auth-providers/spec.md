# auth-providers

## Purpose

Definir autenticação opcional baseada em **provedores plugáveis**, configuração por ambiente e proteção das APIs da ferramenta quando a autenticação estiver ativa.

## ADDED Requirements

### Requirement: Configuração por variáveis de ambiente

O sistema DEVE ler a habilitação de autenticação e o provedor ativo a partir de variáveis de ambiente (por exemplo documentadas em `.env.example`), incluindo pelo menos: flag que indica se a autenticação está **habilitada**, identificador do **provedor ativo** e segredo ou material necessário para **assinatura/validação de sessão** quando a autenticação estiver habilitada.

#### Scenario: Autenticação desligada em desenvolvimento

- **WHEN** a flag de autenticação está desabilitada conforme configuração
- **THEN** as rotas da API da ferramenta permanecem acessíveis sem credenciais, como hoje

#### Scenario: Autenticação ligada exige segredo de sessão

- **WHEN** a flag de autenticação está habilitada
- **THEN** o sistema exige configuração válida de segredo (ou equivalente) para emitir tokens de sessão e recusa subir ou recusa login com erro configurável se o segredo estiver ausente

### Requirement: Modelo extensível de provedores

O sistema DEVE representar cada modo de autenticação (LDAP, futuros OIDC/OAuth/local) como implementação registrada de um **contrato comum** de provedor, selecionada pela configuração do provedor ativo, de modo que adicionar um novo tipo não exija alterar a forma dos endpoints HTTP de login públicos além do necessário para novos parâmetros.

#### Scenario: Troca de provedor por configuração

- **WHEN** o identificador do provedor ativo é alterado no ambiente (por exemplo de `ldap` para um futuro `oidc`)
- **THEN** o sistema passa a delegar a validação de credenciais à implementação registrada para esse identificador, sem duplicar a lógica de cookie/token na camada HTTP

### Requirement: Endpoints de autenticação e estado de sessão

O sistema DEVE expor operações para **credenciar** o usuário, **encerrar sessão** (quando aplicável ao modelo de cookie/token) e **consultar configuração pública** necessária ao cliente (por exemplo se login é obrigatório e qual o provedor ativo), sem vazar segredos de servidor.

#### Scenario: Login com credenciais válidas

- **WHEN** um cliente envia credenciais aceitas pelo provedor ativo
- **THEN** o sistema estabelece uma sessão assinada (token) conforme o desenho e responde com sucesso

#### Scenario: Consulta de configuração sem autenticação

- **WHEN** um cliente solicita o endpoint público de configuração de autenticação
- **THEN** a resposta indica se a autenticação é obrigatória e qual o provedor ativo, sem incluir senhas ou segredos

### Requirement: Proteção das rotas da ferramenta

Quando a autenticação estiver habilitada, o sistema DEVE exigir sessão válida nas operações da API usadas pelo fluxo de PDFs (upload, merge, extração, etc.), exceto rotas explicitamente públicas de autenticação e documentação/health se mantidas públicas por decisão de implantação.

#### Scenario: Requisição sem sessão quando auth obrigatória

- **WHEN** a autenticação está habilitada e o cliente chama uma rota protegida sem sessão válida
- **THEN** o sistema responde com erro de não autorizado padronizado

#### Scenario: Requisição com sessão válida

- **WHEN** a autenticação está habilitada e o cliente apresenta sessão válida
- **THEN** a rota protegida processa a requisição normalmente
