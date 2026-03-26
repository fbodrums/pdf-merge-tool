# CHANGELOG_DEV (técnico)

## 1.3.0 — autenticação opcional (LDAP + JWT)

- **Backend:** `pdf_tools.auth` — `AuthSettings`, registro de provedores (`ldap`), JWT (PyJWT), rotas `/api/auth/*`, dependência `require_session_user` nas rotas de PDF quando `AUTH_ENABLED=true`. Dependências: `ldap3`, `PyJWT`.
- **Frontend:** `AuthGate` + `apiFetch` com `credentials: 'include'`; `useUpload` (`xhr.withCredentials`), `useMerge` e unlock em `App.tsx` alinhados ao cookie HTTP-only.
- **Testes:** `tests/test_auth.py`; `tests/test_api.py` usa `main_mod.app` para conviver com `importlib.reload`.

## 1.2.0 — deploy em subpath e uploads no repositório

- **Frontend:** `vite.config.ts` — `base` via `VITE_BASE` (default `/`). `frontend/src/lib/apiBase.ts` — `apiUrl()` junta `import.meta.env.BASE_URL` às rotas `/api/*` (`App.tsx`, `useUpload.ts`, `useMerge.ts`). `index.html` — favicon com `%BASE_URL%favicon.svg`.
- **Backend:** `main.py` — `load_dotenv` imediatamente após resolver `Path`, antes de imports `pdf_tools.*`. `session_store.py` — `PDF_TOOLS_UPLOAD_DIR` opcional; default `backend/data/uploads` quando existe `backend/pyproject.toml` no path; senão `<temp>/pdf_tools_uploads`.
- **Repo:** `.gitignore` — `backend/data/`.
- **Operação:** reverse proxy com `location /prefix/ { proxy_pass http://upstream/; }` (barra final) para o mesmo processo que serve static + API; build `VITE_BASE=/prefix/ npm run build`.

## 0.1.0 — change `pdf-merge-tool`

- Capabilities: `pdf-upload`, `page-extraction`, `pdf-merge`, `web-interface`, `cli-interface`
- Stack: FastAPI + pypdf + React (Vite) + Typer
