from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from utils.pdf_reader import read_pdf_documents


def create_text_splitter(chunk_size: int = 1000, chunk_overlap: int = 200) -> RecursiveCharacterTextSplitter:
    """
    Create a RecursiveCharacterTextSplitter with specified parameters.
    
    Args:
        chunk_size (int): Maximum size of each chunk
        chunk_overlap (int): Number of characters to overlap between chunks
        
    Returns:
        RecursiveCharacterTextSplitter: Configured text splitter
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )


def chunk_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Split documents into chunks using RecursiveCharacterTextSplitter.
    
    Args:
        documents (List[Document]): List of documents to split
        chunk_size (int): Maximum size of each chunk
        chunk_overlap (int): Number of characters to overlap between chunks
        
    Returns:
        List[Document]: List of chunked documents
    """
    text_splitter = create_text_splitter(chunk_size, chunk_overlap)
    return text_splitter.split_documents(documents)


def chunk_pdf_documents(document_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Load a PDF and split it into chunks in one step.
    
    Args:
        document_path (str): Path to the PDF file
        chunk_size (int): Maximum size of each chunk
        chunk_overlap (int): Number of characters to overlap between chunks
        
    Returns:
        List[Document]: List of chunked documents
    """
    documents = read_pdf_documents(document_path)
    documents_chunks = chunk_documents(documents, chunk_size, chunk_overlap)
    return documents_chunks


if __name__ == "__main__":
    print(chunk_pdf_documents("docs/employee_handbook.pdf"))