"""Single source of document typography and page layout."""

import os
from functools import lru_cache
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentObject
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.text.font import Font
from fontTools.ttLib import TTFont

from pdftomd.errors import ConversionError

FONT = "Arial"
BODY_SIZE = 11
STRONG_SIZE = 15
CONTENT_WIDTH_CM = 17


def font_paths() -> list[Path]:
    folder = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    return [folder / name for name in ("arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf")]


def require_arial() -> None:
    if not all(path.is_file() for path in font_paths()):
        raise ConversionError("missing_arial")


def check_glyphs(text: str) -> None:
    require_arial()
    characters = {ord(c) for c in text if not c.isspace()}
    for path in font_paths():
        missing = characters.difference(glyphs(path, path.stat().st_mtime_ns))
        if missing:
            codes = ", ".join(f"U+{code:04X}" for code in sorted(missing)[:12])
            raise ConversionError("missing_glyph", f"{path.name}: {codes}")


@lru_cache(maxsize=8)
def glyphs(path: Path, modified: int) -> frozenset[int]:
    with TTFont(path) as font:
        return frozenset(font.getBestCmap() or {})


def format_font(font: Font, *, strong: bool = False, italic: bool = False) -> None:
    font.name = FONT
    font.size = Pt(STRONG_SIZE if strong else BODY_SIZE)
    font.bold = strong
    font.italic = italic
    font.color.rgb = RGBColor(0, 0, 0)
    fonts = font._element.get_or_add_rPr().get_or_add_rFonts()
    for name in ("ascii", "hAnsi", "eastAsia", "cs"):
        fonts.set(qn(f"w:{name}"), FONT)


def new_document() -> DocumentObject:
    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(2)
    section.left_margin = section.right_margin = Cm(2)
    for name in ("Normal", "List Bullet", "List Number", "Quote", "Hyperlink"):
        if name in document.styles:
            format_font(document.styles[name].font)
    for level in range(1, 7):
        style = document.styles[f"Heading {level}"]
        format_font(style.font, strong=True)
        style.paragraph_format.keep_with_next = True
    return document


def add_numbering(document: DocumentObject, *, ordered: bool, start: int, depth: int) -> int:
    numbering = document.part.numbering_part.element
    abstract_id = (
        max(
            (int(n.get(qn("w:abstractNumId"))) for n in numbering.findall(qn("w:abstractNum"))),
            default=-1,
        )
        + 1
    )
    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    level = OxmlElement("w:lvl")
    level.set(qn("w:ilvl"), str(depth))
    for name, value in (
        ("start", str(start)),
        ("numFmt", "decimal" if ordered else "bullet"),
        ("lvlText", f"%{depth + 1}." if ordered else "•"),
        ("suff", "space"),
    ):
        element = OxmlElement(f"w:{name}")
        element.set(qn("w:val"), value)
        level.append(element)
    properties = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), FONT)
    fonts.set(qn("w:hAnsi"), FONT)
    properties.append(fonts)
    for name, value in (("sz", str(BODY_SIZE * 2)), ("color", "000000")):
        element = OxmlElement(f"w:{name}")
        element.set(qn("w:val"), value)
        properties.append(element)
    level.append(properties)
    abstract.append(level)
    numbering.append(abstract)
    return numbering.add_num(abstract_id).numId
