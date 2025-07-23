import PyPDF2
import io
from typing import List, Dict, Any
from pathlib import Path


class PDFReader:
    """PDF reading tool for extracting text content from PDF files."""
    
    def __init__(self):
        self.name = "pdf_reader"
        self.description = "Extract text content from PDF files"
    
    def read_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dict containing extracted text, page count, and metadata
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                    "text": "",
                    "page_count": 0,
                    "metadata": {}
                }
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                metadata = {}
                if pdf_reader.metadata:
                    metadata = {
                        "title": pdf_reader.metadata.get("/Title", ""),
                        "author": pdf_reader.metadata.get("/Author", ""),
                        "subject": pdf_reader.metadata.get("/Subject", ""),
                        "creator": pdf_reader.metadata.get("/Creator", ""),
                        "producer": pdf_reader.metadata.get("/Producer", ""),
                        "creation_date": str(pdf_reader.metadata.get("/CreationDate", "")),
                        "modification_date": str(pdf_reader.metadata.get("/ModDate", ""))
                    }
                
                # Extract text from all pages
                full_text = ""
                page_texts = []
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    page_texts.append({
                        "page_number": page_num + 1,
                        "text": page_text,
                        "word_count": len(page_text.split())
                    })
                    full_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                
                return {
                    "success": True,
                    "text": full_text.strip(),
                    "page_count": len(pdf_reader.pages),
                    "pages": page_texts,
                    "metadata": metadata,
                    "file_path": str(file_path),
                    "word_count": len(full_text.split())
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading PDF: {str(e)}",
                "text": "",
                "page_count": 0,
                "metadata": {}
            }
    
    def read_pdf_pages(self, file_path: str, start_page: int = 1, end_page: int = None) -> Dict[str, Any]:
        """
        Extract text from specific pages of a PDF file.
        
        Args:
            file_path: Path to the PDF file
            start_page: Starting page number (1-indexed)
            end_page: Ending page number (1-indexed), None for last page
            
        Returns:
            Dict containing extracted text from specified pages
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                    "text": "",
                    "pages_processed": 0
                }
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                # Validate page ranges
                start_page = max(1, start_page)
                end_page = min(total_pages, end_page or total_pages)
                
                if start_page > total_pages:
                    return {
                        "success": False,
                        "error": f"Start page {start_page} exceeds total pages {total_pages}",
                        "text": "",
                        "pages_processed": 0
                    }
                
                # Extract text from specified pages
                extracted_text = ""
                pages_processed = 0
                
                for page_num in range(start_page - 1, end_page):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    pages_processed += 1
                
                return {
                    "success": True,
                    "text": extracted_text.strip(),
                    "pages_processed": pages_processed,
                    "start_page": start_page,
                    "end_page": end_page,
                    "total_pages": total_pages,
                    "file_path": str(file_path)
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading PDF pages: {str(e)}",
                "text": "",
                "pages_processed": 0
            }


# Create a global instance
pdf_reader = PDFReader() 