"""One resizable Tk window; all widget access stays on the main thread."""

import ctypes
import os
import tkinter as tk
from collections import Counter
from pathlib import Path
from queue import Empty, Queue
from threading import Event, Thread
from tkinter import filedialog, font, messagebox, ttk

from pdftomd.converters.word_to_pdf import find_libreoffice, save_libreoffice
from pdftomd.errors import ConversionError
from pdftomd.i18n import translate
from pdftomd.jobs import MODES, FileResult, JobEvent, prepare, run
from pdftomd.styles import require_arial


class Application:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.language = "vi"
        self.source = tk.StringVar()
        self.destination = tk.StringVar()
        self.mode = tk.StringVar(value="pdf_md")
        self.events: Queue[JobEvent] = Queue()
        self.cancel_event = Event()
        self.worker: Thread | None = None
        self.results: list[FileResult] = []
        self.output_folder: Path | None = None
        self.closing = False
        self.status_key = "ready"
        self.status_values = {}
        self.labels = []
        self.editable = []
        self.radios = {}
        self.has_lo = find_libreoffice() is not None
        try:
            require_arial()
            self.has_arial = True
        except ConversionError:
            self.has_arial = False
        self.build()
        self.mode.trace_add("write", lambda *_: self.refresh_hint())
        self.refresh_language()
        self.root.update_idletasks()
        self.fit_window()
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.bind("<Return>", self.on_enter)
        root.after(100, self.poll)

    def text(self, key: str, **values) -> str:
        return translate(key, self.language, **values)

    def labelled(self, widget, key: str):
        self.labels.append((widget, key))
        return widget

    def build(self) -> None:
        self.root.geometry("940x560")
        self.root.minsize(850, 540)
        for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
            font.nametofont(name).configure(family="Arial", size=11)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=("Arial", 11), background="#f5f6f8", foreground="#18202c")
        style.configure("TButton", padding=(12, 7))
        style.configure("Primary.TButton", background="#2459a9", foreground="white")
        style.map("Primary.TButton", background=[("active", "#194580"), ("disabled", "#a6b2c2")])
        self.root.configure(background="#f5f6f8")
        frame = ttk.Frame(self.root, padding=22)
        frame.grid(sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(5, weight=1)

        top = ttk.Frame(frame)
        top.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 20))
        top.columnconfigure(0, weight=1)
        self.labelled(ttk.Label(top, font=("Arial", 17, "bold")), "title").grid(sticky="w")
        self.language_box = ttk.Combobox(
            top, values=("Tiếng Việt", "English"), state="readonly", width=13
        )
        self.language_box.current(0)
        self.language_box.grid(row=0, column=1, sticky="e")
        self.language_box.bind("<<ComboboxSelected>>", self.change_language)

        self.labelled(ttk.Label(frame), "source").grid(row=1, column=0, sticky="w", padx=(0, 12))
        source_entry = ttk.Entry(frame, textvariable=self.source)
        source_entry.grid(row=1, column=1, sticky="ew", pady=5)
        choose_file = self.labelled(ttk.Button(frame, command=self.choose_file), "file")
        choose_file.grid(row=1, column=2, padx=(8, 4))
        choose_source = self.labelled(ttk.Button(frame, command=self.choose_source), "folder")
        choose_source.grid(row=1, column=3, padx=(0, 14))
        self.start_button = self.labelled(
            ttk.Button(frame, command=self.start, style="Primary.TButton"), "convert"
        )
        self.start_button.grid(row=1, column=4, sticky="ew")

        self.labelled(ttk.Label(frame), "destination").grid(
            row=2, column=0, sticky="w", padx=(0, 12)
        )
        output_entry = ttk.Entry(frame, textvariable=self.destination)
        output_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5)
        choose_output = self.labelled(ttk.Button(frame, command=self.choose_output), "folder")
        choose_output.grid(row=2, column=3, padx=(8, 14))
        self.cancel_button = self.labelled(
            ttk.Button(frame, command=self.cancel, state="disabled"), "cancel"
        )
        self.cancel_button.grid(row=2, column=4, sticky="ew")
        self.editable = [source_entry, output_entry, choose_file, choose_source, choose_output]

        mode_frame = self.labelled(ttk.LabelFrame(frame, padding=(16, 12)), "mode")
        mode_frame.grid(row=3, column=0, columnspan=5, sticky="ew", pady=(20, 12))
        for column in (0, 1):
            mode_frame.columnconfigure(column, weight=1)
        for key, position in {
            "pdf_md": (0, 0),
            "word_md": (0, 1),
            "md_pdf": (1, 0),
            "md_word": (1, 1),
            "word_pdf": (2, 0),
        }.items():
            radio = self.labelled(ttk.Radiobutton(mode_frame, variable=self.mode, value=key), key)
            radio.grid(row=position[0], column=position[1], sticky="w", pady=5)
            self.radios[key] = radio
        self.hint = ttk.Label(frame, wraplength=850, foreground="#525e70")
        self.hint.grid(row=4, column=0, columnspan=5, sticky="ew")
        dependencies = ttk.Frame(frame)
        dependencies.grid(row=5, column=0, columnspan=5, sticky="nw", pady=(8, 0))
        choose_lo = self.labelled(
            ttk.Button(dependencies, command=self.choose_libreoffice), "choose_lo"
        )
        choose_lo.grid(row=0, column=0, padx=(0, 8))
        recheck = self.labelled(
            ttk.Button(dependencies, command=self.recheck_dependencies), "recheck"
        )
        recheck.grid(row=0, column=1)
        self.editable.extend([choose_lo, recheck])
        self.status = ttk.Label(frame, wraplength=850)
        self.status.grid(row=6, column=0, columnspan=5, sticky="ew", pady=(12, 8))
        self.progress = ttk.Progressbar(frame, mode="determinate")
        self.progress.grid(row=7, column=0, columnspan=5, sticky="ew")
        self.detail_button = self.labelled(
            ttk.Button(frame, command=self.show_details, state="disabled"), "details"
        )
        self.detail_button.grid(row=8, column=0, sticky="w", pady=(12, 0))
        self.open_button = self.labelled(
            ttk.Button(frame, command=self.open_output, state="disabled"), "open"
        )
        self.open_button.grid(row=8, column=1, columnspan=4, sticky="e", pady=(12, 0))
        frame.bind("<Configure>", lambda e: self.resize_labels(e.width))
        source_entry.focus_set()

    def resize_labels(self, width: int) -> None:
        for widget in (self.status, self.hint):
            widget.configure(wraplength=max(500, width - 44))

    def fit_window(self) -> None:
        # Measure after fonts, translated labels and dependency hints are present.
        scale = float(self.root.tk.call("tk", "scaling")) / (96 / 72)
        width = max(round(850 * scale), self.root.winfo_reqwidth())
        height = max(round(440 * scale), self.root.winfo_reqheight())
        self.root.minsize(width, height)
        self.root.geometry(f"{max(width, round(940 * scale))}x{max(height, round(560 * scale))}")

    def available(self, mode: str) -> bool:
        return (not mode.endswith("_pdf") or self.has_lo) and (
            not mode.startswith("md_") or self.has_arial
        )

    def refresh_language(self) -> None:
        self.root.title(self.text("title"))
        for widget, key in self.labels:
            widget.configure(text=self.text(key))
        self.refresh_hint()
        self.set_status(self.status_key, **self.status_values)
        self.update_controls()

    def refresh_hint(self) -> None:
        hints = [self.text("local")]
        if self.mode.get().startswith("md_"):
            hints.append(self.text("markdown_output"))
        if not self.has_lo:
            hints.append(self.text("missing_lo"))
        if not self.has_arial:
            hints.append(self.text("missing_arial"))
        self.hint.configure(text="\n".join(hints))

    def change_language(self, _event=None) -> None:
        self.language = "vi" if self.language_box.current() == 0 else "en"
        self.refresh_language()
        self.root.update_idletasks()
        self.fit_window()

    def set_status(self, key: str, **values) -> None:
        self.status_key, self.status_values = key, values
        self.status.configure(text=self.text(key, **values))

    def update_controls(self) -> None:
        busy = self.worker is not None
        for widget in self.editable:
            widget.configure(state="disabled" if busy else "normal")
        self.start_button.configure(state="disabled" if busy else "normal")
        self.cancel_button.configure(
            state="normal" if busy and not self.cancel_event.is_set() else "disabled"
        )
        for key, radio in self.radios.items():
            radio.configure(state="normal" if not busy and self.available(key) else "disabled")
        self.detail_button.configure(state="normal" if self.results else "disabled")
        self.open_button.configure(
            state="normal" if not busy and self.output_folder else "disabled"
        )

    def choose_file(self) -> None:
        extension = MODES[self.mode.get()][0]
        selected = filedialog.askopenfilename(
            parent=self.root,
            title=self.text("file"),
            filetypes=[
                (extension, f"*{extension}"),
                ("Markdown (.md)", "*.md"),
                (self.text("supported_files"), "*.pdf *.docx *.md"),
                (self.text("all_files"), "*.*"),
            ],
        )
        if selected:
            self.source.set(selected)
            if Path(selected).suffix.lower() == ".md" and not self.mode.get().startswith("md_"):
                self.mode.set("md_word")

    def choose_source(self) -> None:
        selected = filedialog.askdirectory(parent=self.root, title=self.text("source"))
        if selected:
            self.source.set(selected)

    def choose_output(self) -> None:
        selected = filedialog.askdirectory(
            parent=self.root, title=self.text("destination"), mustexist=False
        )
        if selected:
            self.destination.set(selected)

    def recheck_dependencies(self) -> None:
        if self.worker is not None:
            return
        self.has_lo = find_libreoffice() is not None
        try:
            require_arial()
            self.has_arial = True
        except ConversionError:
            self.has_arial = False
        self.refresh_hint()
        self.update_controls()
        self.set_status("pdf_available" if self.has_lo and self.has_arial else "ready")
        self.root.update_idletasks()
        self.fit_window()

    def choose_libreoffice(self) -> None:
        if self.worker is not None:
            return
        selected = filedialog.askopenfilename(
            parent=self.root,
            title=self.text("choose_lo"),
            filetypes=[("LibreOffice (soffice.exe / soffice.com)", "soffice.exe soffice.com")],
        )
        if not selected:
            return
        try:
            save_libreoffice(Path(selected))
        except ConversionError as exc:
            messagebox.showerror(
                self.text("error"),
                self.text(exc.notice.key, detail=exc.notice.detail),
                parent=self.root,
            )
            return
        except OSError as exc:
            messagebox.showerror(
                self.text("error"),
                self.text("path_error", detail=type(exc).__name__),
                parent=self.root,
            )
            return
        self.recheck_dependencies()

    def on_enter(self, _event=None):
        focused = self.root.focus_get()
        if isinstance(focused, ttk.Button):
            focused.invoke()
        elif focused is not self.language_box and self.worker is None:
            self.start()
        return "break"

    def start(self) -> None:
        if self.worker is not None:
            return
        try:
            plan = prepare(self.source.get(), self.destination.get(), self.mode.get())
        except ConversionError as exc:
            messagebox.showerror(
                self.text("error"),
                self.text(exc.notice.key, detail=exc.notice.detail),
                parent=self.root,
            )
            return
        except (OSError, ValueError) as exc:
            messagebox.showerror(
                self.text("error"),
                self.text("path_error", detail=type(exc).__name__),
                parent=self.root,
            )
            return
        self.output_folder = plan.destination
        self.results = []
        self.cancel_event = Event()
        self.progress.configure(value=0, maximum=len(plan.sources))
        if plan.created_directory:
            messagebox.showinfo(
                self.text("destination"),
                self.text("created", path=str(plan.destination)),
                parent=self.root,
            )
        self.worker = Thread(target=run, args=(plan, self.cancel_event, self.events), daemon=True)
        self.update_controls()
        self.worker.start()

    def cancel(self) -> None:
        if self.worker is not None:
            self.cancel_event.set()
            self.set_status(
                "cancel_after_file" if self.mode.get().endswith("_md") else "cancelling"
            )
            self.update_controls()

    def poll(self) -> None:
        try:
            while True:
                event = self.events.get_nowait()
                if event.kind == "started" and not self.cancel_event.is_set():
                    self.set_status(
                        "working", current=event.current + 1, total=event.total, name=event.filename
                    )
                elif event.kind == "result":
                    self.results.append(event.result)
                    self.progress.configure(value=event.current)
                elif event.kind == "done":
                    self.worker = None
                    counts = Counter(result.status for result in self.results)
                    self.set_status(
                        "summary",
                        **{
                            key: counts[key] for key in ("success", "warning", "error", "cancelled")
                        },
                    )
                    self.update_controls()
                    if self.closing:
                        self.root.destroy()
                        return
        except Empty:
            pass
        self.root.after(100, self.poll)

    def show_details(self) -> None:
        window = tk.Toplevel(self.root)
        window.title(self.text("details"))
        window.geometry("760x420")
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        text = tk.Text(window, wrap="word", font=("Arial", 11), padx=16, pady=16)
        text.grid(sticky="nsew")
        scrollbar = ttk.Scrollbar(window, command=text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text.configure(yscrollcommand=scrollbar.set)
        for result in self.results:
            text.insert("end", f"{result.source.name} — {self.text(result.status)}\n")
            if result.output:
                text.insert("end", f"{result.output}\n")
            for notice in result.notices:
                text.insert("end", f"• {self.text(notice.key, detail=notice.detail)}\n")
            text.insert("end", "\n")
        text.configure(state="disabled")

    def open_output(self) -> None:
        if self.output_folder is not None:
            try:
                os.startfile(self.output_folder)
            except OSError as exc:
                messagebox.showerror(
                    self.text("error"),
                    self.text("path_error", detail=type(exc).__name__),
                    parent=self.root,
                )

    def close(self) -> None:
        if self.worker is not None:
            self.closing = True
            self.cancel()
        else:
            self.root.destroy()


def main() -> None:
    if os.name == "nt":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            pass
    root = tk.Tk()
    Application(root)
    root.mainloop()
