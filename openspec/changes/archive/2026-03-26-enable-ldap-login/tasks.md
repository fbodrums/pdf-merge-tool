## 1. Dependências e configuração

- [x] 1.1 Adicionar dependências Python (`ldap3`, biblioteca JWT escolhida no design) ao projeto do backend e registrar versões no gerenciador usado pelo repo
- [x] 1.2 Documentar em `backend/.env.example` todas as variáveis: `AUTH_ENABLED`, `AUTH_PROVIDER`, segredo de sessão, variáveis LDAP e JWT/TTL conforme `design.md`

## 2. Backend — núcleo extensível e JWT

- [x] 2.1 Implementar módulo de configuração de auth a partir do ambiente (validação quando `AUTH_ENABLED=true`)
- [x] 2.2 Implementar contrato `AuthProvider`, registro por id de provedor e fábrica que instancia apenas o provedor configurado
- [x] 2.3 Implementar criação/validação de JWT e dependência FastAPI para extrair usuário atual (cookie HTTP-only e/ou header, conforme design)

## 3. Backend — LDAP

- [x] 3.1 Implementar `LdapAuthProvider` com conexão, busca por filtro e bind do usuário; mapear erros para 401/503 sem vazar detalhes
- [x] 3.2 Testar manualmente ou com teste de integração mockado contra falhas comuns (bind inválido, servidor inacessível)

## 4. Backend — rotas HTTP e proteção

- [x] 4.1 Expor `POST /auth/login`, `POST /auth/logout` (se aplicável), `GET /auth/config` e opcionalmente `GET /auth/me`
- [x] 4.2 Aplicar proteção às rotas existentes do fluxo PDF quando `AUTH_ENABLED=true`; manter comportamento atual quando desligado
- [x] 4.3 Ajustar CORS para credenciais/cookies quando o frontend usar o mesmo origin configurado em `CORS_ORIGINS`

## 5. Frontend

- [x] 5.1 Implementar cliente HTTP compartilhado com `credentials` e/ou header de autorização alinhado ao backend
- [x] 5.2 Consultar configuração pública de auth no carregamento; se obrigatória, renderizar tela de login (usuário/senha) antes do assistente
- [x] 5.3 Após login, armazenar estado de sessão conforme modelo escolhido e propagar para uploads/merge/extract
- [x] 5.4 Exibir erros de login em português e permitir nova tentativa; opção de logout visível quando autenticado

## 6. Qualidade e documentação

- [x] 6.1 Atualizar `README.md` ou documentação de deploy com pré-requisitos LDAP e flag de auth
- [x] 6.2 Revisar CHANGELOG e mensagens de commit conforme convenção do projeto
