from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import json
import os
from .text_chunker import TextChunk
from .embeddings import EmbeddingResult, EmbeddingManager, SentenceTransformerEmbeddingManager


@dataclass
class DocumentChunk:
    """Represents a document chunk with its embedding."""
    chunk: TextChunk
    embedding_result: EmbeddingResult
    document_id: str
    document_metadata: Dict[str, Any]


class AdvancedVectorStore:
    """Advanced in-memory vector store with enhanced retrieval capabilities."""
    
    def __init__(self, embedding_manager: Optional[EmbeddingManager] = None):
        if embedding_manager is None:
            # Use Sentence Transformers instead of OpenAI (free, local, no API limits)
            try:
                self.embedding_manager = SentenceTransformerEmbeddingManager(model_name="all-MiniLM-L6-v2")
            except ImportError:
                self.embedding_manager = EmbeddingManager()
        else:
            self.embedding_manager = embedding_manager
        self.documents: Dict[str, DocumentChunk] = {}  # chunk_id -> DocumentChunk
        self.document_index: Dict[str, List[str]] = {}  # doc_id -> list of chunk_ids
        self.name = "advanced_vector_store"
        self.description = "Advanced vector store with semantic retrieval and re-ranking"
    
    async def add_document(self, 
                          document_id: str,
                          chunks: List[TextChunk], 
                          document_metadata: Optional[Dict] = None,
                          batch_size: int = 50) -> Dict[str, Any]:
        """
        Add a document's chunks to the vector store.
        
        Args:
            document_id: Unique identifier for the document
            chunks: List of TextChunk objects
            document_metadata: Metadata about the document
            batch_size: Batch size for embedding generation
            
        Returns:
            Result dictionary with processing statistics
        """
        if not chunks:
            return {
                "success": False,
                "error": "No chunks provided",
                "chunks_added": 0,
                "document_id": document_id
            }
        
        document_metadata = document_metadata or {}
        
        try:
            # Prepare texts and metadata for embedding
            texts = [chunk.content for chunk in chunks]
            metadata_list = []
            
            for chunk in chunks:
                chunk_metadata = {
                    "chunk_id": chunk.chunk_id,
                    "document_id": document_id,
                    "start_index": chunk.start_index,
                    "end_index": chunk.end_index,
                    "word_count": chunk.word_count,
                    **chunk.metadata,
                    **document_metadata
                }
                metadata_list.append(chunk_metadata)
            
            # Generate embeddings in batches
            embedding_results = await self.embedding_manager.generate_embeddings_batch(
                texts, metadata_list, batch_size
            )
            
            # Store document chunks
            chunk_ids = []
            for chunk, embedding_result in zip(chunks, embedding_results):
                doc_chunk = DocumentChunk(
                    chunk=chunk,
                    embedding_result=embedding_result,
                    document_id=document_id,
                    document_metadata=document_metadata
                )
                
                self.documents[chunk.chunk_id] = doc_chunk
                chunk_ids.append(chunk.chunk_id)
            
            # Update document index
            if document_id in self.document_index:
                self.document_index[document_id].extend(chunk_ids)
            else:
                self.document_index[document_id] = chunk_ids
            
            return {
                "success": True,
                "chunks_added": len(chunks),
                "document_id": document_id,
                "chunk_ids": chunk_ids,
                "total_chunks_in_document": len(self.document_index[document_id])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error adding document: {str(e)}",
                "chunks_added": 0,
                "document_id": document_id
            }
    
    async def semantic_search(self, 
                             query: str, 
                             top_k: int = 5, 
                             document_ids: Optional[List[str]] = None,
                             min_similarity: float = 0.0,
                             use_query_expansion: bool = True,
                             use_reranking: bool = True,
                             diversity_threshold: float = 0.8) -> List[Dict[str, Any]]:
        """
        Advanced semantic search with query expansion and re-ranking.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            document_ids: Optional list of document IDs to search within
            min_similarity: Minimum similarity threshold
            use_query_expansion: Whether to expand the query for better coverage
            use_reranking: Whether to apply semantic re-ranking
            diversity_threshold: Threshold for result diversification
            
        Returns:
            List of search results with chunks and metadata
        """
        if not query.strip():
            return []
        
        if not self.documents:
            return []
        
        try:
            # Step 1: Query expansion for better semantic coverage
            queries = [query]
            if use_query_expansion:
                expanded_queries = await self._expand_query(query)
                queries.extend(expanded_queries)
            
            # Step 2: Generate embeddings for all queries
            all_results = []
            for q in queries:
                query_embedding = await self.embedding_manager.embed_query(q)
                
                # Filter chunks by document IDs if specified
                search_chunks = []
                if document_ids:
                    for doc_id in document_ids:
                        if doc_id in self.document_index:
                            for chunk_id in self.document_index[doc_id]:
                                if chunk_id in self.documents:
                                    search_chunks.append(self.documents[chunk_id])
                else:
                    search_chunks = list(self.documents.values())
                
                if not search_chunks:
                    continue
                
                # Extract embeddings for similarity calculation
                embeddings = [chunk.embedding_result for chunk in search_chunks]
                
                # Find most similar chunks for this query
                similar_results = self.embedding_manager.find_most_similar(
                    query_embedding, embeddings, top_k * 2  # Get more for re-ranking
                )
                
                # Convert to results format
                for embedding_result, similarity in similar_results:
                    if similarity >= min_similarity:
                        # Find the corresponding document chunk
                        doc_chunk = None
                        for chunk in search_chunks:
                            if chunk.embedding_result.text_hash == embedding_result.text_hash:
                                doc_chunk = chunk
                                break
                        
                        if doc_chunk:
                            result = {
                                "chunk_id": doc_chunk.chunk.chunk_id,
                                "document_id": doc_chunk.document_id,
                                "content": doc_chunk.chunk.content,
                                "similarity": similarity,
                                "query_variant": q,
                                "metadata": {
                                    **doc_chunk.chunk.metadata,
                                    **doc_chunk.document_metadata,
                                    "word_count": doc_chunk.chunk.word_count,
                                    "start_index": doc_chunk.chunk.start_index,
                                    "end_index": doc_chunk.chunk.end_index
                                }
                            }
                            all_results.append(result)
            
            # Step 3: Deduplicate and merge results
            unique_results = self._deduplicate_results(all_results)
            
            # Step 4: Re-ranking based on multiple factors
            if use_reranking and len(unique_results) > 1:
                unique_results = await self._rerank_results(query, unique_results)
            
            # Step 5: Diversify results to avoid redundancy
            final_results = self._diversify_results(unique_results, diversity_threshold, top_k)
            
            return final_results[:top_k]
            
        except Exception as e:
            print(f"Error during semantic search: {str(e)}")
            return []
    
    async def _expand_query(self, query: str) -> List[str]:
        """
        Expand query with related terms and reformulations.
        Simple implementation - can be enhanced with more sophisticated NLP.
        """
        expanded_queries = []
        
        # Add question variations
        if "?" not in query:
            expanded_queries.append(f"What is {query}?")
            expanded_queries.append(f"How does {query} work?")
        
        # Add different phrasings
        words = query.split()
        if len(words) > 1:
            # Reorder words for different semantic emphasis
            expanded_queries.append(" ".join(reversed(words)))
        
        return expanded_queries[:2]  # Limit to avoid too many queries
    
    async def _rerank_results(self, query: str, results: List[Dict]) -> List[Dict]:
        """
        Re-rank results based on multiple semantic factors.
        """
        if len(results) <= 1:
            return results
        
        # Calculate additional ranking factors
        for result in results:
            content = result["content"]
            
            # Factor 1: Query term coverage (semantic)
            query_embedding = await self.embedding_manager.embed_query(query)
            content_embedding = await self.embedding_manager.embed_query(content)
            semantic_relevance = self.embedding_manager.cosine_similarity(query_embedding, content_embedding)
            
            # Factor 2: Content quality (length, completeness)
            content_quality = min(1.0, len(content.split()) / 100)  # Normalize by 100 words
            
            # Factor 3: Position boost for document structure
            position_boost = 1.0 - (result["metadata"].get("start_index", 0) / 10000)  # Small boost for earlier content
            position_boost = max(0.8, position_boost)  # Don't penalize too much
            
            # Combined score
            result["rerank_score"] = (
                result["similarity"] * 0.6 +  # Original similarity
                semantic_relevance * 0.3 +     # Semantic relevance
                content_quality * 0.1           # Content quality
            ) * position_boost
        
        # Sort by rerank score
        results.sort(key=lambda x: x["rerank_score"], reverse=True)
        return results
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate results based on chunk_id."""
        seen_chunks = set()
        unique_results = []
        
        for result in results:
            chunk_id = result["chunk_id"]
            if chunk_id not in seen_chunks:
                seen_chunks.add(chunk_id)
                unique_results.append(result)
        
        return unique_results
    
    def _diversify_results(self, results: List[Dict], threshold: float, max_results: int) -> List[Dict]:
        """
        Diversify results to avoid semantic redundancy.
        """
        if len(results) <= max_results:
            return results
        
        diverse_results = [results[0]]  # Always include the top result
        
        for result in results[1:]:
            if len(diverse_results) >= max_results:
                break
                
            # Check if this result is sufficiently different from existing ones
            is_diverse = True
            for existing in diverse_results:
                if result["similarity"] > threshold and existing["similarity"] > threshold:
                    # Check content similarity (simple word overlap)
                    words1 = set(result["content"].lower().split())
                    words2 = set(existing["content"].lower().split())
                    overlap = len(words1.intersection(words2)) / max(len(words1), len(words2), 1)
                    
                    if overlap > (1 - threshold):  # Too similar
                        is_diverse = False
                        break
            
            if is_diverse:
                diverse_results.append(result)
        
        return diverse_results
    
    # Keep the original search method for backward compatibility
    async def search(self, 
                    query: str, 
                    top_k: int = 5, 
                    document_ids: Optional[List[str]] = None,
                    min_similarity: float = 0.0) -> List[Dict[str, Any]]:
        """
        Standard search method (calls semantic_search with default settings).
        """
        return await self.semantic_search(
            query=query,
            top_k=top_k,
            document_ids=document_ids,
            min_similarity=min_similarity,
            use_query_expansion=False,
            use_reranking=False
        )
    
    def get_document_chunks(self, document_id: str) -> List[DocumentChunk]:
        """Get all chunks for a specific document."""
        if document_id not in self.document_index:
            return []
        
        chunks = []
        for chunk_id in self.document_index[document_id]:
            if chunk_id in self.documents:
                chunks.append(self.documents[chunk_id])
        
        return chunks
    
    def remove_document(self, document_id: str) -> Dict[str, Any]:
        """Remove a document and all its chunks from the store."""
        if document_id not in self.document_index:
            return {
                "success": False,
                "error": f"Document {document_id} not found",
                "chunks_removed": 0
            }
        
        chunk_ids = self.document_index[document_id]
        chunks_removed = 0
        
        for chunk_id in chunk_ids:
            if chunk_id in self.documents:
                del self.documents[chunk_id]
                chunks_removed += 1
        
        del self.document_index[document_id]
        
        return {
            "success": True,
            "chunks_removed": chunks_removed,
            "document_id": document_id
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        total_chunks = len(self.documents)
        total_documents = len(self.document_index)
        
        # Calculate document sizes
        doc_sizes = [len(chunk_ids) for chunk_ids in self.document_index.values()]
        avg_chunks_per_doc = sum(doc_sizes) / len(doc_sizes) if doc_sizes else 0
        
        # Get embedding stats
        embedding_stats = self.embedding_manager.get_cache_stats()
        
        return {
            "total_documents": total_documents,
            "total_chunks": total_chunks,
            "avg_chunks_per_document": avg_chunks_per_doc,
            "document_ids": list(self.document_index.keys()),
            "embedding_stats": embedding_stats
        }
    
    def save_to_file(self, file_path: str) -> None:
        """Save the vector store to a file."""
        store_data = {
            "documents": {},
            "document_index": self.document_index
        }
        
        # Serialize document chunks
        for chunk_id, doc_chunk in self.documents.items():
            store_data["documents"][chunk_id] = {
                "chunk": {
                    "content": doc_chunk.chunk.content,
                    "chunk_id": doc_chunk.chunk.chunk_id,
                    "start_index": doc_chunk.chunk.start_index,
                    "end_index": doc_chunk.chunk.end_index,
                    "metadata": doc_chunk.chunk.metadata,
                    "word_count": doc_chunk.chunk.word_count
                },
                "embedding_result": {
                    "text": doc_chunk.embedding_result.text,
                    "embedding": doc_chunk.embedding_result.embedding,
                    "model": doc_chunk.embedding_result.model,
                    "token_count": doc_chunk.embedding_result.token_count,
                    "text_hash": doc_chunk.embedding_result.text_hash,
                    "metadata": doc_chunk.embedding_result.metadata
                },
                "document_id": doc_chunk.document_id,
                "document_metadata": doc_chunk.document_metadata
            }
        
        with open(file_path, 'w') as f:
            json.dump(store_data, f, indent=2)
    
    def load_from_file(self, file_path: str) -> None:
        """Load the vector store from a file."""
        try:
            with open(file_path, 'r') as f:
                store_data = json.load(f)
            
            self.documents = {}
            self.document_index = store_data.get("document_index", {})
            
            # Deserialize document chunks
            for chunk_id, data in store_data.get("documents", {}).items():
                chunk_data = data["chunk"]
                embedding_data = data["embedding_result"]
                
                # Reconstruct TextChunk
                chunk = TextChunk(
                    content=chunk_data["content"],
                    chunk_id=chunk_data["chunk_id"],
                    start_index=chunk_data["start_index"],
                    end_index=chunk_data["end_index"],
                    metadata=chunk_data["metadata"],
                    word_count=chunk_data["word_count"]
                )
                
                # Reconstruct EmbeddingResult
                embedding_result = EmbeddingResult(
                    text=embedding_data["text"],
                    embedding=embedding_data["embedding"],
                    model=embedding_data["model"],
                    token_count=embedding_data["token_count"],
                    text_hash=embedding_data["text_hash"],
                    metadata=embedding_data["metadata"]
                )
                
                # Reconstruct DocumentChunk
                doc_chunk = DocumentChunk(
                    chunk=chunk,
                    embedding_result=embedding_result,
                    document_id=data["document_id"],
                    document_metadata=data["document_metadata"]
                )
                
                self.documents[chunk_id] = doc_chunk
                
        except FileNotFoundError:
            print(f"Vector store file {file_path} not found. Starting with empty store.")
        except Exception as e:
            print(f"Error loading vector store: {e}. Starting with empty store.")


# Backward compatibility
VectorStore = AdvancedVectorStore

# Create a global instance
vector_store = AdvancedVectorStore() 