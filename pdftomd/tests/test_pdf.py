from pathlib import Path
from threading import Event
from zipfile import ZIP_DEFLATED, ZipFile

import pdfplumber
import pytest

from pdftomd.converters import markdown_to_docx, word_to_pdf
from pdftomd.errors import Cancelled, ConversionError

FIXTURES = Path(__file__).parent / "fixtures"


def test_saved_libreoffice_survives_restart_and_stale_override(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "settings"))
    monkeypatch.setenv("PDFTOMD_LIBREOFFICE", str(tmp_path / "missing.exe"))
    executable = tmp_path / "Cài đặt riêng" / "program" / "soffice.exe"
    executable.parent.mkdir(parents=True)
    executable.touch()
    word_to_pdf.save_libreoffice(executable)
    assert word_to_pdf.find_libreoffice() == executable.resolve()
    monkeypatch.delenv("PDFTOMD_LIBREOFFICE")
    assert word_to_pdf.find_libreoffice() == executable.resolve()
    monkeypatch.setenv("PDFTOMD_LIBREOFFICE", str(tmp_path / "missing.exe"))
    assert word_to_pdf.find_libreoffice() == executable.resolve()
    with pytest.raises(ConversionError, match="invalid_lo"):
        word_to_pdf.save_libreoffice(FIXTURES / "en.pdf")
    assert word_to_pdf.find_libreoffice() == executable.resolve()


def test_validation(tmp_path):
    word_to_pdf.validate_pdf(FIXTURES / "en.pdf", arial=True)
    corrupt = tmp_path / "bad.pdf"
    corrupt.write_bytes(b"not pdf")
    with pytest.raises(ConversionError, match="invalid_pdf"):
        word_to_pdf.validate_pdf(corrupt)


def test_cancel_and_missing_backend(tmp_path, monkeypatch):
    monkeypatch.setattr(word_to_pdf, "find_libreoffice", lambda: None)
    with pytest.raises(ConversionError, match="missing_lo"):
        word_to_pdf.convert(FIXTURES / "en.docx", tmp_path / "out.pdf", Event())
    cancel = Event()
    cancel.set()
    with pytest.raises(Cancelled):
        word_to_pdf.convert(
            FIXTURES / "en.docx", tmp_path / "out.pdf", cancel, executable=Path("fake.exe")
        )


def test_external_resource_is_rejected(tmp_path):
    source = tmp_path / "linked.docx"
    with ZipFile(source, "w", ZIP_DEFLATED) as archive:
        archive.writestr(
            "word/_rels/document.xml.rels",
            """
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="r1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
TargetMode="External" Target="https://example.com/image.png"/>
</Relationships>""",
        )
    with pytest.raises(ConversionError, match="external_resource"):
        word_to_pdf.require_local_resources(source)


@pytest.mark.parametrize(
    "outcome,key",
    [
        ("exit_error", "lo_failed"),
        ("timeout", "lo_timeout"),
        ("missing_output", "invalid_pdf"),
        ("success", None),
        ("cancel", "cancel"),
    ],
)
def test_backend_process_outcomes(tmp_path, monkeypatch, outcome, key):
    import shutil

    target = tmp_path / "en.pdf"
    cancel = Event()

    class Process:
        pid = 99999
        returncode = 1 if outcome == "exit_error" else 0

        def poll(self):
            return None if outcome in ("timeout", "cancel") else self.returncode

        def wait(self, **kwargs):
            self.returncode = -1
            return self.returncode

        def kill(self):
            self.returncode = -1

    process = Process()
    command_seen = []

    def launch(command, **kwargs):
        command_seen.extend(command)
        assert kwargs["shell"] is False
        assert "UserInstallation=file:///" in command[1]
        if outcome == "success":
            shutil.copyfile(FIXTURES / "en.pdf", target)
        elif outcome == "cancel":
            cancel.set()
        return process

    monkeypatch.setattr(word_to_pdf.subprocess, "Popen", launch)
    monkeypatch.setattr(word_to_pdf.subprocess, "run", lambda *a, **kw: None)
    if key is None:
        word_to_pdf.convert(
            FIXTURES / "en.docx", target, cancel, executable=Path("fake.exe"), arial=True
        )
        assert target.is_file()
    else:
        error_type = Cancelled if outcome == "cancel" else ConversionError
        with pytest.raises(error_type) as error:
            word_to_pdf.convert(
                FIXTURES / "en.docx", target, cancel, executable=Path("fake.exe"), timeout=0
            )
        if isinstance(error.value, ConversionError):
            assert error.value.notice.key == key
    assert "--headless" in command_seen


@pytest.mark.skipif(word_to_pdf.find_libreoffice() is None, reason="LibreOffice not installed")
def test_real_markdown_pdf(tmp_path):
    intermediate = tmp_path / "sample.docx"
    markdown_to_docx.convert(FIXTURES / "sample.md", intermediate, Event())
    target = tmp_path / "sample.pdf"
    word_to_pdf.convert(intermediate, target, Event(), arial=True)
    with pdfplumber.open(target) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        assert "Chuyển đổi tài liệu" in text
        assert "Chữ đậm trong bảng" in text
        assert "English" in text
        assert "Tiếng Việt: Đặng, Nguyễn, cộng hòa" in text
        assert "© ± € → ≤ ≥" in text
        for level in range(3, 7):
            assert f"Heading {level}" in text
        for page in pdf.pages:
            assert all("Arial" in c["fontname"] for c in page.chars if c["text"].strip())
        chars = [c for page in pdf.pages for c in page.chars if c["text"].strip()]
        assert any(c["size"] == pytest.approx(11) for c in chars)
        assert any(c["size"] == pytest.approx(15) and "Bold" in c["fontname"] for c in chars)
        assert all(c["non_stroking_color"] in ((0, 0, 0), 0) for c in chars)


@pytest.mark.skipif(word_to_pdf.find_libreoffice() is None, reason="LibreOffice not installed")
def test_real_word_pdf(tmp_path):
    source = FIXTURES / "word-layout.docx"
    original = source.read_bytes()
    target = tmp_path / "output.pdf"
    word_to_pdf.convert(source, target, Event())
    with pdfplumber.open(target) as pdf:
        assert len(pdf.pages) == 2
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        for expected in ("HEADER", "FOOTER", "Tiếng Việt", "PAGE TWO", "42"):
            assert expected in text
        assert pdf.pages[0].images
        assert any(
            "Times" in c["fontname"] and c["size"] == pytest.approx(18) for c in pdf.pages[0].chars
        )
    assert source.read_bytes() == original
