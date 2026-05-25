import os

def read_txt(file_path):
    """Reads a plain text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf(file_path):
    """Reads a PDF file. Requires pypdf or PyPDF2."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)
    except ImportError:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            return "\n".join(text)
        except ImportError:
            print("Warning: pypdf or PyPDF2 not installed. PDF files cannot be processed.")
            return ""

def read_docx(file_path):
    """Reads a DOCX file. Requires python-docx."""
    try:
        import docx
        doc = docx.Document(file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n".join(text)
    except ImportError:
        print("Warning: python-docx not installed. DOCX files cannot be processed.")
        return ""

def read_file(file_path):
    """Auto-detects file extension and reads content accordingly."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return read_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        return read_docx(file_path)
    else:
        return read_txt(file_path)
