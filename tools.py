import re
import io
import pypdf
from PIL import Image
from crewai.tools import tool

# Global OCR Reader initialization
_easyocr_reader = None

def get_easyocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            _easyocr_reader = easyocr.Reader(['en'], gpu=False)
        except Exception:
            _easyocr_reader = False
    return _easyocr_reader

@tool("Lab Report File Reader")
def read_lab_report_file(file_content: str) -> str:
    """
    Reads and validates the raw text content extracted from an uploaded medical lab report file.
    """
    if not file_content or not file_content.strip():
        return "No readable text content found in the lab report."
    return file_content.strip()

def extract_text_from_file(uploaded_file) -> str:
    """Extracts raw text content from an uploaded PDF, TXT, or Image (PNG/JPG/JPEG) lab report file."""
    try:
        filename = uploaded_file.name.lower()
        file_bytes = uploaded_file.read()
        
        # 1. PDF File Extraction
        if filename.endswith(".pdf"):
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
            
        # 2. Image File Extraction (PNG, JPG, JPEG, BMP, TIFF) via OCR
        elif filename.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            image = Image.open(io.BytesIO(file_bytes))
            
            # Method A: Try pytesseract
            try:
                import pytesseract
                extracted_text = pytesseract.image_to_string(image)
                if extracted_text and len(extracted_text.strip()) > 10:
                    return extracted_text.strip()
            except Exception:
                pass
                
            # Method B: Try easyocr fallback
            try:
                reader = get_easyocr_reader()
                if reader:
                    results = reader.readtext(file_bytes, detail=0)
                    extracted_text = " ".join(results)
                    if extracted_text and len(extracted_text.strip()) > 5:
                        return extracted_text.strip()
            except Exception:
                pass
                
            return "Could not extract clear clinical text from image. Please ensure the lab report photo is well-lit and legible."
            
        # 3. Plain Text File Extraction (.txt)
        else:
            return file_bytes.decode("utf-8", errors="ignore").strip()
            
    except Exception as e:
        return f"Error reading file: {str(e)}"
