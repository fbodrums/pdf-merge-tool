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

"""CLI pdftools (typer + rich)."""

from __future__ import annotations

import glob as glob_mod
import json
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn

from pdf_tools.core.pdf_extractor import extract_pages_bytes
from pdf_tools.core.pdf_merger import merge_pdf_parts
from pdf_tools.exceptions import InvalidPDFError, PageOutOfRangeError

app = typer.Typer(help="Ferramentas de manipulação de PDFs.", no_args_is_help=True)
console = Console()


@app.command("version")
def version_cmd() -> None:
    """Mostra a versão instalada."""
    from pdf_tools import __version__

    typer.echo(__version__)


def _expand_inputs(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for p in patterns:
        if any(ch in p for ch in "*?["):
            found = sorted(glob_mod.glob(p))
            if not found:
                console.print(f"[red]Nenhum arquivo encontrado para o padrão {p!r}[/red]")
                raise typer.Exit(code=1)
            paths.extend(Path(x) for x in found)
        else:
            paths.append(Path(p))
    return paths


def _load_config(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    raw = Path(path).read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise typer.BadParameter("O JSON de configuração deve ser um objeto no nível raiz.")
    out: dict[str, str] = {}
    for k, v in data.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise typer.BadParameter("Chaves e valores do JSON devem ser strings.")
        out[k] = v
    return out


@app.command("merge")
def merge_cmd(
    files: list[str] = typer.Argument(
        ...,
        help="Arquivos PDF ou glob patterns (ex: contratos/*.pdf).",
    ),
    pages: str = typer.Option(
        "1,2",
        "--pages",
        "-p",
        help="Páginas a extrair de cada arquivo (quando não houver --config).",
    ),
    output: str = typer.Option(
        "output.pdf",
        "--output",
        "-o",
        help="Nome do PDF de saída.",
    ),
    config: str | None = typer.Option(
        None,
        "--config",
        "-c",
        help="JSON com páginas por arquivo: {\"a.pdf\": \"1-3\", \"b.pdf\": \"1\"}.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Log detalhado.",
    ),
    tolerant: bool = typer.Option(
        False,
        "--tolerant",
        "-t",
        help="Ignorar arquivos inválidos e processar o restante.",
    ),
) -> None:
    """Extrai páginas de vários PDFs e gera um único arquivo."""
    cfg = _load_config(config)
    paths = _expand_inputs(files)
    if not paths:
        console.print("[red]Nenhum arquivo PDF informado.[/red]")
        raise typer.Exit(code=1)

    parts: list[bytes] = []
    errors: list[str] = []

    progress_cols = (
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
    )

    with Progress(*progress_cols, console=console, disable=not verbose) as progress:
        task = progress.add_task("Processando", total=len(paths))
        for path in paths:
            key = path.name
            spec = cfg.get(key) or cfg.get(str(path)) or pages
            data = path.read_bytes()
            try:
                chunk = extract_pages_bytes(data, spec if spec.strip() else None)
                parts.append(chunk)
                if verbose:
                    console.print(
                        f"[green]OK[/green] {path} → páginas {spec!r} "
                        f"({len(chunk)} bytes)"
                    )
            except (InvalidPDFError, PageOutOfRangeError, OSError) as e:
                msg = f"{path}: {e}"
                errors.append(msg)
                if tolerant:
                    console.print(f"[yellow]Ignorado:[/yellow] {msg}")
                    progress.advance(task)
                    continue
                console.print(f"[red]{msg}[/red]")
                raise typer.Exit(code=1) from e
            progress.advance(task)

    if not parts:
        console.print("[red]Nenhuma parte válida para mesclar.[/red]")
        raise typer.Exit(code=1)

    merged = merge_pdf_parts(parts)
    out_path = Path(output)
    if not out_path.suffix.lower() == ".pdf":
        out_path = out_path.with_suffix(".pdf")
    out_path.write_bytes(merged)
    console.print(
        f"[green]Gerado[/green] {out_path} ({len(merged)} bytes)"
    )
    if errors and tolerant:
        console.print(f"[yellow]{len(errors)} arquivo(s) ignorado(s).[/yellow]")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
