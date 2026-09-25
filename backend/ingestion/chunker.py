from pathlib import Path
import os

_converter = None
_chunker = None

def get_chunker_tools():
    global _converter, _chunker
    if _converter is None:
        os.environ.setdefault("HF_HOME", "D:/cache/huggingface")
        os.environ.setdefault("TORCH_HOME", "D:/cache/torch")
        os.environ.setdefault("DOCLING_CACHE_DIR", "D:/cache/docling")
        from docling.document_converter import DocumentConverter
        from docling.chunking import HybridChunker
        _converter = DocumentConverter()
        _chunker = HybridChunker()
    return _converter, _chunker

def chunk_document(pdf_path: str):
    pdf_path = str(Path(pdf_path).resolve())
    chunks = []
    
    # Try Docling first
    try:
        converter, chunker = get_chunker_tools()
        result = converter.convert(pdf_path)
        for chunk in chunker.chunk(result.document):
            text = getattr(chunk, "text", None) or str(chunk)
            if text and text.strip():
                chunks.append(text.strip())
    except Exception as e:
        print(f"Docling conversion warning: {e}")
        
    # If Docling returned nothing or threw an error, use pypdfium2 fallback
    if not chunks:
        try:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(pdf_path)
            full_text = []
            for page in pdf:
                textpage = page.get_textpage()
                extracted = textpage.get_text_range()
                if extracted.strip():
                    full_text.append(extracted.strip())
            joined = "\n\n".join(full_text)
            if joined:
                chunk_size = 600
                overlap = 100
                for i in range(0, len(joined), chunk_size - overlap):
                    c = joined[i:i + chunk_size]
                    if c.strip():
                        chunks.append(c.strip())
        except Exception as err:
            print(f"Fallback parser error: {err}")
            
    return chunks