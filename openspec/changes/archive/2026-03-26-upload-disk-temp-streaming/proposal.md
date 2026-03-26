## Why

O backend mantém o conteúdo dos PDFs em memória (bytes no `StoredFile`), o que aumenta o uso de RAM com uploads grandes ou muitos arquivos e pode degradar ou derrubar o processo. Persistir em disco temporário e copiar o upload em streaming reduz o pico de memória sem alterar o contrato HTTP visível ao cliente.

## What Changes

- Substituir armazenamento em memória por **arquivos temporários em disco** sob um diretório dedicado (ex.: `Path(tempfile.gettempdir()) / "pdf_tools_uploads"`), com `StoredFile` guardando `file_path` em vez de `bytes`, expondo leitura via propriedade `data` quando necessário.
- **Streaming na rota de upload**: copiar cada `UploadFile` para arquivo temporário com `shutil.copyfileobj` (chunks), evitando carregar o arquivo inteiro de uma vez.
- Garantir **criação do diretório**, **limpeza** ao remover sessão/arquivo (manter o comportamento atual de lifecycle) e testes cobrindo o novo fluxo.
- Documentar limitação conhecida: armazenamento local não é compartilhado entre múltiplas instâncias do servidor (fora do escopo desta mudança).

## Capabilities

### New Capabilities

- (nenhuma capacidade nova de domínio; o comportamento da API permanece o mesmo para o cliente.)

### Modified Capabilities

- `pdf-upload`: acrescentar requisitos não funcionais sobre persistência em disco e cópia em streaming do upload, alinhados ao design técnico, sem quebrar cenários existentes de validação, resposta e desbloqueio por senha.

## Impact

- **Backend**: modelos `StoredFile` / store em memória, rotas `upload` (e pontos que leem bytes), utilitários de arquivo temporário, testes em `backend/tests/`.
- **Frontend / CLI**: sem mudança de contrato esperada; apenas regressão se algum fluxo assumir detalhe interno de armazenamento.
- **Infra**: uso de disco no diretório temporário do SO; monitorar espaço em ambientes com muitos uploads simultâneos.
