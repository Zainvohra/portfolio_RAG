import os
import openai
import math
from typing import List, Dict, Any, Optional, Union
import asyncio
from dataclasses import dataclass
import json
import hashlib

# Add sentence-transformers import
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


@dataclass
class EmbeddingResult:
    """Represents an embedding result with metadata."""
    text: str
    embedding: List[float]
    model: str
    token_count: int
    text_hash: str
    metadata: Dict[str, Any]


class SentenceTransformerEmbeddingManager:
    """Manages text embeddings using Sentence Transformers (local, free)."""
    
    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 cache_embeddings: bool = True,
                 device: Optional[str] = None):
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers")
        
        self.model_name = model_name
        self.cache_embeddings = cache_embeddings
        self.embedding_cache: Dict[str, EmbeddingResult] = {}
        self.name = "sentence_transformer_embedding_manager"
        self.description = "Generate and manage text embeddings using Sentence Transformers"
        
        # Initialize the model
        print(f"🔄 Loading Sentence Transformer model: {model_name}")
        self.model = SentenceTransformer(model_name, device=device)
        print(f"✅ Model loaded successfully. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def _get_text_hash(self, text: str) -> str:
        """Generate a hash for the text to use as cache key."""
        return hashlib.md5(text.encode()).hexdigest()
    
    async def generate_embedding(self, text: str, metadata: Optional[Dict] = None) -> EmbeddingResult:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            metadata: Additional metadata to store with embedding
            
        Returns:
            EmbeddingResult object
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        text = text.strip()
        text_hash = self._get_text_hash(text)
        metadata = metadata or {}
        
        # Check cache first
        if self.cache_embeddings and text_hash in self.embedding_cache:
            cached_result = self.embedding_cache[text_hash]
            # Update metadata if provided
            if metadata:
                cached_result.metadata.update(metadata)
            return cached_result
        
        try:
            # Generate embedding using Sentence Transformers
            embedding = await asyncio.to_thread(self.model.encode, text)
            
            # Convert to list if it's a numpy array
            if hasattr(embedding, 'tolist'):
                embedding = embedding.tolist()
            
            result = EmbeddingResult(
                text=text,
                embedding=embedding,
                model=self.model_name,
                token_count=len(text.split()),  # Approximate token count
                text_hash=text_hash,
                metadata=metadata
            )
            
            # Cache the result
            if self.cache_embeddings:
                self.embedding_cache[text_hash] = result
            
            return result
            
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")
    
    async def generate_embeddings_batch(self, 
                                       texts: List[str], 
                                       metadata_list: Optional[List[Dict]] = None,
                                       batch_size: int = 100) -> List[EmbeddingResult]:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to embed
            metadata_list: List of metadata dictionaries (optional)
            batch_size: Batch size for processing
            
        Returns:
            List of EmbeddingResult objects
        """
        if not texts:
            return []
        
        metadata_list = metadata_list or [{}] * len(texts)
        results = []
        
        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_metadata = metadata_list[i:i + batch_size]
            
            try:
                # Generate embeddings for the batch
                embeddings = await asyncio.to_thread(self.model.encode, batch_texts)
                
                # Convert to list if it's a numpy array
                if hasattr(embeddings, 'tolist'):
                    embeddings = embeddings.tolist()
                
                # Create EmbeddingResult objects
                for j, (text, embedding) in enumerate(zip(batch_texts, embeddings)):
                    text_hash = self._get_text_hash(text)
                    
                    result = EmbeddingResult(
                        text=text,
                        embedding=embedding,
                        model=self.model_name,
                        token_count=len(text.split()),
                        text_hash=text_hash,
                        metadata=batch_metadata[j]
                    )
                    
                    # Cache the result
                    if self.cache_embeddings:
                        self.embedding_cache[text_hash] = result
                    
                    results.append(result)
                    
            except Exception as e:
                raise Exception(f"Error generating batch embeddings: {str(e)}")
        
        return results
    
    def cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        if len(embedding1) != len(embedding2):
            raise ValueError("Embeddings must have the same dimension")
        
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        magnitude1 = math.sqrt(sum(a * a for a in embedding1))
        magnitude2 = math.sqrt(sum(a * a for a in embedding2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def find_most_similar(self, 
                         query_embedding: List[float], 
                         embeddings: List[EmbeddingResult], 
                         top_k: int = 5) -> List[tuple]:
        """
        Find the most similar embeddings to the query embedding.
        
        Args:
            query_embedding: Query embedding vector
            embeddings: List of EmbeddingResult objects to search through
            top_k: Number of top results to return
            
        Returns:
            List of tuples (EmbeddingResult, similarity_score)
        """
        similarities = []
        
        for embedding_result in embeddings:
            similarity = self.cosine_similarity(query_embedding, embedding_result.embedding)
            similarities.append((embedding_result, similarity))
        
        # Sort by similarity (descending) and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    async def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a search query."""
        result = await self.generate_embedding(query)
        return result.embedding
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the embedding cache."""
        return {
            "cache_size": len(self.embedding_cache),
            "model_name": self.model_name,
            "embedding_dimension": self.model.get_sentence_embedding_dimension()
        }
    
    def save_cache(self, file_path: str) -> None:
        """Save the embedding cache to a file."""
        cache_data = {}
        for text_hash, result in self.embedding_cache.items():
            cache_data[text_hash] = {
                "text": result.text,
                "embedding": result.embedding,
                "model": result.model,
                "token_count": result.token_count,
                "metadata": result.metadata
            }
        
        with open(file_path, 'w') as f:
            json.dump(cache_data, f)
    
    def load_cache(self, file_path: str) -> None:
        """Load the embedding cache from a file."""
        if not os.path.exists(file_path):
            return
        
        with open(file_path, 'r') as f:
            cache_data = json.load(f)
        
        for text_hash, data in cache_data.items():
            result = EmbeddingResult(
                text=data["text"],
                embedding=data["embedding"],
                model=data["model"],
                token_count=data["token_count"],
                text_hash=text_hash,
                metadata=data["metadata"]
            )
            self.embedding_cache[text_hash] = result


class EmbeddingManager:
    """Manages text embeddings using OpenAI's embedding models."""
    
    def __init__(self, 
                 model: str = "text-embedding-3-small",
                 api_key: Optional[str] = None,
                 cache_embeddings: bool = True):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.cache_embeddings = cache_embeddings
        self.embedding_cache: Dict[str, EmbeddingResult] = {}
        self.name = "embedding_manager"
        self.description = "Generate and manage text embeddings for RAG"
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
    
    def _get_text_hash(self, text: str) -> str:
        """Generate a hash for the text to use as cache key."""
        return hashlib.md5(text.encode()).hexdigest()
    
    async def generate_embedding(self, text: str, metadata: Optional[Dict] = None) -> EmbeddingResult:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            metadata: Additional metadata to store with embedding
            
        Returns:
            EmbeddingResult object
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        text = text.strip()
        text_hash = self._get_text_hash(text)
        metadata = metadata or {}
        
        # Check cache first
        if self.cache_embeddings and text_hash in self.embedding_cache:
            cached_result = self.embedding_cache[text_hash]
            # Update metadata if provided
            if metadata:
                cached_result.metadata.update(metadata)
            return cached_result
        
        try:
            # Generate embedding using OpenAI API
            response = await asyncio.to_thread(
                openai.embeddings.create,
                input=text,
                model=self.model
            )
            
            embedding = response.data[0].embedding
            token_count = response.usage.total_tokens
            
            result = EmbeddingResult(
                text=text,
                embedding=embedding,
                model=self.model,
                token_count=token_count,
                text_hash=text_hash,
                metadata=metadata
            )
            
            # Cache the result
            if self.cache_embeddings:
                self.embedding_cache[text_hash] = result
            
            return result
            
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")
    
    async def generate_embeddings_batch(self, 
                                       texts: List[str], 
                                       metadata_list: Optional[List[Dict]] = None,
                                       batch_size: int = 100) -> List[EmbeddingResult]:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to embed
            metadata_list: List of metadata dicts (same length as texts)
            batch_size: Number of texts to process in each batch
            
        Returns:
            List of EmbeddingResult objects
        """
        if not texts:
            return []
        
        if metadata_list and len(metadata_list) != len(texts):
            raise ValueError("metadata_list must have same length as texts")
        
        results = []
        
        # Process texts in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_metadata = metadata_list[i:i + batch_size] if metadata_list else [{}] * len(batch_texts)
            
            # Check cache for each text in batch
            uncached_texts = []
            uncached_metadata = []
            uncached_indices = []
            
            batch_results = [None] * len(batch_texts)
            
            for j, (text, meta) in enumerate(zip(batch_texts, batch_metadata)):
                text = text.strip()
                text_hash = self._get_text_hash(text)
                
                if self.cache_embeddings and text_hash in self.embedding_cache:
                    cached_result = self.embedding_cache[text_hash]
                    if meta:
                        cached_result.metadata.update(meta)
                    batch_results[j] = cached_result
                else:
                    uncached_texts.append(text)
                    uncached_metadata.append(meta)
                    uncached_indices.append(j)
            
            # Generate embeddings for uncached texts
            if uncached_texts:
                try:
                    response = await asyncio.to_thread(
                        openai.embeddings.create,
                        input=uncached_texts,
                        model=self.model
                    )
                    
                    for k, (text, meta, original_idx) in enumerate(zip(uncached_texts, uncached_metadata, uncached_indices)):
                        embedding = response.data[k].embedding
                        text_hash = self._get_text_hash(text)
                        
                        result = EmbeddingResult(
                            text=text,
                            embedding=embedding,
                            model=self.model,
                            token_count=response.usage.total_tokens // len(uncached_texts),  # Approximate
                            text_hash=text_hash,
                            metadata=meta
                        )
                        
                        batch_results[original_idx] = result
                        
                        # Cache the result
                        if self.cache_embeddings:
                            self.embedding_cache[text_hash] = result
                
                except Exception as e:
                    raise Exception(f"Error generating batch embeddings: {str(e)}")
            
            results.extend([r for r in batch_results if r is not None])
        
        return results
    
    def cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in embedding1))
        magnitude2 = math.sqrt(sum(a * a for a in embedding2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def find_most_similar(self, 
                         query_embedding: List[float], 
                         embeddings: List[EmbeddingResult], 
                         top_k: int = 5) -> List[tuple]:
        """
        Find most similar embeddings to a query embedding.
        
        Args:
            query_embedding: Query embedding vector
            embeddings: List of EmbeddingResult objects to search
            top_k: Number of top results to return
            
        Returns:
            List of tuples (EmbeddingResult, similarity_score)
        """
        if not embeddings:
            return []
        
        similarities = []
        for embedding_result in embeddings:
            similarity = self.cosine_similarity(query_embedding, embedding_result.embedding)
            similarities.append((embedding_result, similarity))
        
        # Sort by similarity (descending) and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    async def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a query string.
        
        Args:
            query: Query text to embed
            
        Returns:
            Embedding vector
        """
        result = await self.generate_embedding(query, {"type": "query"})
        return result.embedding
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the embedding cache."""
        total_embeddings = len(self.embedding_cache)
        total_tokens = sum(result.token_count for result in self.embedding_cache.values())
        
        models_used = set(result.model for result in self.embedding_cache.values())
        
        return {
            "total_cached_embeddings": total_embeddings,
            "total_tokens_used": total_tokens,
            "models_used": list(models_used),
            "cache_enabled": self.cache_embeddings,
            "current_model": self.model
        }
    
    def save_cache(self, file_path: str) -> None:
        """Save embedding cache to file."""
        cache_data = {}
        for text_hash, result in self.embedding_cache.items():
            cache_data[text_hash] = {
                "text": result.text,
                "embedding": result.embedding,
                "model": result.model,
                "token_count": result.token_count,
                "text_hash": result.text_hash,
                "metadata": result.metadata
            }
        
        with open(file_path, 'w') as f:
            json.dump(cache_data, f, indent=2)
    
    def load_cache(self, file_path: str) -> None:
        """Load embedding cache from file."""
        try:
            with open(file_path, 'r') as f:
                cache_data = json.load(f)
            
            self.embedding_cache = {}
            for text_hash, data in cache_data.items():
                result = EmbeddingResult(
                    text=data["text"],
                    embedding=data["embedding"],
                    model=data["model"],
                    token_count=data["token_count"],
                    text_hash=data["text_hash"],
                    metadata=data["metadata"]
                )
                self.embedding_cache[text_hash] = result
                
        except FileNotFoundError:
            print(f"Cache file {file_path} not found. Starting with empty cache.")
        except Exception as e:
            print(f"Error loading cache: {e}. Starting with empty cache.")


# Create a global instance with Sentence Transformers as default
try:
    embedding_manager = SentenceTransformerEmbeddingManager(model_name="all-MiniLM-L6-v2")
except ImportError:
    embedding_manager = EmbeddingManager() 