"""Sequential background jobs, stable input snapshots and safe publication."""

import importlib.util
import logging
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from threading import Event

from pdftomd.converters import markdown_to_docx, markitdown_adapter, word_to_pdf
from pdftomd.errors import Cancelled, ConversionError, Notice
from pdftomd.styles import require_arial

MODES = {
    "pdf_md": (".pdf", ".md"),
    "word_md": (".docx", ".md"),
    "md_pdf": (".md", ".pdf"),
    "md_word": (".md", ".docx"),
    "word_pdf": (".docx", ".pdf"),
}


@dataclass(frozen=True)
class Plan:
    sources: tuple[Path, ...]
    destination: Path
    mode: str
    created_directory: bool


@dataclass(frozen=True)
class FileResult:
    source: Path
    status: str
    output: Path | None = None
    notices: tuple[Notice, ...] = ()


@dataclass(frozen=True)
class JobEvent:
    kind: str
    current: int = 0
    total: int = 0
    filename: str = ""
    result: FileResult | None = None


def check_dependencies(mode: str) -> None:
    if mode not in MODES:
        raise ConversionError("invalid_mode")
    modules = ["docx", "markdown_it", "fontTools", "PIL"] if mode.startswith("md_") else []
    if mode.endswith("_md"):
        modules += ["markitdown", "mammoth", "pdfminer", "pdfplumber"]
    for module in modules:
        if importlib.util.find_spec(module) is None:
            raise ConversionError("missing_dependency", module)
    if mode.startswith("md_"):
        require_arial()
    if mode.endswith("_pdf") and word_to_pdf.find_libreoffice() is None:
        raise ConversionError("missing_lo")


def prepare(source_text: str, destination_text: str, mode: str) -> Plan:
    check_dependencies(mode)
    if not source_text.strip() or not destination_text.strip():
        raise ConversionError("empty_paths")
    source = Path(source_text.strip().strip('"')).expanduser().resolve()
    destination = Path(destination_text.strip().strip('"')).expanduser().resolve()
    if not source.exists():
        raise ConversionError("source_missing", str(source))
    if source.is_file() and source.suffix.lower() == ".doc":
        raise ConversionError("legacy_doc")
    extension = MODES[mode][0]

    def eligible(path: Path) -> bool:
        return (
            path.is_file()
            and path.suffix.lower() == extension
            and not path.name.startswith(("~$", "~", "."))
        )

    if source.is_dir():
        sources = tuple(
            sorted(
                (p for p in source.iterdir() if eligible(p)),
                key=lambda p: (p.name.casefold(), p.name),
            )
        )
    elif eligible(source):
        sources = (source,)
    else:
        raise ConversionError("wrong_extension", extension)
    if not sources:
        raise ConversionError("no_files", extension)
    # Detect inaccessible inputs before a worker starts, without reading their content.
    for path in sources:
        with path.open("rb"):
            pass
    created = not destination.exists()
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryFile(dir=destination):
        pass
    return Plan(sources, destination, mode, created)


def publish(staged: Path, destination: Path, stem: str, extension: str) -> Path:
    """Reserve an unused name, then atomically replace our own reservation."""
    index = 0
    while True:
        name = f"{stem}{f' ({index})' if index else ''}{extension}"
        if name.casefold() in {p.name.casefold() for p in destination.iterdir()}:
            index += 1
            continue
        output = destination / name
        try:
            descriptor = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            index += 1
            continue
        os.close(descriptor)
        try:
            os.replace(staged, output)
        except BaseException:
            output.unlink(missing_ok=True)
            raise
        return output


def run(plan: Plan, cancel: Event, events: Queue[JobEvent]) -> None:
    total = len(plan.sources)
    try:
        for index, source in enumerate(plan.sources, 1):
            if cancel.is_set():
                result = FileResult(source, "cancelled")
            else:
                events.put(JobEvent("started", index - 1, total, source.name))
                try:
                    with tempfile.TemporaryDirectory(
                        prefix=".pdftomd-", dir=plan.destination
                    ) as tmp:
                        folder = Path(tmp)
                        staged = folder / (source.stem + MODES[plan.mode][1])
                        notices: list[Notice] = []
                        if plan.mode.endswith("_md"):
                            notices = markitdown_adapter.convert(source, staged)
                        elif plan.mode.startswith("md_"):
                            intermediate = folder / (source.stem + ".docx")
                            notices = markdown_to_docx.convert(source, intermediate, cancel)
                            if plan.mode == "md_pdf":
                                word_to_pdf.convert(intermediate, staged, cancel, arial=True)
                                notices.append(Notice("pdf_unverified"))
                            else:
                                staged = intermediate
                        else:
                            # Export a copy so Writer never receives the original editable file.
                            copied = folder / source.name
                            shutil.copyfile(source, copied)
                            word_to_pdf.convert(copied, staged, cancel)
                            notices.append(Notice("word_pdf_layout"))
                        if cancel.is_set():
                            raise Cancelled()
                        output = publish(staged, plan.destination, source.stem, MODES[plan.mode][1])
                    result = FileResult(
                        source, "warning" if notices else "success", output, tuple(notices)
                    )
                except Cancelled:
                    result = FileResult(source, "cancelled")
                except ConversionError as exc:
                    result = FileResult(source, "error", notices=(exc.notice,))
                except Exception as exc:
                    # Never include backend exception bodies which may contain document text.
                    logging.getLogger(__name__).warning(
                        "Conversion failed: %s (%s)", source.name, type(exc).__name__
                    )
                    result = FileResult(
                        source, "error", notices=(Notice("file_error", type(exc).__name__),)
                    )
            events.put(JobEvent("result", index, total, source.name, result))
    finally:
        events.put(JobEvent("done", total, total))
