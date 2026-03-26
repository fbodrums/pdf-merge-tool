# PDF Merge Tool

Ferramenta para extrair páginas específicas de vários arquivos PDF e gerar um único documento. Inclui **API FastAPI**, **interface web (React + Vite)** e **CLI** (`pdftools`).

## Requisitos

- Python 3.11+
- Node.js 20+ (apenas para o frontend)

## Instalação (backend)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

O comando `pdftools` fica disponível no ambiente virtual.

## Instalação (frontend)

```bash
cd frontend
npm install
```

## Variáveis de ambiente (backend)

O servidor carrega automaticamente o arquivo **`backend/.env`** (se existir). Você pode copiar `backend/.env.example` como ponto de partida. Variáveis também podem ser definidas no shell (`export …`) antes de subir o `uvicorn`.

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `CORS_ORIGINS` | Não | Lista de origens permitidas no CORS, **separadas por vírgula** (espaços ao redor são ignorados). Se **não** estiver definida, o padrão é desenvolvimento local: `http://localhost:5173`, `http://127.0.0.1:5173`, `http://localhost:4173` e `http://127.0.0.1:4173`. Se estiver definida (mesmo vazia), só entram as URLs informadas — útil em produção para restringir ao domínio do front. |
| `PDF_TOOLS_STATIC` | Não | Caminho absoluto da pasta `frontend/dist` para servir a interface na raiz da API (ver [Build de produção](#build-de-produção-frontend--servir-pela-api)). |

Exemplo de `.env` para produção com front em outro host:

```env
CORS_ORIGINS=https://tools.exemplo.com.br
PDF_TOOLS_STATIC=/caminho/absoluto/para/pdf/frontend/dist
```

## Desenvolvimento (API + web)

Na raiz do repositório (após `npm install` na raiz para instalar `concurrently`):

```bash
npm run dev
```

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000) — documentação em `/docs`
- Frontend (Vite): [http://127.0.0.1:5173](http://127.0.0.1:5173) — o proxy envia `/api` para o backend

**Importante:** o script `dev:api` assume `backend/.venv`. Crie o virtualenv conforme a seção de instalação.

### Apenas o backend

```bash
cd backend && source .venv/bin/activate
uvicorn pdf_tools.main:app --reload --host 127.0.0.1 --port 8000
```

### Apenas o frontend

```bash
cd frontend && npm run dev
```

## Build de produção (frontend + servir pela API)

```bash
cd frontend && npm run build
```

Defina `PDF_TOOLS_STATIC` com o caminho absoluto para `frontend/dist` (no `backend/.env` ou via `export`; ver [Variáveis de ambiente](#variáveis-de-ambiente-backend)). Ajuste `CORS_ORIGINS` se o front não estiver no mesmo host/porta do padrão de desenvolvimento.

```bash
export PDF_TOOLS_STATIC=/caminho/para/pdf/frontend/dist
cd backend && source .venv/bin/activate
uvicorn pdf_tools.main:app --host 0.0.0.0 --port 8000
```

A API continua em `/api/*`; a interface é servida na raiz (`/`).

## Uso da CLI

```bash
pdftools merge arquivo1.pdf arquivo2.pdf
pdftools merge *.pdf --pages "1,3-5" --output resultado.pdf
pdftools merge contratos/*.pdf --config pages.json --tolerant --verbose
pdftools version
```

- **`--pages`**: páginas por arquivo quando não há `--config` (padrão `1,2`).
- **`--config`**: JSON com chave = nome do arquivo e valor = especificação de páginas, por exemplo `{"a.pdf": "1-3", "b.pdf": "1"}`.
- **`--tolerant`**: ignora arquivos inválidos e segue com os demais.

## Testes

```bash
cd backend && source .venv/bin/activate
pytest
```

## Estrutura

- `backend/src/pdf_tools/` — núcleo (`core/`), API (`main.py`, `api/`), CLI (`cli.py`)
- `frontend/` — React + TypeScript + Tailwind CSS v4
- `openspec/` — especificações OpenSpec do projeto

## Licença

Este projeto está licenciado sob a [GNU General Public License v3.0](LICENSE) (GPL-3.0-only).
