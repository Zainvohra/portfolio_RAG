import asyncio
import os
from typing import Dict, Any
from agents import function_tool

# Import our RAG components from rag_utils
from utils import TextChunker, EmbeddingManager, SentenceTransformerEmbeddingManager, AdvancedVectorStore, PDFReader

# Global instances for tool functions
text_chunker = TextChunker(chunk_size=1000, overlap_size=200)

# Use Sentence Transformers instead of OpenAI (free, local, no API limits)
try:
    embedding_manager = SentenceTransformerEmbeddingManager(model_name="all-MiniLM-L6-v2")
    print("✅ Using Sentence Transformers for embeddings (free, local)")
except ImportError:
    print("⚠️  Sentence Transformers not available, falling back to OpenAI")
    embedding_manager = EmbeddingManager()

vector_store = AdvancedVectorStore(embedding_manager)
pdf_reader = PDFReader()

def run_async_safe(coro):
    """Safely run async coroutine in sync context."""
    try:
        # Check if we're already in an event loop
        loop = asyncio.get_running_loop()
        # If we're in a loop, we need to create a task
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        # No running loop, safe to use asyncio.run
        return asyncio.run(coro)

@function_tool
def read_pdf_tool(file_path: str, chunk_strategy: str = "semantic") -> Dict[str, Any]:
    """
    Read and process a PDF file for RAG system.
    
    Args:
        file_path: Path to the PDF file to process
        chunk_strategy: Chunking strategy - 'recursive', 'sentence', 'paragraph', or 'semantic'
    """
    print(f"🔧 TOOL INVOKED: read_pdf_tool(file_path='{file_path}', chunk_strategy='{chunk_strategy}')")
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File not found: {file_path}",
                "file_path": file_path
            }
        
        # Read PDF content
        pdf_content = pdf_reader.read_pdf(file_path)
        if not pdf_content["success"]:
            return pdf_content
        
        # Process the content synchronously
        result = _process_pdf_content_sync(
            pdf_content["text"], 
            file_path, 
            chunk_strategy,
            pdf_content.get("metadata", {})
        )
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing PDF: {str(e)}",
            "file_path": file_path
        }

def _process_pdf_content_sync(text: str, file_path: str, chunk_strategy: str, metadata: Dict) -> Dict[str, Any]:
    """Process PDF content into chunks and add to vector store synchronously."""
    try:
        # Create document ID from file path
        document_id = os.path.splitext(os.path.basename(file_path))[0]
        
        # Chunk the text
        chunks = text_chunker.chunk_text(
            text, 
            strategy=chunk_strategy, 
            metadata={"source_file": file_path, **metadata}
        )
        
        if not chunks:
            return {
                "success": False,
                "error": "No chunks generated from PDF content",
                "document_id": document_id,
                "chunks_added": 0
            }
        
        # Add chunks to vector store synchronously
        result = run_async_safe(vector_store.add_document(
            document_id=document_id,
            chunks=chunks,
            document_metadata=metadata
        ))
        
        # Get chunking statistics
        chunk_stats = text_chunker.get_chunk_statistics(chunks)
        
        return {
            "success": True,
            "document_id": document_id,
            "chunks_added": len(chunks),
            "chunking_strategy": chunk_strategy,
            "chunk_statistics": chunk_stats,
            "file_path": file_path,
            "metadata": metadata
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing PDF content: {str(e)}",
            "document_id": document_id,
            "chunks_added": 0
        }

@function_tool
def search_documents_tool(query: str, top_k: int = 5, min_similarity: float = 0.3) -> Dict[str, Any]:
    """
    Search through processed documents for relevant content using basic vector similarity.
    
    Args:
        query: The search query to find relevant document chunks
        top_k: Maximum number of results to return (default: 5)
        min_similarity: Minimum similarity threshold for results (default: 0.3)
    """
    print(f"🔧 TOOL INVOKED: search_documents_tool(query='{query}', top_k={top_k}, min_similarity={min_similarity})")
    
    try:
        # Perform basic search (no query expansion or re-ranking)
        results = run_async_safe(vector_store.search(
            query=query,
            top_k=top_k,
            min_similarity=min_similarity
        ))
        
        # Format results for better readability
        formatted_results = []
        for result in results:
            formatted_results.append({
                "content": result["content"],
                "similarity": round(result["similarity"], 3),
                "source": result["metadata"].get("source_file", "Unknown"),
                "chunk_id": result["chunk_id"]
            })
        
        return {
            "success": True,
            "query": query,
            "results_count": len(results),
            "results": formatted_results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching documents: {str(e)}",
            "query": query,
            "results": []
        }

@function_tool
def semantic_search_tool(query: str, 
                        top_k: int = 5, 
                        min_similarity: float = 0.3,
                        use_query_expansion: bool = True,
                        use_reranking: bool = True) -> Dict[str, Any]:
    """
    Advanced semantic search with query expansion and re-ranking for better results.
    
    Args:
        query: The search query to find relevant document chunks
        top_k: Maximum number of results to return (default: 5)
        min_similarity: Minimum similarity threshold for results (default: 0.3)
        use_query_expansion: Whether to expand query for better coverage (default: True)
        use_reranking: Whether to apply semantic re-ranking (default: True)
    """
    print(f"🔧 TOOL INVOKED: semantic_search_tool(query='{query}', top_k={top_k}, advanced=True)")
    
    try:
        # Perform advanced semantic search
        results = run_async_safe(vector_store.semantic_search(
            query=query,
            top_k=top_k,
            min_similarity=min_similarity,
            use_query_expansion=use_query_expansion,
            use_reranking=use_reranking
        ))
        
        # Format results with additional metadata
        formatted_results = []
        for result in results:
            formatted_result = {
                "content": result["content"],
                "similarity": round(result["similarity"], 3),
                "source": result["metadata"].get("source_file", "Unknown"),
                "chunk_id": result["chunk_id"],
                "document_id": result["document_id"]
            }
            
            # Add re-ranking score if available
            if "rerank_score" in result:
                formatted_result["rerank_score"] = round(result["rerank_score"], 3)
            
            # Add query variant if available
            if "query_variant" in result:
                formatted_result["matched_query"] = result["query_variant"]
            
            formatted_results.append(formatted_result)
        
        return {
            "success": True,
            "query": query,
            "results_count": len(results),
            "results": formatted_results,
            "search_type": "advanced_semantic",
            "features_used": {
                "query_expansion": use_query_expansion,
                "reranking": use_reranking,
                "diversification": True
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error in semantic search: {str(e)}",
            "query": query,
            "results": []
        }

@function_tool
def ask_question_tool(question: str, 
                     top_k: int = 5, 
                     min_similarity: float = 0.3,
                     use_advanced_search: bool = True) -> Dict[str, Any]:
    """
    Answer a question using RAG - search documents and provide context for answering.
    
    Args:
        question: The question to answer using document content
        top_k: Number of document chunks to retrieve for context (default: 5)
        min_similarity: Minimum similarity threshold for relevant chunks (default: 0.3)
        use_advanced_search: Whether to use advanced semantic search features (default: True)
    """
    print(f"🔧 TOOL INVOKED: ask_question_tool(question='{question}', advanced={use_advanced_search})")
    
    try:
        # Choose search method based on advanced flag
        if use_advanced_search:
            search_results = run_async_safe(vector_store.semantic_search(
                query=question,
                top_k=top_k,
                min_similarity=min_similarity,
                use_query_expansion=True,
                use_reranking=True
            ))
        else:
            search_results = run_async_safe(vector_store.search(
                query=question,
                top_k=top_k,
                min_similarity=min_similarity
            ))
        
        if not search_results:
            return {
                "success": True,
                "question": question,
                "answer": "I couldn't find any relevant information in the processed documents to answer your question. You may need to process more documents first.",
                "context": [],
                "context_text": ""
            }
        
        # Build context from search results
        context_chunks = []
        for result in search_results:
            context_chunk = {
                "content": result["content"],
                "similarity": round(result["similarity"], 3),
                "source": result["metadata"].get("source_file", "Unknown"),
                "chunk_id": result["chunk_id"]
            }
            
            # Include re-ranking score if available
            if "rerank_score" in result:
                context_chunk["rerank_score"] = round(result["rerank_score"], 3)
                
            context_chunks.append(context_chunk)
        
        # Create context string for the LLM
        context_text = "\n\n".join([
            f"[Source: {chunk['source']}, Similarity: {chunk['similarity']:.3f}]\n{chunk['content']}"
            for chunk in context_chunks
        ])
        
        # Calculate average similarity
        avg_similarity = sum(r['similarity'] for r in context_chunks) / len(context_chunks)
        
        return {
            "success": True,
            "question": question,
            "context": context_chunks,
            "context_text": context_text,
            "average_similarity": round(avg_similarity, 3),
            "sources_found": len(set(chunk['source'] for chunk in context_chunks)),
            "search_method": "advanced_semantic" if use_advanced_search else "basic_vector"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error answering question: {str(e)}",
            "question": question,
            "context": [],
            "context_text": ""
        }

@function_tool
def get_document_stats_tool() -> Dict[str, Any]:
    """
    Get statistics about the processed documents in the RAG system.
    """
    print(f"🔧 TOOL INVOKED: get_document_stats_tool()")
    
    try:
        stats = vector_store.get_stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting document stats: {str(e)}",
            "stats": {}
        }

@function_tool
def list_documents_tool() -> Dict[str, Any]:
    """
    List all processed documents in the RAG system.
    """
    print(f"🔧 TOOL INVOKED: list_documents_tool()")
    
    try:
        stats = vector_store.get_stats()
        return {
            "success": True,
            "documents": stats.get("document_ids", []),
            "total_documents": stats.get("total_documents", 0),
            "total_chunks": stats.get("total_chunks", 0)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error listing documents: {str(e)}",
            "documents": [],
            "total_documents": 0,
            "total_chunks": 0
        } 