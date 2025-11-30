# utils/pdf_reader.py
"""PDF extraction helper using pdfplumber (optional)."""

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except Exception:
    PDFPLUMBER_AVAILABLE = False

def extract_text_from_pdf_bytes(uploaded_file):
    """
    uploaded_file: Streamlit UploadedFile object
    Returns concatenated text or empty string if not available.
    """
    if not PDFPLUMBER_AVAILABLE:
        return ""
    try:
        # streamable object accepted by pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            pages = []
            for p in pdf.pages:
                txt = p.extract_text()
                if txt:
                    pages.append(txt)
        return "\n".join(pages)
    except Exception:
        return ""
