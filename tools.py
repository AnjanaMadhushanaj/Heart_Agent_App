import re
import io
import pypdf
from crewai.tools import tool

@tool("Lab Report File Reader")
def read_lab_report_file(file_content: str) -> str:
    """
    Reads and validates the raw text content extracted from an uploaded medical lab report file.
    """
    if not file_content or not file_content.strip():
        return "No readable text content found in the lab report."
    return file_content.strip()

def extract_text_from_file(uploaded_file) -> str:
    """Extracts raw text content from an uploaded PDF or TXT lab report file."""
    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
        else:
            return uploaded_file.read().decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return f"Error reading file: {str(e)}"
