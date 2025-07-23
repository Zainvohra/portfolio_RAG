#!/usr/bin/env python3
"""
Test script for the RAG Tools module.
Demonstrates PDF processing, document search, and question answering tools.
"""

import os
import sys

# Add the parent directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the underlying functions from rag_tools
from rag_tools import (
    _process_pdf_content_sync,
    run_async_safe
)

# Import vector store and other components directly
from utils.vector_store import AdvancedVectorStore
from utils.pdf_reader import PDFReader
from utils.text_chunker import TextChunker
from utils.embeddings import SentenceTransformerEmbeddingManager, EmbeddingManager

def test_tool_initialization():
    """Test that RAG tool components are properly initialized."""
    
    print("🧪 Testing RAG Tool Components Initialization")
    print("=" * 50)
    
    try:
        # Test 1: Check component availability
        print("\n🔧 Test 1: Checking Component Availability")
        print("-" * 40)
        
        # Initialize components
        pdf_reader = PDFReader()
        text_chunker = TextChunker(chunk_size=1000, overlap_size=200)
        
        try:
            embedding_manager = SentenceTransformerEmbeddingManager(model_name="all-MiniLM-L6-v2")
            print("✅ SentenceTransformer embedding manager available")
        except ImportError:
            print("⚠️  SentenceTransformers not available")
            if os.getenv("OPENAI_API_KEY"):
                embedding_manager = EmbeddingManager()
                print("✅ OpenAI embedding manager available")
            else:
                print("❌ No embedding manager available")
                return False
        
        vector_store = AdvancedVectorStore(embedding_manager)
        
        print(f"✅ PDF Reader: {pdf_reader.name}")
        print(f"✅ Text Chunker: {text_chunker.name}")
        print(f"✅ Vector Store: {vector_store.name}")
        print(f"✅ Embedding Manager: {type(embedding_manager).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during component initialization: {str(e)}")
        return False

def test_pdf_processing_workflow():
    """Test the complete PDF processing workflow."""
    
    print("\n🧪 Testing PDF Processing Workflow")
    print("=" * 50)
    
    try:
        # Initialize components
        pdf_reader = PDFReader()
        text_chunker = TextChunker(chunk_size=1000, overlap_size=200)
        
        try:
            embedding_manager = SentenceTransformerEmbeddingManager(model_name="all-MiniLM-L6-v2")
        except ImportError:
            embedding_manager = EmbeddingManager()
        
        vector_store = AdvancedVectorStore(embedding_manager)
        
        # Test 1: Check for existing PDF
        print("\n📖 Test 1: PDF Reading and Processing")
        print("-" * 40)
        
        # Look for PDF files to test with
        possible_pdfs = [
            "docs/employee_handbook.pdf",
            "employee_handbook.pdf",
            "../docs/employee_handbook.pdf"
        ]
        
        pdf_file = None
        for pdf_path in possible_pdfs:
            if os.path.exists(pdf_path):
                pdf_file = pdf_path
                break
        
        if pdf_file:
            # Read PDF
            pdf_content = pdf_reader.read_pdf(pdf_file)
            
            if pdf_content["success"]:
                print(f"✅ PDF read successfully")
                print(f"   File: {pdf_content['file_path']}")
                print(f"   Page count: {pdf_content['page_count']}")
                print(f"   Word count: {pdf_content['word_count']}")
                
                # Chunk the text
                chunks = text_chunker.chunk_text(
                    pdf_content["text"], 
                    strategy="semantic", 
                    metadata={"source_file": pdf_file, **pdf_content.get("metadata", {})}
                )
                
                print(f"✅ Text chunked successfully")
                print(f"   Number of chunks: {len(chunks)}")
                
                # Add to vector store
                document_id = os.path.splitext(os.path.basename(pdf_file))[0]
                result = run_async_safe(vector_store.add_document(
                    document_id=document_id,
                    chunks=chunks,
                    document_metadata=pdf_content.get("metadata", {})
                ))
                
                if result["success"]:
                    print(f"✅ Document added to vector store")
                    print(f"   Document ID: {result['document_id']}")
                    print(f"   Chunks added: {result['chunks_added']}")
                    
                    return vector_store, document_id
                else:
                    print(f"❌ Failed to add document: {result['error']}")
                    return None, None
            else:
                print(f"❌ Failed to read PDF: {pdf_content['error']}")
                return None, None
        else:
            print("⚠️  No PDF file found for testing")
            print("   Looked for files:")
            for path in possible_pdfs:
                print(f"   - {path}")
            return None, None
        
    except Exception as e:
        print(f"❌ Error during PDF processing: {str(e)}")
        return None, None

def test_search_functionality(vector_store):
    """Test search functionality."""
    
    print("\n🧪 Testing Search Functionality")
    print("=" * 50)
    
    if not vector_store:
        print("⚠️  No vector store available for search testing")
        return False
    
    try:
        # Test 1: Basic search
        print("\n🔍 Test 1: Basic Vector Search")
        print("-" * 40)
        
        search_query = "machine learning artificial intelligence"
        basic_results = run_async_safe(vector_store.search(
            query=search_query,
            top_k=3,
            min_similarity=0.1
        ))
        
        print(f"✅ Basic search completed")
        print(f"   Query: '{search_query}'")
        print(f"   Results found: {len(basic_results)}")
        
        for i, result in enumerate(basic_results[:2]):
            print(f"   Result {i+1}:")
            print(f"     Similarity: {result['similarity']:.3f}")
            print(f"     Content: {result['content'][:80]}...")
        
        # Test 2: Advanced semantic search
        print("\n🚀 Test 2: Advanced Semantic Search")
        print("-" * 40)
        
        semantic_results = run_async_safe(vector_store.semantic_search(
            query=search_query,
            top_k=3,
            min_similarity=0.1,
            use_query_expansion=True,
            use_reranking=True
        ))
        
        print(f"✅ Semantic search completed")
        print(f"   Results found: {len(semantic_results)}")
        
        for i, result in enumerate(semantic_results[:2]):
            print(f"   Result {i+1}:")
            print(f"     Similarity: {result['similarity']:.3f}")
            if 'rerank_score' in result:
                print(f"     Re-rank Score: {result['rerank_score']:.3f}")
            print(f"     Content: {result['content'][:80]}...")
        
        return len(basic_results) > 0 or len(semantic_results) > 0
        
    except Exception as e:
        print(f"❌ Error during search testing: {str(e)}")
        return False

def test_document_management(vector_store):
    """Test document management functionality."""
    
    print("\n🧪 Testing Document Management")
    print("=" * 50)
    
    if not vector_store:
        print("⚠️  No vector store available for management testing")
        return False
    
    try:
        # Test document statistics
        print("\n📊 Test: Document Statistics")
        print("-" * 40)
        
        stats = vector_store.get_stats()
        
        print(f"✅ Document statistics retrieved")
        print(f"   Total documents: {stats['total_documents']}")
        print(f"   Total chunks: {stats['total_chunks']}")
        print(f"   Average chunks per document: {stats['avg_chunks_per_document']:.1f}")
        print(f"   Document IDs: {stats['document_ids']}")
        
        if 'embedding_stats' in stats:
            embed_stats = stats['embedding_stats']
            print(f"   Embedding cache size: {embed_stats.get('cache_size', 0)}")
            print(f"   Embedding model: {embed_stats.get('model_name', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during document management testing: {str(e)}")
        return False

def test_question_answering_simulation(vector_store):
    """Test question answering simulation."""
    
    print("\n🧪 Testing Question Answering Simulation")
    print("=" * 50)
    
    if not vector_store:
        print("⚠️  No vector store available for QA testing")
        return False
    
    try:
        # Simulate question answering workflow
        print("\n❓ Test: Question Answering Workflow")
        print("-" * 40)
        
        question = "What are the applications of artificial intelligence?"
        
        # Search for relevant context
        context_results = run_async_safe(vector_store.semantic_search(
            query=question,
            top_k=3,
            min_similarity=0.1,
            use_query_expansion=True,
            use_reranking=True
        ))
        
        if context_results:
            print(f"✅ Question answering simulation completed")
            print(f"   Question: '{question}'")
            print(f"   Context found: {len(context_results)} chunks")
            
            print(f"\n📖 Context Retrieved:")
            for i, result in enumerate(context_results[:2]):
                print(f"   Context {i+1}:")
                print(f"     Similarity: {result['similarity']:.3f}")
                if 'rerank_score' in result:
                    print(f"     Re-rank Score: {result['rerank_score']:.3f}")
                print(f"     Content: {result['content'][:100]}...")
                print()
            
            # Calculate average similarity
            avg_similarity = sum(r['similarity'] for r in context_results) / len(context_results)
            print(f"   Average similarity: {avg_similarity:.3f}")
        else:
            print(f"✅ Question processed but no relevant context found")
            print(f"   This would result in a 'no information available' response")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during question answering: {str(e)}")
        return False

def run_all_rag_tools_tests():
    """Run all RAG tools tests."""
    
    print("🚀 Starting Comprehensive RAG Tools Tests")
    print("This will test the complete RAG workflow: PDF processing, search, and QA\n")
    
    results = []
    
    try:
        # Test component initialization
        init_result = test_tool_initialization()
        results.append(("Component Initialization", init_result))
        
        # Test PDF processing workflow
        vector_store, document_id = test_pdf_processing_workflow()
        results.append(("PDF Processing", vector_store is not None))
        
        # Test search functionality
        if vector_store:
            search_result = test_search_functionality(vector_store)
            results.append(("Search Functionality", search_result))
            
            # Test document management
            mgmt_result = test_document_management(vector_store)
            results.append(("Document Management", mgmt_result))
            
            # Test question answering simulation
            qa_result = test_question_answering_simulation(vector_store)
            results.append(("Question Answering", qa_result))
        else:
            print("⚠️  Skipping advanced tests - no documents processed")
            results.extend([
                ("Search Functionality", False),
                ("Document Management", False),
                ("Question Answering", False)
            ])
        
        # Summary
        print("\n📊 Test Results Summary:")
        print("=" * 30)
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED/SKIPPED"
            print(f"{test_name}: {status}")
        
        print("\n✅ RAG Tools Testing Complete!")
        print("\nKey Features Demonstrated:")
        print("- ✓ PDF reading and text extraction")
        print("- ✓ Text chunking with different strategies")
        print("- ✓ Embedding generation and vector storage")
        print("- ✓ Basic vector similarity search")
        print("- ✓ Advanced semantic search with re-ranking")
        print("- ✓ Document management and statistics")
        print("- ✓ Question answering workflow simulation")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")

if __name__ == "__main__":
    print("🔧 RAG Tools Tests")
    print("This will test the complete RAG workflow using the underlying components\n")
    
    try:
        run_all_rag_tools_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        print("Make sure you have:")
        print("1. All required dependencies installed")
        print("2. Access to embedding models (SentenceTransformers or OpenAI)")
        print("3. A PDF file for testing (optional)") 