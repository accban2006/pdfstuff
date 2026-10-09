"""Isolated, cancellable LibreOffice conversion and PDF validation."""

import os
import shutil
import subprocess
import time
from pathlib import Path
from threading import Event
from xml.etree import ElementTree
from zipfile import ZipFile

import pdfplumber

from pdftomd.errors import Cancelled, ConversionError


def libreoffice_config_path() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".config"))
    return folder / "pdftomd" / "libreoffice.txt"


def save_libreoffice(executable: Path) -> None:
    executable = executable.resolve()
    if executable.name.lower() not in {"soffice.exe", "soffice.com", "soffice"} or not (
        executable.is_file()
    ):
        raise ConversionError("invalid_lo", str(executable))
    config = libreoffice_config_path()
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(str(executable), encoding="utf-8")
    # A selection in the GUI also replaces a stale environment override for this run.
    os.environ["PDFTOMD_LIBREOFFICE"] = str(executable)


def find_libreoffice() -> Path | None:
    configured = os.environ.get("PDFTOMD_LIBREOFFICE")
    candidates = [configured] if configured else []
    try:
        candidates.append(libreoffice_config_path().read_text(encoding="utf-8").strip())
    except (OSError, UnicodeError):
        pass
    candidates += [shutil.which("soffice.com"), shutil.which("soffice")]
    for key in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        folder = os.environ.get(key)
        if folder:
            candidates += [
                str(Path(folder) / "LibreOffice/program/soffice.com"),
                str(Path(folder) / "LibreOffice/program/soffice.exe"),
            ]
    return next((Path(p).resolve() for p in candidates if p and Path(p).is_file()), None)


def validate_pdf(path: Path, *, arial: bool = False) -> None:
    try:
        with path.open("rb") as stream:
            if stream.read(5) != b"%PDF-":
                raise ValueError("Invalid PDF header")
        with pdfplumber.open(path) as pdf:
            if not pdf.pages:
                raise ValueError("PDF has no pages")
            for page in pdf.pages:
                if arial:
                    fonts = {c["fontname"] for c in page.chars if c["text"].strip()}
                    unexpected = {font for font in fonts if "arial" not in font.lower()}
                    if unexpected:
                        raise ConversionError("pdf_font", ", ".join(sorted(unexpected)))
                # Force parsing each page, including the direct Word export path.
                _ = page.chars
                page.close()
    except ConversionError:
        raise
    except Exception as exc:
        raise ConversionError("invalid_pdf", path.name) from exc


def require_local_resources(source: Path) -> None:
    with ZipFile(source) as archive:
        for name in archive.namelist():
            if name.endswith(".rels"):
                for relation in ElementTree.fromstring(archive.read(name)):
                    if relation.get("TargetMode") == "External" and not relation.get(
                        "Type", ""
                    ).endswith("/hyperlink"):
                        raise ConversionError("external_resource", relation.get("Target", ""))


def convert(
    source: Path,
    destination: Path,
    cancel: Event,
    *,
    executable: Path | None = None,
    timeout: float = 120,
    arial: bool = False,
) -> None:
    executable = executable or find_libreoffice()
    if executable is None:
        raise ConversionError("missing_lo")
    if cancel.is_set():
        raise Cancelled()
    require_local_resources(source)
    # Caller owns the temporary task directory; never share a running user profile.
    profile = destination.parent / "lo-profile"
    profile.mkdir()
    command = [
        str(executable),
        f"-env:UserInstallation={profile.resolve().as_uri()}",
        "--headless",
        "--nologo",
        "--nodefault",
        "--norestore",
        "--convert-to",
        "pdf:writer_pdf_Export",
        "--outdir",
        str(destination.parent),
        str(source.resolve()),
    ]
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    started = time.monotonic()
    # Files prevent pipe buffers from deadlocking on large diagnostic output.
    with (
        (destination.parent / "lo-stdout.log").open("wb") as stdout,
        (destination.parent / "lo-stderr.log").open("wb") as stderr,
    ):
        process = subprocess.Popen(
            command, shell=False, stdout=stdout, stderr=stderr, creationflags=flags
        )
        try:
            while process.poll() is None:
                if cancel.wait(0.1):
                    raise Cancelled()
                if time.monotonic() - started > timeout:
                    raise ConversionError("lo_timeout")
            if cancel.is_set():
                raise Cancelled()
            if process.returncode != 0:
                raise ConversionError("lo_failed", str(process.returncode))
        finally:
            if process.poll() is None:
                # soffice may launch soffice.bin; terminate only this isolated tree.
                if os.name == "nt":
                    subprocess.run(
                        ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                        shell=False,
                        creationflags=flags,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                else:
                    process.kill()
                process.wait(timeout=10)
    produced = destination.parent / (source.stem + ".pdf")
    validate_pdf(produced, arial=arial)
    if produced != destination:
        produced.rename(destination)
