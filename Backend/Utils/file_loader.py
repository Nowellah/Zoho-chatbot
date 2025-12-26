from PyPDF2 import PdfReader
from docx import Document


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


def load_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])


def load_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
