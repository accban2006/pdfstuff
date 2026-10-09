"""Call only the local PDF/DOCX converters, without plugins or services."""

from pathlib import Path
from zipfile import ZipFile

import pdfplumber
from markitdown import MarkItDown
from markitdown.converters import DocxConverter, PdfConverter

from pdftomd.errors import ConversionError, Notice


def create_backend() -> MarkItDown:
    backend = MarkItDown(enable_builtins=False, enable_plugins=False)
    backend.register_converter(DocxConverter())
    backend.register_converter(PdfConverter())
    return backend


def convert(source: Path, destination: Path) -> list[Notice]:
    markdown = create_backend().convert_local(str(source)).markdown
    if not markdown.strip():
        raise ConversionError("no_text")
    notices = []
    if source.suffix.lower() == ".pdf":
        with pdfplumber.open(source) as pdf:
            empty_pages = []
            for index, page in enumerate(pdf.pages, 1):
                if not page.chars:
                    empty_pages.append(str(index))
                page.close()
        if empty_pages:
            notices.append(Notice("pdf_empty_pages", ", ".join(empty_pages)))
        notices.append(Notice("pdf_structure"))
    else:
        with ZipFile(source) as archive:
            names = archive.namelist()
            if any(name.startswith("word/media/") for name in names):
                notices.append(Notice("docx_images"))
            if any(name.startswith(("word/header", "word/footer")) for name in names):
                notices.append(Notice("docx_headers"))
            xml = archive.read("word/document.xml")
            if any(marker in xml for marker in (b"<w:txbxContent", b"<w:ins", b"<w:del")):
                notices.append(Notice("docx_complex"))
            if any(marker in xml for marker in (b"<w:gridSpan", b"<w:vMerge", b"<m:oMath")):
                notices.append(Notice("docx_merged_math"))
    with destination.open("w", encoding="utf-8", newline="\n") as output:
        output.write(markdown.replace("\r\n", "\n").replace("\r", "\n"))
    return notices
