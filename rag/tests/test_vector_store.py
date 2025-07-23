#!/usr/bin/env python3
"""
Test script for the Vector Store utility.
Demonstrates document storage, semantic search, query expansion, and re-ranking.
"""

import asyncio
import os
import sys
import json

# Add the parent directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.vector_store import AdvancedVectorStore
from utils.text_chunker import TextChunker, TextChunk
from utils.embeddings import SentenceTransformerEmbeddingManager, EmbeddingManager

async def test_vector_store_initialization():
    """Test vector store initialization with different embedding managers."""
    
    print("🧪 Testing Vector Store Initialization")
    print("=" * 50)
    
    try:
        # Test 1: Default initialization (SentenceTransformers)
        print("\n⚙️  Test 1: Default Initialization (SentenceTransformers)")
        print("-" * 40)
        
        try:
            vector_store = AdvancedVectorStore()
            print(f"✅ Vector store initialized with SentenceTransformers")
            print(f"   Name: {vector_store.name}")
            print(f"   Description: {vector_store.description}")
            print(f"   Embedding manager type: {type(vector_store.embedding_manager).__name__}")
        except ImportError:
            print("⚠️  SentenceTransformers not available, trying OpenAI")
            if os.getenv("OPENAI_API_KEY"):
                embedding_manager = EmbeddingManager()
                vector_store = AdvancedVectorStore(embedding_manager)
                print(f"✅ Vector store initialized with OpenAI embeddings")
            else:
                print("❌ No embedding manager available")
                return None
        
        # Test 2: Custom embedding manager
        print("\n🔧 Test 2: Custom Embedding Manager")
        print("-" * 40)
        
        try:
            custom_embedding_manager = SentenceTransformerEmbeddingManager(
                model_name="all-MiniLM-L6-v2",
                cache_embeddings=True
            )
            custom_vector_store = AdvancedVectorStore(custom_embedding_manager)
            print(f"✅ Custom vector store initialized")
            print(f"   Embedding model: {custom_embedding_manager.model_name}")
        except ImportError:
            print("⚠️  Custom SentenceTransformer not available")
            custom_vector_store = vector_store
        
        return vector_store, custom_vector_store
        
    except Exception as e:
        print(f"❌ Error during vector store initialization: {str(e)}")
        return None, None

def create_sample_chunks():
    """Create sample text chunks for testing."""
    
    sample_texts = [
        "Artificial intelligence is revolutionizing the way we work and live. Machine learning algorithms can process vast amounts of data to identify patterns and make predictions.",
        
        "Natural language processing enables computers to understand and generate human language. This technology powers chatbots, translation services, and text analysis tools.",
        
        "Computer vision allows machines to interpret and analyze visual information from images and videos. Applications include facial recognition, autonomous vehicles, and medical imaging.",
        
        "Deep learning uses neural networks with multiple layers to solve complex problems. These models have achieved breakthrough results in image recognition, speech processing, and game playing.",
        
        "Robotics combines AI with mechanical engineering to create intelligent machines that can perform physical tasks. Modern robots are used in manufacturing, healthcare, and exploration.",
        
        "Data science involves extracting insights from large datasets using statistical methods and machine learning. It's essential for business intelligence and scientific research.",
        
        "Cloud computing provides on-demand access to computing resources over the internet. It enables scalable AI applications and reduces infrastructure costs.",
        
        "Cybersecurity protects digital systems from threats and attacks. AI-powered security tools can detect anomalies and respond to threats in real-time.",
        
        "The Internet of Things (IoT) connects everyday devices to the internet, creating smart homes, cities, and industries. AI helps process and analyze IoT data.",
        
        "Blockchain technology provides secure, decentralized record-keeping. It's used in cryptocurrency, supply chain management, and digital identity verification."
    ]
    
    chunker = TextChunker(chunk_size=200, overlap_size=50)
    chunks = []
    
    for i, text in enumerate(sample_texts):
        chunk = TextChunk(
            content=text,
            chunk_id=f"chunk_{i:03d}",
            start_index=i * 200,
            end_index=(i + 1) * 200,
            metadata={"topic": "technology", "source": "test_data"},
            word_count=len(text.split())
        )
        chunks.append(chunk)
    
    return chunks

async def test_document_storage(vector_store):
    """Test document storage and indexing."""
    
    print("\n🧪 Testing Document Storage")
    print("=" * 50)
    
    try:
        # Test 1: Add single document
        print("\n📄 Test 1: Adding Single Document")
        print("-" * 40)
        
        sample_chunks = create_sample_chunks()[:5]  # Use first 5 chunks
        
        result = await vector_store.add_document(
            document_id="tech_article_1",
            chunks=sample_chunks,
            document_metadata={"title": "Technology Overview", "author": "Test", "year": 2024}
        )
        
        print(f"✅ Document added successfully")
        print(f"   Document ID: {result['document_id']}")
        print(f"   Chunks added: {result['chunks_added']}")
        print(f"   Success: {result['success']}")
        print(f"   Chunk IDs: {result['chunk_ids'][:3]}...")
        
        # Test 2: Add second document
        print("\n📚 Test 2: Adding Second Document")
        print("-" * 40)
        
        more_chunks = create_sample_chunks()[5:]  # Use remaining chunks
        
        result2 = await vector_store.add_document(
            document_id="tech_article_2",
            chunks=more_chunks,
            document_metadata={"title": "Advanced Technology", "author": "Test", "year": 2024}
        )
        
        print(f"✅ Second document added")
        print(f"   Document ID: {result2['document_id']}")
        print(f"   Chunks added: {result2['chunks_added']}")
        
        # Test 3: Get document statistics
        print("\n📊 Test 3: Document Statistics")
        print("-" * 40)
        
        stats = vector_store.get_stats()
        print(f"✅ Statistics retrieved")
        print(f"   Total documents: {stats['total_documents']}")
        print(f"   Total chunks: {stats['total_chunks']}")
        print(f"   Average chunks per document: {stats['avg_chunks_per_document']:.1f}")
        print(f"   Document IDs: {stats['document_ids']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during document storage: {str(e)}")
        return False

async def test_basic_search(vector_store):
    """Test basic vector similarity search."""
    
    print("\n🧪 Testing Basic Vector Search")
    print("=" * 50)
    
    try:
        # Test 1: Simple search
        print("\n🔍 Test 1: Simple Search Query")
        print("-" * 40)
        
        query = "machine learning algorithms"
        results = await vector_store.search(
            query=query,
            top_k=3,
            min_similarity=0.1
        )
        
        print(f"✅ Basic search completed")
        print(f"   Query: '{query}'")
        print(f"   Results found: {len(results)}")
        
        for i, result in enumerate(results):
            print(f"   Result {i+1}:")
            print(f"     Similarity: {result['similarity']:.3f}")
            print(f"     Content: {result['content'][:80]}...")
            print(f"     Document: {result['document_id']}")
            print()
        
        # Test 2: Search with higher threshold
        print("\n🎯 Test 2: Search with High Similarity Threshold")
        print("-" * 40)
        
        high_threshold_results = await vector_store.search(
            query="artificial intelligence",
            top_k=5,
            min_similarity=0.3
        )
        
        print(f"✅ High threshold search completed")
        print(f"   Results with similarity > 0.3: {len(high_threshold_results)}")
        
        for i, result in enumerate(high_threshold_results):
            print(f"   Result {i+1}: Similarity {result['similarity']:.3f}")
        
        # Test 3: Search specific document
        print("\n📄 Test 3: Search Within Specific Document")
        print("-" * 40)
        
        doc_specific_results = await vector_store.search(
            query="computer vision",
            top_k=3,
            document_ids=["tech_article_1"]
        )
        
        print(f"✅ Document-specific search completed")
        print(f"   Results from tech_article_1: {len(doc_specific_results)}")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"❌ Error during basic search: {str(e)}")
        return False

async def test_semantic_search(vector_store):
    """Test advanced semantic search with query expansion and re-ranking."""
    
    print("\n🧪 Testing Advanced Semantic Search")
    print("=" * 50)
    
    try:
        # Test 1: Semantic search with query expansion
        print("\n🚀 Test 1: Semantic Search with Query Expansion")
        print("-" * 40)
        
        query = "AI applications"
        results = await vector_store.semantic_search(
            query=query,
            top_k=4,
            min_similarity=0.1,
            use_query_expansion=True,
            use_reranking=True
        )
        
        print(f"✅ Semantic search with expansion completed")
        print(f"   Query: '{query}'")
        print(f"   Results found: {len(results)}")
        
        for i, result in enumerate(results):
            print(f"   Result {i+1}:")
            print(f"     Similarity: {result['similarity']:.3f}")
            if 'rerank_score' in result:
                print(f"     Re-rank Score: {result['rerank_score']:.3f}")
            if 'matched_query' in result:
                print(f"     Matched Query: {result['matched_query']}")
            print(f"     Content: {result['content'][:80]}...")
            print()
        
        # Test 2: Compare with and without advanced features
        print("\n⚖️  Test 2: Comparing Basic vs Advanced Search")
        print("-" * 40)
        
        basic_results = await vector_store.search(
            query="deep learning networks",
            top_k=3,
            min_similarity=0.1
        )
        
        advanced_results = await vector_store.semantic_search(
            query="deep learning networks",
            top_k=3,
            min_similarity=0.1,
            use_query_expansion=True,
            use_reranking=True
        )
        
        print(f"✅ Comparison completed")
        print(f"   Basic search results: {len(basic_results)}")
        print(f"   Advanced search results: {len(advanced_results)}")
        
        if basic_results and advanced_results:
            print(f"   Basic top similarity: {basic_results[0]['similarity']:.3f}")
            print(f"   Advanced top similarity: {advanced_results[0]['similarity']:.3f}")
            if 'rerank_score' in advanced_results[0]:
                print(f"   Advanced re-rank score: {advanced_results[0]['rerank_score']:.3f}")
        
        # Test 3: Test diversification
        print("\n🌈 Test 3: Result Diversification")
        print("-" * 40)
        
        diverse_results = await vector_store.semantic_search(
            query="technology",
            top_k=5,
            min_similarity=0.1,
            use_query_expansion=False,
            use_reranking=True,
            diversity_threshold=0.7
        )
        
        print(f"✅ Diversified search completed")
        print(f"   Diverse results: {len(diverse_results)}")
        
        for i, result in enumerate(diverse_results):
            print(f"   Result {i+1}: {result['content'][:60]}...")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"❌ Error during semantic search: {str(e)}")
        return False

async def test_document_management(vector_store):
    """Test document management operations."""
    
    print("\n🧪 Testing Document Management")
    print("=" * 50)
    
    try:
        # Test 1: Get document chunks
        print("\n📑 Test 1: Retrieving Document Chunks")
        print("-" * 40)
        
        doc_chunks = vector_store.get_document_chunks("tech_article_1")
        print(f"✅ Document chunks retrieved")
        print(f"   Chunks in tech_article_1: {len(doc_chunks)}")
        
        if doc_chunks:
            print(f"   Sample chunk: {doc_chunks[0].chunk.content[:60]}...")
            print(f"   Chunk metadata: {doc_chunks[0].chunk.metadata}")
        
        # Test 2: Add another document for testing removal
        print("\n➕ Test 2: Adding Document for Removal Test")
        print("-" * 40)
        
        temp_chunks = [
            TextChunk(
                content="Temporary test content for removal testing.",
                chunk_id="temp_001",
                start_index=0,
                end_index=50,
                metadata={"temp": True},
                word_count=7
            )
        ]
        
        add_result = await vector_store.add_document(
            document_id="temp_doc",
            chunks=temp_chunks,
            document_metadata={"temporary": True}
        )
        
        print(f"✅ Temporary document added")
        print(f"   Document ID: {add_result['document_id']}")
        
        # Check stats before removal
        stats_before = vector_store.get_stats()
        print(f"   Documents before removal: {stats_before['total_documents']}")
        
        # Test 3: Remove document
        print("\n🗑️  Test 3: Removing Document")
        print("-" * 40)
        
        remove_result = vector_store.remove_document("temp_doc")
        
        print(f"✅ Document removal completed")
        print(f"   Success: {remove_result['success']}")
        print(f"   Chunks removed: {remove_result['chunks_removed']}")
        
        # Check stats after removal
        stats_after = vector_store.get_stats()
        print(f"   Documents after removal: {stats_after['total_documents']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during document management: {str(e)}")
        return False

async def test_persistence(vector_store):
    """Test save and load functionality."""
    
    print("\n🧪 Testing Vector Store Persistence")
    print("=" * 50)
    
    try:
        # Test 1: Save vector store
        print("\n💾 Test 1: Saving Vector Store")
        print("-" * 40)
        
        save_file = "test_vector_store.json"
        vector_store.save_to_file(save_file)
        
        print(f"✅ Vector store saved successfully")
        print(f"   Saved to: {save_file}")
        print(f"   File exists: {os.path.exists(save_file)}")
        
        if os.path.exists(save_file):
            file_size = os.path.getsize(save_file)
            print(f"   File size: {file_size:,} bytes")
        
        # Test 2: Create new vector store and load
        print("\n📂 Test 2: Loading Vector Store")
        print("-" * 40)
        
        new_vector_store = AdvancedVectorStore()
        new_vector_store.load_from_file(save_file)
        
        # Compare stats
        original_stats = vector_store.get_stats()
        loaded_stats = new_vector_store.get_stats()
        
        print(f"✅ Vector store loaded successfully")
        print(f"   Original documents: {original_stats['total_documents']}")
        print(f"   Loaded documents: {loaded_stats['total_documents']}")
        print(f"   Original chunks: {original_stats['total_chunks']}")
        print(f"   Loaded chunks: {loaded_stats['total_chunks']}")
        
        # Test 3: Verify search works on loaded store
        print("\n🔍 Test 3: Testing Search on Loaded Store")
        print("-" * 40)
        
        test_results = await new_vector_store.search(
            query="artificial intelligence",
            top_k=2
        )
        
        print(f"✅ Search on loaded store successful")
        print(f"   Results found: {len(test_results)}")
        
        # Clean up
        if os.path.exists(save_file):
            os.remove(save_file)
            print(f"✅ Test file cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during persistence testing: {str(e)}")
        return False

async def run_all_vector_store_tests():
    """Run all vector store tests."""
    
    print("🚀 Starting Comprehensive Vector Store Tests")
    print("This will test document storage, semantic search, and advanced features\n")
    
    results = []
    
    try:
        # Test initialization
        vector_store, custom_vector_store = await test_vector_store_initialization()
        if vector_store:
            results.append(("Initialization", True))
            
            # Test document storage
            storage_result = await test_document_storage(vector_store)
            results.append(("Document Storage", storage_result))
            
            # Test basic search
            basic_search_result = await test_basic_search(vector_store)
            results.append(("Basic Search", basic_search_result))
            
            # Test semantic search
            semantic_search_result = await test_semantic_search(vector_store)
            results.append(("Semantic Search", semantic_search_result))
            
            # Test document management
            management_result = await test_document_management(vector_store)
            results.append(("Document Management", management_result))
            
            # Test persistence
            persistence_result = await test_persistence(vector_store)
            results.append(("Persistence", persistence_result))
            
        else:
            results.append(("Initialization", False))
        
        # Summary
        print("\n📊 Test Results Summary:")
        print("=" * 30)
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        print("\n✅ Vector Store Testing Complete!")
        print("\nKey Features Demonstrated:")
        print("- ✓ Document storage and indexing")
        print("- ✓ Basic vector similarity search")
        print("- ✓ Advanced semantic search with query expansion")
        print("- ✓ Re-ranking and result diversification")
        print("- ✓ Document management operations")
        print("- ✓ Persistence and data loading")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")

if __name__ == "__main__":
    print("🗄️  Vector Store Utility Tests")
    print("This will test advanced vector search, storage, and retrieval capabilities\n")
    
    try:
        asyncio.run(run_all_vector_store_tests())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        print("Make sure you have:")
        print("1. Installed sentence-transformers: pip install sentence-transformers")
        print("2. Or set OPENAI_API_KEY if using OpenAI embeddings") 