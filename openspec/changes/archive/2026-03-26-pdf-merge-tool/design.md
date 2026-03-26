## Context

Projeto novo (greenfield). Não há código existente nem infraestrutura prévia. A ferramenta precisa processar PDFs de forma efêmera (sem persistência de dados), com uma interface web moderna para uso visual e uma CLI para automação.

O usuário-alvo é interno à empresa, necessitando consolidar páginas de múltiplos PDFs (ex: extrair páginas 1 e 2 de 20 contratos e gerar um único documento).

Restrições:
- Arquivos PDF não devem ser persistidos no servidor (processamento efêmero)
- A interface deve ser fluida para operações com múltiplos arquivos
- O backend deve suportar PDFs grandes sem estourar memória

## Goals / Non-Goals

**Goals:**
- Backend Python modular com lógica de PDF isolada em `core/`
- API REST via FastAPI para upload, configuração e download
- Frontend React responsivo com upload drag & drop, configuração visual de páginas e reordenação
- CLI funcional para automação e batch processing
- Processamento rápido e baixo consumo de memória

**Non-Goals:**
- OCR ou extração de texto dos PDFs (futuro, com pdfplumber)
- Edição de conteúdo dentro das páginas (anotações, marcações)
- Autenticação/autorização de usuários (ferramenta interna sem controle de acesso)
- Armazenamento permanente de PDFs no servidor
- Conversão de/para outros formatos (Word, imagem, etc.)

## Decisions

### 1. pypdf como biblioteca única de PDF

**Escolha**: pypdf
**Alternativas**: PyPDF2 (descontinuada), pikepdf (mais pesada, C++ bindings), pdfplumber (foco em extração textual)

**Rationale**: pypdf é a evolução oficial do PyPDF2, ativamente mantida, leve (pure Python), e cobre 100% dos casos de uso: leitura, extração de páginas e merge. Não há necessidade de bibliotecas adicionais para manipulação de páginas.

### 2. FastAPI como framework web

**Escolha**: FastAPI
**Alternativas**: Flask (síncrono, sem tipagem nativa), Django (muito pesado para este caso)

**Rationale**: FastAPI oferece tipagem com Pydantic, documentação automática (Swagger), suporte nativo a upload de arquivos (UploadFile) e performance assíncrona. Ideal para uma API de processamento de arquivos.

### 3. React + shadcn/ui para frontend

**Escolha**: React 19 + TypeScript + Tailwind CSS 4 + shadcn/ui
**Alternativas**: Streamlit (limitado em UX, rerun a cada interação), Vue.js (equipe sem experiência)

**Rationale**: React com shadcn/ui permite UX fluida para operações complexas (drag & drop, configuração por arquivo, reordenação). A equipe já domina essa stack do projeto Frota. shadcn/ui fornece componentes acessíveis e consistentes sem overhead.

### 4. Arquitetura de upload: arquivo por arquivo via multipart

**Escolha**: Upload individual de cada PDF via `multipart/form-data`, mantendo arquivos em memória no backend
**Alternativas**: Upload em batch (todos de uma vez), upload para storage temporário (S3/disco)

**Rationale**: Upload individual permite feedback imediato por arquivo (validação, contagem de páginas). Manter em memória evita gerenciamento de arquivos temporários em disco. Para arquivos muito grandes (>50MB), implementar streaming.

### 5. Processamento efêmero com BytesIO

**Escolha**: Todo processamento em memória usando `io.BytesIO`. PDF final retornado como streaming response.
**Alternativas**: Salvar em /tmp e limpar com cron, usar Redis como cache

**Rationale**: Sem persistência = sem risco de vazamento de dados. BytesIO é eficiente para PDFs de tamanho típico (<50MB). FastAPI `StreamingResponse` permite enviar o resultado sem carregar tudo em memória.

### 6. Parsing de configuração de páginas

**Escolha**: Sintaxe flexível que aceita: número (`1`), intervalo (`1-3`), lista (`1,3,5`) e combinação (`1-3,5,7-9`)
**Alternativas**: Apenas seleção por checkbox (visual), apenas intervalo

**Rationale**: A sintaxe combinada é intuitiva e poderosa. No frontend, o campo de texto é complementado por atalhos visuais (botões "Todas", "Primeira", "1 e 2"). No CLI, é passado como string no argumento `--pages`.

### 7. Monorepo com backend/ e frontend/

**Escolha**: Monorepo com `backend/` (Python/FastAPI) e `frontend/` (React/Vite) na raiz
**Alternativas**: Repositórios separados, backend servindo frontend estático

**Rationale**: Projeto pequeno e coeso. Monorepo simplifica o desenvolvimento, CI/CD e deploy. Em produção, o frontend pode ser servido como build estático pelo próprio FastAPI ou por Nginx.

## Risks / Trade-offs

- **[Memória com PDFs grandes]** → PDFs acima de 50MB podem consumir muita RAM em BytesIO. Mitigação: limitar tamanho máximo de upload (configurável, padrão 50MB) e implementar streaming para o merge.

- **[Concorrência]** → Múltiplos usuários processando PDFs grandes simultaneamente podem saturar o servidor. Mitigação: FastAPI assíncrono distribui bem; para escala, adicionar fila (futura).

- **[PDFs protegidos por senha]** → pypdf suporta leitura com senha, mas a UX precisa tratar isso. Mitigação: detectar PDF protegido no upload e solicitar senha ao usuário antes de processar.

- **[PDFs corrompidos]** → Arquivos inválidos podem causar exceções inesperadas. Mitigação: validação no upload com try/except no PdfReader do pypdf; retornar erro 422 com mensagem clara.

- **[CORS]** → Frontend e backend em portas diferentes durante desenvolvimento. Mitigação: configurar CORSMiddleware no FastAPI com origins permitidos.
