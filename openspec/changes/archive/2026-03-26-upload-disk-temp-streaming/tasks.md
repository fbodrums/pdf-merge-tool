## 1. Modelo e diretório de upload

- [x] 1.1 Definir `UPLOAD_DIR` (ex.: `Path(tempfile.gettempdir()) / "pdf_tools_uploads"`) e garantir criação com `mkdir(parents=True, exist_ok=True)` no arranque ou no primeiro uso.
- [x] 1.2 Alterar `StoredFile` para `file_path: Path`, remover `data: bytes` como campo obrigatório e adicionar propriedade `data` que lê `file_path.read_bytes()` (ou atualizar call sites para usar path/bytes de forma consistente).
- [x] 1.3 Revisar todos os usos de `StoredFile` / `sf.data` (`unlock`, `merge`, testes) para compatibilidade com o novo modelo.

## 2. Rota de upload com streaming

- [x] 2.1 Substituir `await f.read()` por cópia com `shutil.copyfileobj` para `NamedTemporaryFile(delete=False, suffix=".pdf")`, fechar o handle e passar o path para validação.
- [x] 2.2 Manter validação atômica: em falha de qualquer arquivo, remover temporários criados no request e não criar sessão com sucesso parcial.
- [x] 2.3 Calcular `size_bytes` via `file_path.stat().st_size` no `UploadedFileInfo`.

## 3. Limpeza e sessão

- [x] 3.1 Ao expurgar sessão expirada ou remover sessão do store, apagar arquivos em disco (`unlink(missing_ok=True)`) para cada `StoredFile` da sessão.
- [x] 3.2 Garantir que erros de unlink não impeçam remoção da sessão (log opcional).

## 4. Testes e regressão

- [x] 4.1 Atualizar ou adicionar testes em `backend/tests/` para upload, unlock e merge com arquivos em disco.
- [x] 4.2 Executar suíte de testes do backend e corrigir falhas relacionadas.
