# PDF to Markdown Toolkit

A minimal desktop app to batch-convert PDF files to Markdown `.md` files.

## Download

**[→ Download the latest .exe (Windows)](https://github.com/kaitoooooooooooooooooooo/pdf-to-markdown-toolkit/releases/latest)**

No installation required — just run the `.exe`.

---

## Usage

1. Launch `PDF-to-Markdown.exe`
2. Click **Browse** and select a folder containing PDF files
3. The app shows how many PDFs were found
4. Click **Convert** — Markdown files are saved in the same folder

---

## Run from source

**Requirements**
```
pip install pdfplumber
```

**Launch**
```
python pdf_to_md.py
```

**Build the .exe yourself**
```
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "PDF-to-Markdown" pdf_to_md.py
```
The executable will be in `dist/PDF-to-Markdown.exe`.

---

## Notes

- Converted `.md` files are saved next to the original PDFs
- Only text-based PDFs are supported (scanned/image PDFs won't extract text)
