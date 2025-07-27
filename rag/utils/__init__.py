# Utils package for RAG functionality

# PDF processing functions
from .pdf_reader import read_pdf_documents, read_pdf_content

# Text chunking functions
from .text_chunker import (
    create_text_splitter,
    chunk_documents,
    chunk_pdf_documents
)

# Embedding functions and classes
from .embeddings import EmbeddingManager

# Vector store functions and classes
from .vector_store import VectorStoreManager

# Convenience functions for easier usage
def create_embedding_manager(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> EmbeddingManager:
    """
    Create an EmbeddingManager instance.
    
    Args:
        model_name (str): Name of the HuggingFace embedding model
        
    Returns:
        EmbeddingManager: Embedding manager instance
    """
    return EmbeddingManager(model_name)


def create_query_embedding(query: str, embedding_manager: EmbeddingManager = None) -> list:
    """
    Create embedding for a query using EmbeddingManager.
    
    Args:
        query (str): Text query to embed
        embedding_manager (EmbeddingManager, optional): Embedding manager instance
        
    Returns:
        list: Query embedding vector
    """
    if embedding_manager is None:
        embedding_manager = EmbeddingManager()
    return embedding_manager.create_query_embedding(query)


def create_vectorstore_from_pdf(pdf_path: str, vectorstore_dir: str = "vectorstore", 
                               chunk_size: int = 1000, chunk_overlap: int = 200) -> VectorStoreManager:
    """
    Create a vector store from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        vectorstore_dir (str): Directory to store the vectorstore
        chunk_size (int): Size of text chunks
        chunk_overlap (int): Overlap between chunks
        
    Returns:
        VectorStoreManager: Vector store manager with loaded vectorstore
    """
    # Create chunks from PDF
    chunks = chunk_pdf_documents(pdf_path, chunk_size, chunk_overlap)
    
    # Create vector store manager
    vs_manager = VectorStoreManager(vectorstore_dir_path=vectorstore_dir)
    
    # Create vectorstore from chunks
    vs_manager.create_vectorstore_from_chunks(chunks)
    
    return vs_manager


def load_or_create_vectorstore(pdf_path: str = None, index_name: str = "index", 
                             vectorstore_dir: str = "vectorstore", 
                             chunk_size: int = 1000, chunk_overlap: int = 200) -> VectorStoreManager:
    """
    Load existing vectorstore or create new one from PDF.
    
    Args:
        pdf_path (str, optional): Path to PDF file (required if creating new vectorstore)
        index_name (str): Name of the vectorstore index
        vectorstore_dir (str): Directory containing the vectorstore
        chunk_size (int): Size of text chunks (for new vectorstore)
        chunk_overlap (int): Overlap between chunks (for new vectorstore)
        
    Returns:
        VectorStoreManager: Vector store manager instance
    """
    vs_manager = VectorStoreManager(vectorstore_dir_path=vectorstore_dir)
    
    # Try to load existing vectorstore
    loaded_vs = vs_manager.load_vectorstore(index_name)
    
    if loaded_vs is None:
        if pdf_path is None:
            raise ValueError("PDF path is required when creating new vectorstore")
        print(f"Creating new vectorstore from {pdf_path}")
        chunks = chunk_pdf_documents(pdf_path, chunk_size, chunk_overlap)
        vs_manager.create_vectorstore_from_chunks(chunks)
        vs_manager.save_vectorstore(index_name)
    else:
        print(f"Loaded existing vectorstore: {index_name}")
    
    return vs_manager


__all__ = [
    # PDF processing
    'read_pdf_documents',
    'read_pdf_content',

    # Text chunking
    'create_text_splitter',
    'chunk_documents',
    'chunk_pdf_documents',

    # Embeddings
    'EmbeddingManager',
    'create_embedding_manager',
    'create_query_embedding',

    # Vector store
    'VectorStoreManager',
    'create_vectorstore_from_pdf',
    'load_or_create_vectorstore'
]