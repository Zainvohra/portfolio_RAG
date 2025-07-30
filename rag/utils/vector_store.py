import os
from typing import List, Optional

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from .embeddings import EmbeddingManager
from .text_chunker import chunk_pdf_documents


class VectorStoreManager:
    """Manages FAISS vector store operations."""
    
    def __init__(self, embedding_manager: Optional[EmbeddingManager] = None,
                 vectorstore_dir_path: str = "rag\\vectorstore"):
                # vectorstore_dir_path: str = "rag/vectorstore"):
        """
        Initialize the vector store manager.
        
        Args:
            embedding_manager (Optional[EmbeddingManager]): Embedding manager instance
            vectorstore_dir_path (str): Directory path for vectorstore files
        """
        self.vectorstore_dir_path = vectorstore_dir_path
        self.embedding_manager = embedding_manager or EmbeddingManager()
        self.vectorstore: Optional[FAISS] = None

    
    def create_vectorstore_from_chunks(self, chunks: List[Document]) -> FAISS:
        """
        Create a FAISS vectorstore from document chunks.
        
        Args:
            chunks (List[Document]): List of document chunks
            
        Returns:
            FAISS: Created vectorstore
        """
        texts = [chunk.page_content for chunk in chunks]
        self.vectorstore = FAISS.from_texts(
            texts,
            self.embedding_manager.embedding_model
        )
        return self.vectorstore
    
    def create_vectorstore_from_texts(self, texts: List[str]) -> FAISS:
        """
        Create a FAISS vectorstore from text list.
        
        Args:
            texts (List[str]): List of texts
            
        Returns:
            FAISS: Created vectorstore
        """
        self.vectorstore = FAISS.from_texts(
            texts,
            self.embedding_manager.embedding_model
        )
        return self.vectorstore
    
    def save_vectorstore(self, index_name: str = "index") -> None:
        """
        Save the vectorstore to disk.
        
        Args:
            index_name (str):
        """
        if self.vectorstore is None:
            raise ValueError("No vectorstore to save. Create a vectorstore first.")
        
        # Create directory if it doesn't exist
        os.makedirs(self.vectorstore_dir_path, exist_ok=True)
        self.vectorstore.save_local(folder_path=self.vectorstore_dir_path,
                                    index_name=index_name)
    
    def load_vectorstore(self, index_name: str = "index") -> Optional[FAISS]:
        """
        Load a vectorstore from disk.
        
        Args:
            index_name (str): Name of the index
            
        Returns:
            Optional[FAISS]: Loaded vectorstore or None if loading fails
        """
        try:
            index_path = os.path.join(self.vectorstore_dir_path, f"{index_name}.faiss")
            if os.path.exists(index_path):
                self.vectorstore = FAISS.load_local(
                    folder_path=self.vectorstore_dir_path,
                    embeddings=self.embedding_manager.embedding_model,
                    index_name=index_name,
                    allow_dangerous_deserialization=True
                )
                return self.vectorstore
            else:
                print(f"Vectorstore path {index_path} does not exist.")
                return None
        except Exception as e:
            print(f"Error loading vectorstore: {e}")
            return None

    
    def semantic_search(self, query: str, k: int = 3) -> List[Document]:
        """
        Perform semantic search on the vectorstore.
        
        Args:
            query (str): Search query
            k (int): Number of results to return
            
        Returns:
            List[Document]: Search results
        """
        if self.vectorstore is None:
            raise ValueError("No vectorstore available. Create or load a vectorstore first.")
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def semantic_search_by_vector(self, query_embedding: List[float], k: int = 3) -> List[Document]:
        """
        Perform semantic search using a query embedding vector.
        
        Args:
            query_embedding (List[float]): Query embedding vector
            k (int): Number of results to return
            
        Returns:
            List[Document]: Search results
        """
        if self.vectorstore is None:
            raise ValueError("No vectorstore available. Create or load a vectorstore first.")
        
        return self.vectorstore.similarity_search_by_vector(query_embedding, k=k)

if __name__ == "__main__":
    print("VectorStoreManager Example Usage")
    print("=" * 50)

    # Create vector store manager
    vs_manager = VectorStoreManager()

    # Process PDF and create chunks
    # chunks = chunk_pdf_documents("docs/employee_handbook.pdf")
    # vs_manager.create_vectorstore_from_chunks(chunks)
    # vs_manager.save_vectorstore("employee_handbook")

    # Load vectorstore if
    vs_manager.load_vectorstore("employee_handbook")

    # Perform semantic search
    query = "What is the company's policy on remote work?"
    results = vs_manager.semantic_search(query, k=3)

    print(f"Search results for '{query}':")
    for i, result in enumerate(results):
        print(f"{i + 1}. {result.page_content}...")

