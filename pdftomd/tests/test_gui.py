import time
import tkinter as tk
from pathlib import Path

import pytest

from pdftomd.gui import Application


def test_pdf_enabled_after_install_without_restart(tmp_path, monkeypatch):
    installed = False
    monkeypatch.setattr(
        "pdftomd.gui.find_libreoffice", lambda: Path("soffice.exe") if installed else None
    )
    root = tk.Tk()
    try:
        app = Application(root)
        assert "disabled" in app.radios["md_pdf"].state()
        installed = True
        app.recheck_dependencies()
        assert "disabled" not in app.radios["md_pdf"].state()
        assert "disabled" not in app.radios["word_pdf"].state()
        assert app.status_key == "pdf_available"
        assert "chưa tìm thấy LibreOffice" not in app.hint.cget("text")
        app.language_box.current(1)
        app.change_language()
        assert "LibreOffice and Arial found" in app.status.cget("text")
    finally:
        root.destroy()


def test_choose_libreoffice_persists_and_enables_pdf(tmp_path, monkeypatch):
    from pdftomd.converters.word_to_pdf import find_libreoffice

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "settings"))
    monkeypatch.setenv("PDFTOMD_LIBREOFFICE", "")
    monkeypatch.setattr("pdftomd.gui.find_libreoffice", lambda: None)
    executable = tmp_path / "LibreOffice" / "soffice.exe"
    executable.parent.mkdir()
    executable.touch()
    monkeypatch.setattr("pdftomd.gui.filedialog.askopenfilename", lambda **kw: str(executable))
    root = tk.Tk()
    try:
        app = Application(root)
        monkeypatch.setattr("pdftomd.gui.find_libreoffice", find_libreoffice)
        app.choose_libreoffice()
        assert "disabled" not in app.radios["md_pdf"].state()
        monkeypatch.delenv("PDFTOMD_LIBREOFFICE")
        assert find_libreoffice() == executable.resolve()
    finally:
        root.destroy()


def test_language_resize_worker_and_progress(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("pdftomd.gui.find_libreoffice", lambda: None)
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 2.0)
        app = Application(root)
        root.update()
        assert "disabled" in app.radios["md_pdf"].state()
        assert "disabled" in app.radios["word_pdf"].state()
        assert "disabled" not in app.radios["md_word"].state()
        assert "disabled" in app.cancel_button.state()
        app.language_box.current(1)
        app.change_language()
        assert app.start_button.cget("text") == "Convert"
        for scale, geometry in ((1.0, "940x480"), (1.5, "1200x700")):
            root.tk.call("tk", "scaling", scale)
            root.geometry(geometry)
            root.update()
            for widget, _ in app.labels:
                assert widget.winfo_rootx() >= root.winfo_rootx()
                assert widget.winfo_rootx() + widget.winfo_width() <= (
                    root.winfo_rootx() + root.winfo_width()
                )
                assert widget.winfo_rooty() + widget.winfo_height() <= (
                    root.winfo_rooty() + root.winfo_height()
                )
        monkeypatch.setattr("pdftomd.gui.messagebox.showinfo", lambda *a, **kw: None)
        source = tmp_path / "Tài liệu.md"
        source.write_text("# English / Tiếng Việt", encoding="utf-8")
        app.source.set(str(source))
        app.destination.set(str(tmp_path / "out"))
        app.mode.set("md_word")
        app.start()
        assert app.worker is not None
        assert "disabled" in app.start_button.state()
        deadline = time.monotonic() + 20
        ticks = 0
        while app.worker is not None and time.monotonic() < deadline:
            root.update()
            ticks += 1
            time.sleep(0.01)
        assert app.worker is None and ticks > 1
        assert app.status_key == "summary"
        assert app.results[0].status == "success"
        assert app.progress.cget("value") == 1
        assert "disabled" in app.cancel_button.state()
        assert "disabled" not in app.open_button.state()
    finally:
        root.destroy()


@pytest.mark.parametrize("initial_mode", ["pdf_md", "md_word", "md_pdf"])
def test_choose_markdown_file_and_output_hint(tmp_path, monkeypatch, initial_mode):
    monkeypatch.setattr("pdftomd.gui.find_libreoffice", lambda: Path("soffice.exe"))
    selected = tmp_path / "Tài liệu.MD"
    selected.write_text("# Tiếng Việt / English", encoding="utf-8")
    root = tk.Tk()
    try:
        app = Application(root)
        app.mode.set(initial_mode)
        filters = []

        def choose(**kwargs):
            filters.extend(kwargs["filetypes"])
            return str(selected)

        monkeypatch.setattr("pdftomd.gui.filedialog.askopenfilename", choose)
        app.choose_file()
        assert app.source.get() == str(selected)
        assert app.mode.get() == ("md_pdf" if initial_mode == "md_pdf" else "md_word")
        assert ("Markdown (.md)", "*.md") in filters
        assert "Arial 15 pt" in app.hint.cget("text")
        app.language_box.current(1)
        app.change_language()
        assert "Choose Word (.docx) or PDF" in app.hint.cget("text")
        app.mode.set("pdf_md")
        assert "Choose Word (.docx) or PDF" not in app.hint.cget("text")
    finally:
        root.destroy()
