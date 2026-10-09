from pathlib import Path

import pytest
from markitdown import FileConversionException, MarkItDown

from pdftomd.converters.markitdown_adapter import convert
from pdftomd.errors import ConversionError

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("language", ["en", "vi"])
@pytest.mark.parametrize("extension", ["pdf", "docx"])
def test_matches_local_backend(tmp_path, language, extension):
    source = FIXTURES / f"{language}.{extension}"
    original = source.read_bytes()
    expected = MarkItDown(enable_plugins=False).convert_local(str(source)).markdown
    target = tmp_path / "result.md"
    convert(source, target)
    assert target.read_text(encoding="utf-8") == expected.replace("\r\n", "\n").replace("\r", "\n")
    text = target.read_text(encoding="utf-8")
    assert ("Tiếng Việt" if language == "vi" else "English document") in text
    for word in ("©", "±", "€", "123", "First item", "Second item", "42"):
        assert word in text
    if extension == "docx":
        assert "# " in text and "* First item" in text and "|" in text
    assert source.read_bytes() == original


def test_scan_and_corrupt_file(tmp_path):
    with pytest.raises(ConversionError, match="no_text"):
        convert(FIXTURES / "scan.pdf", tmp_path / "scan.md")
    assert not (tmp_path / "scan.md").exists()
    for extension in ("pdf", "docx"):
        source = tmp_path / f"bad.{extension}"
        source.write_bytes(b"corrupt")
        with pytest.raises(FileConversionException):
            convert(source, tmp_path / f"{extension}.md")
        assert not (tmp_path / f"{extension}.md").exists()


def test_word_images_and_headers_warn(tmp_path):
    notices = convert(FIXTURES / "word-layout.docx", tmp_path / "result.md")
    assert {n.key for n in notices} >= {"docx_images", "docx_headers"}
