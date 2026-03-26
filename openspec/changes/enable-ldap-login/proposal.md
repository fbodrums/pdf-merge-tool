## Why

A ferramenta hoje é aberta na rede onde o backend estiver exposto. Em ambientes corporativos é comum exigir **identidade corporativa (LDAP)** antes de usar utilitários internos. Também precisamos de uma base para **outros modos de login** (OIDC, redes sociais, credenciais próprias) sem redesenhar tudo a cada provedor.

## What Changes

- **Configuração via `.env`**: flag para habilitar autenticação, flag ou seletor de **provedor ativo** (inicialmente apenas LDAP), e variáveis específicas do LDAP (servidor, base DN, bind opcional de serviço, TLS, etc.), documentadas em `.env.example`.
- **Modelo extensível de provedores** no backend: contrato comum (por exemplo “validar credenciais / emitir sessão”), registro de implementações; **única implementação na primeira entrega: LDAP** (bind ou pesquisa + bind do usuário, conforme desenho).
- **Exigência opcional de login**: quando a autenticação estiver habilitada, as rotas da API usadas pela ferramenta passam a exigir sessão válida; sem login, o frontend não acessa o fluxo principal.
- **Frontend**: tela ou passo de login quando o modo “auth obrigatória” estiver ativo; armazenamento seguro do token/sessão (por exemplo header ou cookie, alinhado ao design) e integração com chamadas existentes.

## Capabilities

### New Capabilities

- `auth-providers`: modelo de provedores de autenticação plugáveis, configuração global (`.env`), modo “ferramenta exige login” e contrato comum para sessão/aplicação das rotas protegidas.
- `auth-ldap`: comportamento e variáveis do provedor **LDAP** quando selecionado (conexão, segurança, validação de usuário/senha, erros esperados).

### Modified Capabilities

- `web-interface`: quando a autenticação estiver habilitada no backend, a interface DEVE apresentar fluxo de login antes do assistente de PDFs e DEVE enviar credenciais/sessão de forma compatível com a API.

## Impact

- **Backend**: FastAPI (`pdf_tools.main` e novos módulos de auth), dependências para cliente LDAP (`ldap3` ou equivalente), middleware/dependências nas rotas existentes, possível endpoint de login/logout/refresh conforme design.
- **Frontend**: novo fluxo de login e cliente HTTP com credenciais; possível roteamento ou estado global de “autenticado”.
- **Operação**: variáveis de ambiente e documentação; testes em ambiente com LDAP de teste ou mock.
