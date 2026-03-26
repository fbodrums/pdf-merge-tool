## Context

Hoje o `StoredFile` em `session_store.py` guarda `data: bytes` e a rota `POST /api/upload` em `main.py` faz `await f.read()` para cada `UploadFile`, carregando o PDF inteiro na RAM. Validação (`read_pdf`) e merge/extract consomem esses bytes. Com vários arquivos ou PDFs grandes, o pico de memória do processo cresce de forma relevante.

## Goals / Non-Goals

**Goals:**

- Manter o contrato HTTP e os modelos de resposta (`UploadResponse`, metadados, fluxo atômico de validação, unlock, merge).
- Persistir cada upload em disco sob um diretório dedicado (ex.: `Path(tempfile.gettempdir()) / "pdf_tools_uploads"`, criado na inicialização).
- Alterar `StoredFile` para referenciar `file_path: pathlib.Path` e expor leitura de bytes via propriedade `data` (ou uso direto de `read_bytes()` onde fizer sentido) para minimizar mudanças em `read_pdf` / `extract_pages_bytes`.
- Na rota de upload, copiar cada upload com `shutil.copyfileobj` para `NamedTemporaryFile(delete=False, suffix=".pdf")` (ou equivalente), fechando o handle antes de validar — evitando `await f.read()` como buffer único.
- Calcular `size_bytes` com `file_path.stat().st_size` (ou equivalente) para o payload de resposta.
- Ao expirar/remover sessão no `SessionStore`, apagar arquivos temporários associados (hoje só se remove o dict em memória).

**Non-Goals:**

- Armazenamento compartilhado entre instâncias (Redis, S3, volume NFS); continua single-node / disco local.
- Alterar limites de tamanho, MIME ou formato da API.
- Mudar o frontend.

## Decisions

1. **Diretório base** — `UPLOAD_DIR = Path(tempfile.gettempdir()) / "pdf_tools_uploads"` com `mkdir(parents=True, exist_ok=True)` no startup ou no primeiro uso documentado. **Rationale:** menor esforço, padrão POSIX; **Alternative:** variável de ambiente `PDF_TOOLS_UPLOAD_DIR` (pode ser follow-up).

2. **Arquivo temporário** — `tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")` + `shutil.copyfileobj(upload_file.file, tmp, length=... opcional)`. **Rationale:** streaming explícito; **Alternative:** `SpooledTemporaryFile` — menos controle direto do path final sem wrapper.

3. **API interna de bytes** — propriedade `StoredFile.data` que faz `self.file_path.read_bytes()` para compatibilidade com chamadas existentes a `sf.data`, com consciência de que isso carrega bytes na leitura (aceitável para trechos já existentes; merge pode continuar recebendo bytes ou evoluir depois). **Rationale:** mudança mínima; **Alternative:** refatorar todo o pipeline para paths (maior escopo).

4. **Limpeza** — ao `_purge_expired` / remoção de sessão, iterar `StoredFile` e `unlink(missing_ok=True)` dos paths. **Rationale:** evita vazamento de disco; **Risk:** falha de unlink deve ser logada mas não impedir remoção da sessão.

5. **Validação atômica** — manter a semântica atual: se um arquivo falha, nenhum entra na sessão; após copiar para temp, validar; em falha, apagar temp criado naquele request.

## Risks / Trade-offs

- [Disco cheio / quota] → checar `OSError` na escrita e retornar 507/500 com mensagem clara; monitorar `/tmp` em produção.
- [Arquivos órfãos se processo morrer] → aceito no escopo “menor esforço”; opcional: job de limpeza por idade (open question).
- [`.read_bytes()` na propriedade `data`] → ainda pode carregar RAM em pontos que leem o arquivo inteiro; mitigação futura: stream no merge (fora deste escopo).
- [Multi-instância] → sessões não compartilham disco entre hosts; documentado como limitação já existente para estado em memória.

## Migration Plan

1. Implementar modelo + upload + limpeza + testes.
2. Deploy: sem migração de dados (sem persistência antiga em disco).
3. Rollback: reverter commit; usuários apenas refazem upload (sessões são efêmeras).

## Open Questions

- Expor `PDF_TOOLS_UPLOAD_DIR` para ambientes com `/tmp` restritivo?
- Política de limpeza periódica para arquivos órfãos (cron) além do TTL de sessão?
