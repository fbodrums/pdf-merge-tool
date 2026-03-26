"""Testes da CLI."""

from io import BytesIO
from pathlib import Path

from pypdf import PdfWriter
from typer.testing import CliRunner

from pdf_tools.cli import app


def _write_pdf(path: Path, pages: int = 2) -> None:
    w = PdfWriter()
    for _ in range(pages):
        w.add_blank_page(width=612, height=792)
    buf = BytesIO()
    w.write(buf)
    path.write_bytes(buf.getvalue())


def test_merge_basic(tmp_path: Path) -> None:
    a = tmp_path / "a.pdf"
    b = tmp_path / "b.pdf"
    _write_pdf(a)
    _write_pdf(b)
    out = tmp_path / "out.pdf"
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["merge", str(a), str(b), "--pages", "1", "--output", str(out)],
    )
    assert result.exit_code == 0, result.stdout
    assert out.exists()


def test_merge_invalid_file_tolerant(tmp_path: Path) -> None:
    a = tmp_path / "a.pdf"
    bad = tmp_path / "bad.pdf"
    _write_pdf(a)
    bad.write_text("nope")
    out = tmp_path / "out.pdf"
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["merge", str(a), str(bad), "--pages", "1", "--output", str(out), "--tolerant"],
    )
    assert result.exit_code == 0
    assert out.exists()
