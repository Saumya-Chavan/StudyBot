import pdfplumber

def extract_text_from_pdf(uploaded_file):
    """Extracts raw text from a PDF file object."""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        return f"Error reading PDF: {e}"
    return text
