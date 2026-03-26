# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

"""Aplicação FastAPI."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_BACKEND_ROOT / ".env")

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from pdf_tools.api.models import (
    MergeRequest,
    UnlockRequest,
    UnlockResponse,
    UploadedFileInfo,
    UploadResponse,
)
from pdf_tools.api.session_store import (
    UPLOAD_DIR,
    StoredFile,
    SessionStore,
    new_file_id,
    store,
)
from pdf_tools.core.pdf_extractor import extract_pages_bytes
from pdf_tools.core.pdf_merger import merge_pdf_parts
from pdf_tools.core.pdf_reader import read_pdf
from pdf_tools.exceptions import (
    InvalidPDFError,
    PageOutOfRangeError,
    PasswordProtectedError,
)

MAX_BYTES = 50 * 1024 * 1024

_DEFAULT_CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]


def _cors_origins() -> list[str]:
    raw = os.environ.get("CORS_ORIGINS")
    if raw is None:
        return list(_DEFAULT_CORS_ORIGINS)
    return [o.strip() for o in raw.split(",") if o.strip()]


def get_store() -> SessionStore:
    return store


app = FastAPI(title="PDF Merge Tool API", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _validate_single_upload(
    f: UploadFile,
    file_path: Path,
) -> StoredFile:
    size = file_path.stat().st_size
    if size > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Arquivo excede o tamanho máximo de 50MB",
        )
    name = f.filename or "document.pdf"
    data = file_path.read_bytes()

    try:
        reader = read_pdf(data, password=None)
    except PasswordProtectedError:
        fid = new_file_id()
        return StoredFile(
            file_id=fid,
            filename=name,
            file_path=file_path,
            password=None,
            total_pages=None,
            password_protected=True,
        )
    except InvalidPDFError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    total = len(reader.pages)
    fid = new_file_id()
    return StoredFile(
        file_id=fid,
        filename=name,
        file_path=file_path,
        password=None,
        total_pages=total,
        password_protected=False,
    )


@app.post("/api/upload", response_model=UploadResponse)
async def upload_files(
    files: Annotated[list[UploadFile], File(...)],
    st: Annotated[SessionStore, Depends(get_store)],
) -> UploadResponse:
    if not files:
        raise HTTPException(status_code=422, detail="Nenhum arquivo enviado")

    paths_created: list[Path] = []
    validated: list[StoredFile] = []
    try:
        for f in files:
            tmp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
                dir=UPLOAD_DIR,
            )
            p = Path(tmp.name)
            paths_created.append(p)
            try:
                shutil.copyfileobj(f.file, tmp)
            finally:
                tmp.close()
            validated.append(_validate_single_upload(f, p))
    except HTTPException:
        for p in paths_created:
            p.unlink(missing_ok=True)
        raise
    except Exception as e:  # noqa: BLE001
        for p in paths_created:
            p.unlink(missing_ok=True)
        raise HTTPException(
            status_code=422,
            detail=f"Falha ao validar {f.filename!r}: {e}",
        ) from e

    sess = st.create_session()
    for sf in validated:
        sess.files[sf.file_id] = sf

    infos = [
        UploadedFileInfo(
            file_id=sf.file_id,
            filename=sf.filename,
            total_pages=sf.total_pages,
            size_bytes=sf.file_path.stat().st_size,
            password_protected=sf.password_protected,
        )
        for sf in validated
    ]
    return UploadResponse(session_id=sess.session_id, files=infos)


@app.post("/api/unlock", response_model=UnlockResponse)
def unlock_pdf(
    body: UnlockRequest,
    st: Annotated[SessionStore, Depends(get_store)],
) -> UnlockResponse:
    sess = st.get(body.session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Sessão não encontrada ou expirada")
    sf = sess.files.get(body.file_id)
    if not sf:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    if not sf.password_protected:
        return UnlockResponse(
            file_id=sf.file_id,
            total_pages=sf.total_pages or 0,
            password_protected=False,
        )

    try:
        reader = read_pdf(sf.data, password=body.password)
    except InvalidPDFError:
        raise HTTPException(status_code=401, detail="Senha incorreta") from None

    total = len(reader.pages)
    sf.password = body.password
    sf.total_pages = total
    sf.password_protected = False
    st.touch(body.session_id)

    return UnlockResponse(
        file_id=sf.file_id,
        total_pages=total,
        password_protected=False,
    )


@app.post("/api/merge")
def merge_pdfs(
    body: MergeRequest,
    st: Annotated[SessionStore, Depends(get_store)],
) -> StreamingResponse:
    sess = st.get(body.session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Sessão não encontrada ou expirada")

    if not body.items:
        raise HTTPException(status_code=422, detail="Lista de itens vazia")

    parts: list[bytes] = []
    for item in body.items:
        sf = sess.files.get(item.file_id)
        if not sf:
            raise HTTPException(status_code=404, detail=f"Arquivo {item.file_id} não encontrado")
        if sf.password_protected:
            raise HTTPException(
                status_code=422,
                detail=f"O arquivo {sf.filename} ainda está protegido por senha",
            )
        try:
            chunk = extract_pages_bytes(
                sf.data,
                item.pages,
                password=sf.password,
            )
        except PageOutOfRangeError as e:
            raise HTTPException(status_code=422, detail=str(e)) from e
        except InvalidPDFError as e:
            raise HTTPException(status_code=422, detail=str(e)) from e
        parts.append(chunk)

    try:
        merged = merge_pdf_parts(parts)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Erro ao mesclar PDFs: {e}") from e

    st.touch(body.session_id)
    name = body.output_filename or "merged.pdf"
    if not name.lower().endswith(".pdf"):
        name = f"{name}.pdf"

    return StreamingResponse(
        iter([merged]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


_static = os.environ.get("PDF_TOOLS_STATIC")
if _static and Path(_static).is_dir():
    app.mount(
        "/",
        StaticFiles(directory=_static, html=True),
        name="spa",
    )
