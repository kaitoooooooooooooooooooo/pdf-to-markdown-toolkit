import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk

import pdfplumber

BG = "#f5f5f5"
WHITE = "#ffffff"
BORDER = "#d9d9d9"
FG = "#1a1a1a"
FG_DIM = "#888888"
ACCENT = "#1a1a1a"
SUCCESS = "#2e7d32"
ERROR = "#c0392b"
FONT_TITLE = ("Segoe UI", 13, "bold")
FONT_MAIN = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)


def scan_folder(folder):
    if not folder or not os.path.isdir(folder):
        return []
    return [f for f in os.listdir(folder) if f.endswith(".pdf")]


def browse():
    folder = filedialog.askdirectory()
    if folder:
        path_var.set(folder)
        pdfs = scan_folder(folder)
        if pdfs:
            info_label.config(
                text=f"{len(pdfs)} PDF file(s) found",
                fg=FG_DIM,
            )
            btn_convert.config(state="normal")
        else:
            info_label.config(text="No PDF files found in this folder.", fg=ERROR)
            btn_convert.config(state="disabled")
        progress["value"] = 0
        status_label.config(text="")


def convert():
    folder = path_var.get()
    pdfs = scan_folder(folder)
    if not pdfs:
        return

    btn_convert.config(state="disabled")
    btn_browse.config(state="disabled")
    progress["value"] = 0
    progress["maximum"] = len(pdfs)
    status_label.config(text="Converting…", fg=FG_DIM)

    def run():
        for i, filename in enumerate(pdfs):
            pdf_path = os.path.join(folder, filename)
            md_path = os.path.join(folder, filename.replace(".pdf", ".md"))
            full_text = ""

            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n\n"

            with open(md_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            progress["value"] = i + 1
            status_label.config(text=f"{i + 1} / {len(pdfs)}  —  {filename}", fg=FG_DIM)
            root.update_idletasks()

        status_label.config(text=f"Done — {len(pdfs)} file(s) converted.", fg=SUCCESS)
        info_label.config(text="")
        btn_convert.config(state="disabled")
        btn_browse.config(state="normal")

    threading.Thread(target=run, daemon=True).start()


def draw_icon(canvas):
    canvas.create_rectangle(2, 1, 18, 23, fill=WHITE, outline="#bbbbbb", width=1)
    canvas.create_polygon(13, 1, 18, 6, 18, 6, 13, 6, fill="#dddddd", outline="#bbbbbb")
    canvas.create_rectangle(13, 1, 18, 6, fill="#e8e8e8", outline="#bbbbbb", width=1)
    canvas.create_text(10, 14, text="PDF", font=("Segoe UI", 4, "bold"), fill="#555555")

    canvas.create_line(22, 12, 30, 12, fill="#888888", width=1.5)
    canvas.create_polygon(28, 9, 32, 12, 28, 15, fill="#888888", outline="")

    canvas.create_rectangle(34, 1, 50, 23, fill=WHITE, outline="#bbbbbb", width=1)
    canvas.create_polygon(45, 1, 50, 6, 50, 6, 45, 6, fill="#dddddd", outline="#bbbbbb")
    canvas.create_rectangle(45, 1, 50, 6, fill="#e8e8e8", outline="#bbbbbb", width=1)
    canvas.create_text(42, 14, text="MD", font=("Segoe UI", 4, "bold"), fill="#555555")


root = tk.Tk()
root.title("PDF to Markdown")
root.resizable(False, False)
root.configure(bg=BG)

outer = tk.Frame(root, bg=BG, padx=32, pady=28)
outer.pack()

header = tk.Frame(outer, bg=BG)
header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 20))

icon_canvas = tk.Canvas(header, width=52, height=24, bg=BG, highlightthickness=0)
icon_canvas.pack(side="left", padx=(0, 10))
draw_icon(icon_canvas)

tk.Label(header, text="PDF to Markdown", font=FONT_TITLE, bg=BG, fg=FG).pack(side="left")

tk.Label(outer, text="SOURCE FOLDER", font=("Segoe UI", 8), bg=BG, fg=FG_DIM).grid(
    row=1, column=0, columnspan=3, sticky="w", pady=(0, 5)
)

path_var = tk.StringVar()

entry_frame = tk.Frame(outer, bg=WHITE, highlightthickness=1, highlightbackground=BORDER)
entry_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(0, 8))

entry = tk.Entry(
    entry_frame,
    textvariable=path_var,
    width=34,
    font=FONT_MAIN,
    bg=WHITE,
    fg=FG,
    insertbackground=FG,
    relief="flat",
    bd=6,
)
entry.pack(fill="x")

btn_browse = tk.Button(
    outer,
    text="Browse",
    command=browse,
    font=FONT_MAIN,
    bg=WHITE,
    fg=FG,
    activebackground=BORDER,
    activeforeground=FG,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=BORDER,
    padx=14,
    pady=7,
    cursor="hand2",
)
btn_browse.grid(row=2, column=2, sticky="ew")

info_label = tk.Label(outer, text="", font=FONT_SMALL, bg=BG, fg=FG_DIM)
info_label.grid(row=3, column=0, columnspan=3, sticky="w", pady=(8, 0))

sep = tk.Frame(outer, bg=BORDER, height=1)
sep.grid(row=4, column=0, columnspan=3, sticky="ew", pady=16)

btn_convert = tk.Button(
    outer,
    text="Convert",
    command=convert,
    font=("Segoe UI", 10, "bold"),
    bg=ACCENT,
    fg=WHITE,
    activebackground="#333333",
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=0,
    pady=10,
    cursor="hand2",
    state="disabled",
)
btn_convert.grid(row=5, column=0, columnspan=3, sticky="ew")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Grey.Horizontal.TProgressbar",
    troughcolor=BORDER,
    background="#555555",
    bordercolor=BG,
    lightcolor="#555555",
    darkcolor="#555555",
    thickness=4,
)

progress = ttk.Progressbar(
    outer,
    orient="horizontal",
    mode="determinate",
    style="Grey.Horizontal.TProgressbar",
)
progress.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(12, 4))

status_label = tk.Label(outer, text="", font=FONT_SMALL, bg=BG, fg=FG_DIM)
status_label.grid(row=7, column=0, columnspan=3, sticky="w")

root.mainloop()
