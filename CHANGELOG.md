# Changelog

![Versão](https://img.shields.io/badge/versão-1.2.0-blue)

## 1.2.0 — 2026-03-26

### Novidades

- Interface preparada para deploy atrás de um **subpath** (ex.: `/pdf-merge-tools/`): `VITE_BASE` no build e URLs de API com `import.meta.env.BASE_URL`.
- Uploads temporários por defeito em **`backend/data/uploads`** quando a aplicação corre a partir do repositório; pasta `backend/data/` ignorada pelo Git.
- Variável **`PDF_TOOLS_UPLOAD_DIR`** para definir outro diretório de uploads (opcional).
- **`load_dotenv`** executado antes dos imports internos, para `.env` aplicar ao diretório de uploads e restantes opções desde o arranque.

## 1.1.0 — 2026-03-26

### Novidades

- Primeira versão da ferramenta de merge de PDFs: envio de vários arquivos, escolha de páginas por documento e geração de um único PDF.
- Interface web para arrastar arquivos, reordenar a lista e baixar o resultado.
- Linha de comando (`pdftools merge`) para uso em scripts e automação.

### Documentação

- README: seção **Variáveis de ambiente** (`CORS_ORIGINS`, `PDF_TOOLS_STATIC`, uso de `backend/.env`).
