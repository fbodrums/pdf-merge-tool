## Why

Não existe uma ferramenta interna para consolidar páginas específicas de múltiplos PDFs em um único documento. Hoje, os usuários dependem de ferramentas online (inseguras para documentos sensíveis) ou softwares pagos. Precisamos de uma solução própria, rápida e visual que permita selecionar arquivos, escolher páginas e gerar o PDF final com um clique.

## What Changes

- Criar backend Python com FastAPI para processamento de PDFs (upload, extração de páginas, merge)
- Criar frontend React com TypeScript para interface visual (upload drag & drop, configuração de páginas por arquivo, reordenação, download)
- Criar CLI com typer para uso programático e automação em batch
- Usar pypdf como biblioteca principal de manipulação de PDF
- Estrutura modular: core (lógica pura), API (rotas), frontend (UI), CLI (terminal)

## Capabilities

### New Capabilities
- `pdf-upload`: Upload de múltiplos arquivos PDF com validação (tipo, tamanho, integridade)
- `page-extraction`: Extração de páginas específicas por número, intervalo (1-3) ou lista (1,3,5) com padrão configurável (páginas 1 e 2)
- `pdf-merge`: Merge de páginas extraídas em um único PDF final respeitando a ordem dos arquivos
- `web-interface`: Interface web React com upload drag & drop, configuração visual de páginas, reordenação de arquivos e download do resultado
- `cli-interface`: Interface de linha de comando com typer para uso programático e automação

### Modified Capabilities

_(Projeto novo — nenhuma capability existente a modificar)_

## Impact

- **Novas dependências backend**: Python 3.11+, FastAPI, uvicorn, pypdf, python-multipart
- **Novas dependências frontend**: React 19, TypeScript, Vite, Tailwind CSS 4, shadcn/ui, react-dropzone, react-pdf, @dnd-kit
- **Novas dependências CLI**: typer, rich
- **Infraestrutura**: Requer servidor para hospedar backend (FastAPI) e frontend (build estático ou mesmo servidor)
- **Armazenamento temporário**: Arquivos PDF ficam em memória/tmp durante processamento e são descartados após download
- **Segurança**: Arquivos não são persistidos no servidor; processamento efêmero
