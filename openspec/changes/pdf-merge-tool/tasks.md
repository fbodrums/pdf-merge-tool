## 1. Setup do Projeto

cd - [x] 1.1 Criar estrutura de diretórios do monorepo (backend/, frontend/, cli/)
- [x] 1.2 Inicializar projeto Python com pyproject.toml (dependências: fastapi, uvicorn, pypdf, python-multipart)
- [x] 1.3 Inicializar projeto React com Vite + TypeScript (npm create vite@latest)
- [x] 1.4 Configurar Tailwind CSS 4 e instalar shadcn/ui no frontend
- [x] 1.5 Configurar CORS no FastAPI para desenvolvimento local
- [x] 1.6 Criar README.md com instruções de setup e uso

## 2. Core — Lógica de PDF

- [x] 2.1 Implementar `core/page_config.py` — parsing de configuração de páginas (número, intervalo, lista combinada, remoção de duplicatas)
- [x] 2.2 Implementar `core/pdf_reader.py` — leitura e validação de PDF (tipo, integridade, detecção de senha, metadados)
- [x] 2.3 Implementar `core/pdf_extractor.py` — extração de páginas com validação de range e configuração padrão (1,2)
- [x] 2.4 Implementar `core/pdf_merger.py` — merge de múltiplos conjuntos de páginas em PDF único via BytesIO
- [x] 2.5 Implementar exceções tipadas (`exceptions.py`) — InvalidPDFError, PageOutOfRangeError, PasswordProtectedError
- [x] 2.6 Escrever testes pytest para page_config (parsing, duplicatas, intervalos inválidos)
- [x] 2.7 Escrever testes pytest para pdf_reader (PDF válido, inválido, protegido)
- [x] 2.8 Escrever testes pytest para pdf_extractor (extração, range inválido, padrão)
- [x] 2.9 Escrever testes pytest para pdf_merger (merge simples, reordenação, arquivo único)

## 3. Backend — API FastAPI

- [x] 3.1 Criar `main.py` com app FastAPI, CORS e rotas base
- [x] 3.2 Implementar endpoint POST /api/upload — receber múltiplos PDFs, validar e retornar metadados
- [x] 3.3 Implementar endpoint POST /api/unlock — receber senha para PDF protegido
- [x] 3.4 Implementar endpoint POST /api/merge — receber configuração de páginas por arquivo e retornar PDF final como StreamingResponse
- [x] 3.5 Implementar gerenciamento de sessão em memória (dict com TTL de 30 min para arquivos uploaded)
- [x] 3.6 Implementar modelos Pydantic para request/response (UploadResponse, MergeRequest, FileConfig)
- [x] 3.7 Escrever testes pytest para endpoints (upload, merge, erros)

## 4. Frontend — Interface React

- [x] 4.1 Criar layout base da página com Tailwind CSS (header, área principal, footer)
- [x] 4.2 Implementar componente UploadZone com react-dropzone (drag & drop + clique, aceitar apenas PDF)
- [x] 4.3 Implementar componente FileList — lista de arquivos com nome, páginas, campo de config e botão remover
- [x] 4.4 Implementar componente PageConfigInput — campo de texto com validação em tempo real da sintaxe de páginas
- [x] 4.5 Implementar reordenação de arquivos na FileList com @dnd-kit
- [x] 4.6 Implementar componente OutputConfig — campo para nome do arquivo de saída
- [x] 4.7 Implementar componente MergeButton — botão "Gerar PDF" com estado de loading e download
- [x] 4.8 Implementar hook useUpload — upload de arquivos para API e gerenciamento de estado
- [x] 4.9 Implementar hook useMerge — requisição de merge e download do resultado
- [x] 4.10 Implementar tratamento de erros na UI (toasts/alerts para erros do backend)
- [x] 4.11 Implementar layout responsivo (desktop lado a lado, tablet/mobile empilhado)

## 5. CLI — Interface de Linha de Comando

- [x] 5.1 Implementar `cli/main.py` com typer — comando `merge` com argumentos e opções (--pages, --output, --verbose)
- [x] 5.2 Implementar suporte a glob patterns na seleção de arquivos
- [x] 5.3 Implementar suporte a configuração via arquivo JSON (--config)
- [x] 5.4 Implementar feedback visual com rich (barra de progresso, mensagens coloridas)
- [x] 5.5 Implementar modo tolerante a erros (pular arquivos inválidos, processar restante)
- [x] 5.6 Escrever testes pytest para CLI (merge básico, opções, erros)

## 6. Integração e Finalização

- [x] 6.1 Configurar script de desenvolvimento (backend + frontend simultâneos)
- [x] 6.2 Testar fluxo completo end-to-end (upload → config → merge → download)
- [x] 6.3 Configurar build de produção do frontend e servir via FastAPI (ou documentar deploy separado)
- [x] 6.4 Criar CHANGELOG.md com versão inicial (0.1.0)
- [x] 6.5 Atualizar README.md com documentação completa (instalação, uso web, uso CLI, exemplos)
