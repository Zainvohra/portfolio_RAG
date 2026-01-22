from typing import List

from langchain_huggingface import HuggingFaceEmbeddings
from singleton_decorator import singleton


@singleton
class EmbeddingManager:
    """Manages embedding operations using HuggingFace embeddings."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding manager.
        
        Args:
            model_name (str): Name of the HuggingFace embedding model
        """
        print("Initializing EmbeddingManager...")
        self.model_name = model_name
        self.embedding_model = HuggingFaceEmbeddings(model_name=model_name)
    
    def create_query_embedding(self, query: str) -> List[float]:
        """
        Create embedding for a single query.
        
        Args:
            query (str): Text query to embed
            
        Returns:
            List[float]: Query embedding vector
        """
        return self.embedding_model.embed_query(query)



if __name__ == "__main__":
    # Example usage and testing
    print("Testing EmbeddingManager...")
    
    # Test basic functionality
    embedding_manager = EmbeddingManager()
    
    # Test queries
    test_queries = [
        "Hello, world!",
        "What is the company's remote work policy?",
        "Employee benefits and vacation time"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        query_embedding = embedding_manager.create_query_embedding(query)
        print(f"Embedding dimensions: {len(query_embedding)}")
        print(f"First 5 values: {query_embedding[:5]}")
    
    print("\nEmbeddingManager test completed successfully!")
