#!/usr/bin/env python3
"""Batch HTML to PDF converter with a desktop GUI.

Features:
- Select multiple HTML/HTM files from file picker
- Select output folder
- Convert each file to a PDF with the same base name
- Runs fully offline

Packaging:
- Can be packaged as a standalone executable with PyInstaller so end users
  do not need a Python installation.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from xhtml2pdf import pisa


@dataclass
class ConversionResult:
    source: Path
    destination: Path
    success: bool
    error: str = ""


def read_text_guess(path: Path) -> str:
    """Read text with pragmatic encoding fallback for Turkish and legacy files."""
    for enc in ("utf-8", "cp1254", "windows-1254", "latin-1"):
        try:
            return path.read_text(encoding=enc, errors="strict")
        except Exception:
            continue
    return path.read_bytes().decode("utf-8", errors="replace")


def convert_html_to_pdf(source: Path, destination: Path) -> ConversionResult:
    """Convert one HTML file to one PDF file."""
    try:
        html = read_text_guess(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("wb") as output_file:
            status = pisa.CreatePDF(src=html, dest=output_file)
        if status.err:
            return ConversionResult(source, destination, False, "PDF oluşturulurken hata döndü.")
        return ConversionResult(source, destination, True)
    except Exception as exc:  # noqa: BLE001
        return ConversionResult(source, destination, False, str(exc))


class HtmlToPdfApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("HTML -> PDF Toplu Dönüştürücü")
        self.root.geometry("880x560")
        self.root.minsize(760, 500)

        self.selected_files: list[Path] = []
        self.output_dir: Path | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)

        actions = ttk.Frame(container)
        actions.pack(fill="x", pady=(0, 10))

        ttk.Button(actions, text="HTML Dosyaları Seç", command=self.select_files).pack(side="left")
        ttk.Button(actions, text="Klasörden Ekle", command=self.add_folder).pack(side="left", padx=8)
        ttk.Button(actions, text="Listeyi Temizle", command=self.clear_files).pack(side="left")

        files_frame = ttk.LabelFrame(container, text="Seçilen HTML Dosyaları", padding=8)
        files_frame.pack(fill="both", expand=True)

        self.file_list = tk.Listbox(files_frame, selectmode=tk.EXTENDED)
        self.file_list.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(files_frame, orient="vertical", command=self.file_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.file_list.configure(yscrollcommand=scrollbar.set)

        out_frame = ttk.Frame(container)
        out_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(out_frame, text="Çıktı Klasörü Seç", command=self.select_output).pack(side="left")
        self.output_var = tk.StringVar(value="Henüz çıktı klasörü seçilmedi")
        ttk.Label(out_frame, textvariable=self.output_var).pack(side="left", padx=10)

        bottom = ttk.Frame(container)
        bottom.pack(fill="x", pady=(10, 0))

        self.convert_btn = ttk.Button(bottom, text="PDF'e Dönüştür", command=self.start_conversion)
        self.convert_btn.pack(side="left")

        self.progress = ttk.Progressbar(bottom, mode="determinate")
        self.progress.pack(side="left", fill="x", expand=True, padx=10)

        self.status_var = tk.StringVar(value="Hazır")
        ttk.Label(container, textvariable=self.status_var).pack(fill="x", pady=(8, 0))

    def select_files(self) -> None:
        paths = filedialog.askopenfilenames(
            title="HTML dosyalarını seçin",
            filetypes=[("HTML Files", "*.html *.htm"), ("All Files", "*.*")],
        )
        self._add_paths([Path(p) for p in paths])

    def add_folder(self) -> None:
        folder = filedialog.askdirectory(title="HTML dosyalarının bulunduğu klasörü seçin")
        if not folder:
            return
        root = Path(folder)
        html_files = sorted([*root.rglob("*.html"), *root.rglob("*.htm")])
        self._add_paths(html_files)

    def clear_files(self) -> None:
        self.selected_files.clear()
        self.file_list.delete(0, tk.END)
        self.status_var.set("Liste temizlendi")

    def _add_paths(self, paths: list[Path]) -> None:
        existing = set(self.selected_files)
        added = 0
        for path in paths:
            if path.is_file() and path.suffix.lower() in {".html", ".htm"} and path not in existing:
                self.selected_files.append(path)
                self.file_list.insert(tk.END, str(path))
                existing.add(path)
                added += 1

        if added == 0:
            self.status_var.set("Yeni HTML dosyası eklenmedi")
        else:
            self.status_var.set(f"{added} dosya eklendi. Toplam: {len(self.selected_files)}")

    def select_output(self) -> None:
        folder = filedialog.askdirectory(title="PDF kayıt klasörünü seçin")
        if not folder:
            return
        self.output_dir = Path(folder)
        self.output_var.set(str(self.output_dir))
        self.status_var.set("Çıktı klasörü seçildi")

    def start_conversion(self) -> None:
        if not self.selected_files:
            messagebox.showwarning("Eksik seçim", "Lütfen en az bir HTML dosyası seçin.")
            return

        if self.output_dir is None:
            messagebox.showwarning("Eksik seçim", "Lütfen bir çıktı klasörü seçin.")
            return

        self.convert_btn.configure(state="disabled")
        self.progress.configure(maximum=len(self.selected_files), value=0)
        self.status_var.set("Dönüştürme başladı...")

        thread = threading.Thread(target=self._run_conversion, daemon=True)
        thread.start()

    def _run_conversion(self) -> None:
        assert self.output_dir is not None

        results: list[ConversionResult] = []
        for idx, source in enumerate(self.selected_files, start=1):
            destination = self.output_dir / f"{source.stem}.pdf"
            result = convert_html_to_pdf(source, destination)
            results.append(result)
            self.root.after(0, self._update_progress, idx, source.name)

        self.root.after(0, self._finish_conversion, results)

    def _update_progress(self, value: int, current_file: str) -> None:
        self.progress.configure(value=value)
        self.status_var.set(f"Dönüştürülüyor ({value}/{len(self.selected_files)}): {current_file}")

    def _finish_conversion(self, results: list[ConversionResult]) -> None:
        self.convert_btn.configure(state="normal")
        success_count = sum(1 for r in results if r.success)
        failed = [r for r in results if not r.success]

        if failed:
            lines = [f"✓ Başarılı: {success_count}", f"✗ Hatalı: {len(failed)}", ""]
            for item in failed[:10]:
                lines.append(f"- {item.source.name}: {item.error}")
            if len(failed) > 10:
                lines.append(f"... ve {len(failed) - 10} hata daha")

            self.status_var.set(f"Tamamlandı. Başarılı: {success_count}, Hatalı: {len(failed)}")
            messagebox.showwarning("Dönüştürme tamamlandı (hatalı dosyalar var)", "\n".join(lines))
            return

        self.status_var.set(f"Tamamlandı. {success_count} dosya PDF'e dönüştürüldü")
        messagebox.showinfo("Başarılı", f"İşlem tamamlandı. {success_count} dosya PDF'e dönüştürüldü.")


def main() -> None:
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    HtmlToPdfApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
