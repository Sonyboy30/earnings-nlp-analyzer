import os
import pypdf

def extract_pdf_text(pdf_path):
    """Extract all text from a PDF file.
    
    Returns plain text, or raises an exception if extraction fails.
    """
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract PDF text: {e}")

def is_pdf(file_path):
    """Check if a file is actually a PDF by reading its magic bytes."""
    try:
        with open(file_path, 'rb') as f:
            return f.read(4) == b'%PDF'
    except:
        return False

def convert_pdf_transcripts(transcripts_dir="transcripts"):
    """Find PDF files disguised as .txt, extract text, overwrite them."""
    for filename in os.listdir(transcripts_dir):
        if not filename.endswith(".txt"):
            continue
        
        path = os.path.join(transcripts_dir, filename)
        
        if not is_pdf(path):
            continue
        
        print(f"Converting PDF: {filename}")
        
        try:
            text = extract_pdf_text(path)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  ✓ Converted successfully ({len(text)} chars)")
        except Exception as e:
            print(f"  ✗ Failed: {e}")

if __name__ == "__main__":
    convert_pdf_transcripts()
    print("\nAll PDFs converted. Run test_split.py next.")