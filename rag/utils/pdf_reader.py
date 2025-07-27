from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def read_pdf_documents(document_path: str) -> List[Document]:
    """
    Load and read a PDF file from a given path.
    
    Args:
        document_path (str): Path to the PDF file
        
    Returns:
        List[Document]: List of documents loaded from the PDF
    """
    loader = PyPDFLoader(document_path)
    documents = loader.load()
    return documents


def read_pdf_content(document_path: str) -> str:
    """
    Read PDF content and return as a single string.
    
    Args:
        document_path (str): Path to the PDF file
        
    Returns:
        str: Complete text content of the PDF
    """
    documents = read_pdf_documents(document_path)
    return "\n\n".join([doc.page_content for doc in documents]) 



if __name__ == "__main__":
    pdf_path = "docs/employee_handbook.pdf"
    print(f"Reading PDF from: {pdf_path}")
    documents = read_pdf_documents(pdf_path)
    print(f"Successfully loaded {len(documents)} pages")
    if documents:
        print(f"First page preview: {documents[0].page_content[:200]}...")

    # Test content function
    content = read_pdf_content(pdf_path)
    print(f"Total content length: {len(content)} characters")

