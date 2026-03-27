# auth-ldap

## Purpose

Comportamento e configuração do provedor **LDAP** quando selecionado como provedor ativo de autenticação.

## Requirements

### Requirement: Variáveis de ambiente LDAP

Quando o provedor ativo for LDAP, o sistema DEVE obter conexão (host/porta, TLS) e escopo de busca (quando aplicável) a partir de variáveis de ambiente (documentadas), incluindo base de usuários, filtro de pesquisa com substituição do nome de usuário informado, e opções de TLS/startTLS conforme suportado pela implementação.

#### Scenario: Parâmetros mínimos para validar usuário

- **WHEN** o provedor ativo é LDAP e as variáveis obrigatórias estão definidas
- **THEN** o sistema consegue estabelecer conexão e validar usuário e senha contra o diretório

#### Scenario: Configuração incompleta

- **WHEN** variáveis obrigatórias do LDAP estão ausentes ou inválidas na inicialização
- **THEN** o sistema registra erro claro nos logs do servidor e não aceita login até a configuração ser corrigida

### Requirement: Validação segura de credenciais

O sistema DEVE validar a senha do usuário usando o diretório LDAP de forma segura (por exemplo bind com credenciais do usuário após resolver o DN ou bind direto), e NÃO DEVE aceitar credenciais incorretas como sucesso.

#### Scenario: Senha incorreta

- **WHEN** o usuário informa senha incorreta para uma conta existente
- **THEN** o login falha com resposta de não autorizado, sem indicar se o nome de usuário existe ou não

#### Scenario: Sucesso de autenticação

- **WHEN** o usuário e a senha correspondem a uma entrada válida no diretório
- **THEN** o fluxo de login conclui com emissão de sessão conforme o contrato global de auth

### Requirement: Erros e observabilidade

Falhas de rede, tempo esgotado ou indisponibilidade do servidor LDAP DEVEM resultar em erro adequado no cliente (por exemplo serviço indisponível ou falha genérica), com detalhes técnicos apenas em log do servidor.

#### Scenario: LDAP indisponível

- **WHEN** o servidor LDAP não responde ou a conexão falha
- **THEN** o cliente recebe mensagem genérica de falha e o servidor registra o motivo para operação
