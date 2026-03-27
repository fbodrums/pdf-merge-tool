## Context

O backend é FastAPI (`pdf_tools.main`), sem autenticação hoje; o frontend (Vite/React) chama a API diretamente. Configuração já usa `python-dotenv` e `.env` na raiz do backend. O objetivo é introduzir **provedores de autenticação plugáveis** com **LDAP como primeira implementação**, controlado por variáveis de ambiente (incluindo desligar tudo para desenvolvimento local).

## Goals / Non-Goals

**Goals:**

- Definir um **contrato interno** de provedor (por exemplo: validar credenciais e devolver identidade estável) e um **registro** onde novos tipos (OIDC, OAuth social, usuário/senha local) possam ser adicionados sem alterar o fluxo HTTP principal.
- Persistir configuração em **`.env`**: habilitar/desabilitar autenticação, escolher provedor ativo, segredos e parâmetros do LDAP.
- Quando a autenticação estiver habilitada, **proteger as rotas da API** usadas pela ferramenta e oferecer **login no frontend** antes do assistente.
- Usar dependência madura para LDAP (por exemplo **`ldap3`**) e falhas claras (credenciais inválidas vs erro de rede/servidor).

**Non-Goals:**

- Implementar OIDC, OAuth social ou cadastro local nesta entrega (apenas deixar o desenho pronto para plugar depois).
- Sincronizar usuários com banco local ou perfis ricos no LDAP além do necessário para exibir identidade na sessão.
- SSO SAML/LDAPS detalhado além do que `ldap3` + TLS permitir com variáveis de ambiente documentadas.

## Decisions

1. **Variáveis globais de auth (`.env`)**  
   - `AUTH_ENABLED` (boolean, ex.: `true`/`false`).  
   - `AUTH_PROVIDER` (string; valores conhecidos: `ldap`; futuros: `oidc`, `local`, etc.).  
   - Quando `AUTH_ENABLED=false`, o sistema ignora provedor e mantém comportamento atual (sem login).  
   - Segredo para assinatura de sessão: `AUTH_JWT_SECRET` (ou nome equivalente) obrigatório quando `AUTH_ENABLED=true`.

2. **Sessão via JWT**  
   - Após login bem-sucedido, o backend emite **JWT** (claims mínimas: `sub`, exp, talvez `provider`).  
   - Transporte preferencial: **cookie HTTP-only** `Secure` em produção + `SameSite` adequado, com alternativa documentada de header `Authorization: Bearer` para integrações, alinhado ao que o frontend implementar na mesma change.  
   - **Racional**: evita expor token em `localStorage` por padrão; FastAPI pode ler cookie ou header numa dependência única.

3. **Contrato de provedor (extensibilidade)**  
   - Interface ou classe base em Python, por exemplo `AuthProvider` com método `authenticate(username, password) -> AuthResult | raise`.  
   - Registro: mapa `provider_id -> factory` carregado na inicialização conforme `AUTH_PROVIDER`.  
   - Novos tipos adicionam módulo + entrada no registro sem mudar assinatura dos endpoints `/auth/*`.

4. **LDAP (`auth-ldap`)**  
   - Variáveis prefixadas, por exemplo: `LDAP_HOST`, `LDAP_PORT`, `LDAP_DOMAIN` (opcional), `LDAP_BIND_DN`, `LDAP_BIND_PASSWORD` (opcional se usar bind anônimo + search — documentar quando usar), `LDAP_USER_BASE_DN`, `LDAP_USER_FILTER` (com placeholder `%(username)s`), `LDAP_START_TLS` / `LDAP_USE_SSL` conforme necessário.  
   - Fluxo recomendado: conectar, (opcional) bind de serviço, **pesquisar** entrada do usuário pelo filtro, **bind com DN do usuário + senha** para validar (padrão seguro e compatível com muitos AD/OpenLDAP).  
   - Erros: distinção entre “não autorizado” (401) e falha de configuração/servidor (503/500 com log no servidor, sem vazar detalhes internos).

5. **Proteção de rotas**  
   - Dependência FastAPI `get_current_user` usada nas rotas existentes de merge/upload quando `AUTH_ENABLED=true`.  
   - Rotas públicas explícitas: `POST /auth/login`, health/docs se desejado; **todo o restante** que hoje serve o fluxo da ferramenta fica protegido.  
   - **Alternativa considerada**: API key global — rejeitada porque o requisito é identidade LDAP por usuário.

6. **Frontend**  
   - Estado global: “autenticado / não autenticado”; se `GET /auth/me` ou equivalente retornar 401 e `AUTH_ENABLED` for inferido pelo cliente via endpoint público `GET /auth/config` (retorna `{ authRequired: boolean, provider: string }`), mostrar **tela de login** antes de `App` do wizard.  
   - Cliente HTTP centralizado envia cookie (credenciais) ou header conforme decisão acima.

## Risks / Trade-offs

- **[Risco]** Configuração LDAP incorreta derruba login para todos. **Mitigação:** validação na subida (log claro), `.env.example` completo, mensagens genéricas ao cliente.  
- **[Risco]** JWT em cookie exige CORS/credentials alinhados ao origin do frontend. **Mitigação:** documentar `CORS_ORIGINS` e `allow_credentials` no FastAPI.  
- **[Trade-off]** Não implementar refresh token na v1 — JWT com TTL curto (ex.: 8h) e novo login ao expirar; aceitável para ferramenta interna.

## Migration Plan

1. Adicionar dependência `ldap3` (e possivelmente `PyJWT`) ao projeto Python.  
2. Implementar módulos de auth e proteger rotas atrás de flag.  
3. Atualizar frontend e `.env.example`.  
4. Deploy: definir `AUTH_ENABLED=true` e variáveis LDAP apenas nos ambientes que exigem; dev local permanece com `AUTH_ENABLED=false`.  
5. **Rollback**: desligar `AUTH_ENABLED` ou reverter deploy; sem migração de dados persistentes.

## Open Questions

- TTL exato do JWT e se haverá endpoint de **logout** que limpa cookie (recomendado sim para UX).  
- Se o produto precisará de **múltiplos provedores simultâneos** na mesma instância (ex.: LDAP + OIDC); hoje o desenho assume **um provedor ativo** por deploy, extensível trocando `AUTH_PROVIDER`.
