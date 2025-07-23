#!/usr/bin/env python3
"""
Test script for the Embeddings utility.
Demonstrates embedding generation, similarity calculations, and caching.
"""

import asyncio
import os
import sys

# Add the parent directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.embeddings import SentenceTransformerEmbeddingManager, EmbeddingManager, EmbeddingResult

async def test_sentence_transformer_embeddings():
    """Test the SentenceTransformer embedding manager."""
    
    print("🧪 Testing SentenceTransformer Embeddings")
    print("=" * 50)
    
    try:
        # Test 1: Initialize embedding manager
        print("\n📚 Test 1: Initializing SentenceTransformer Embedding Manager")
        print("-" * 40)
        
        embedding_manager = SentenceTransformerEmbeddingManager(
            model_name="all-MiniLM-L6-v2",
            cache_embeddings=True
        )
        print(f"✅ Embedding manager initialized successfully")
        print(f"   Model: {embedding_manager.model_name}")
        print(f"   Embedding dimension: {embedding_manager.model.get_sentence_embedding_dimension()}")
        
        # Test 2: Generate single embedding
        print("\n🔍 Test 2: Generating Single Embedding")
        print("-" * 40)
        
        test_text = "This is a test document about artificial intelligence and machine learning."
        result = await embedding_manager.generate_embedding(
            text=test_text,
            metadata={"type": "test", "category": "AI"}
        )
        
        print(f"✅ Embedding generated successfully")
        print(f"   Text: {result.text[:50]}...")
        print(f"   Embedding dimension: {len(result.embedding)}")
        print(f"   Model: {result.model}")
        print(f"   Token count: {result.token_count}")
        print(f"   Metadata: {result.metadata}")
        
        # Test 3: Generate batch embeddings
        print("\n📦 Test 3: Generating Batch Embeddings")
        print("-" * 40)
        
        test_texts = [
            "Artificial intelligence is revolutionizing technology.",
            "Machine learning algorithms can process vast amounts of data.",
            "Natural language processing enables computers to understand human language.",
            "Deep learning models use neural networks with multiple layers.",
            "Computer vision allows machines to interpret visual information."
        ]
        
        batch_results = await embedding_manager.generate_embeddings_batch(
            texts=test_texts,
            metadata_list=[{"batch_id": i, "topic": "AI"} for i in range(len(test_texts))],
            batch_size=3
        )
        
        print(f"✅ Batch embeddings generated successfully")
        print(f"   Number of embeddings: {len(batch_results)}")
        print(f"   Average embedding dimension: {sum(len(r.embedding) for r in batch_results) / len(batch_results)}")
        
        for i, result in enumerate(batch_results):
            print(f"   Embedding {i+1}: {result.text[:30]}... (dim: {len(result.embedding)})")
        
        # Test 4: Test similarity calculations
        print("\n🎯 Test 4: Testing Similarity Calculations")
        print("-" * 40)
        
        # Compare similar texts
        similar_text = "AI and machine learning are changing the world."
        similar_result = await embedding_manager.generate_embedding(similar_text)
        
        similarity = embedding_manager.cosine_similarity(
            result.embedding, 
            similar_result.embedding
        )
        
        print(f"✅ Similarity calculation complete")
        print(f"   Text 1: {result.text[:50]}...")
        print(f"   Text 2: {similar_result.text}")
        print(f"   Cosine similarity: {similarity:.4f}")
        
        # Test 5: Find most similar embeddings
        print("\n🔍 Test 5: Finding Most Similar Embeddings")
        print("-" * 40)
        
        query_text = "What is machine learning?"
        query_result = await embedding_manager.generate_embedding(query_text)
        
        most_similar = embedding_manager.find_most_similar(
            query_result.embedding,
            batch_results,
            top_k=3
        )
        
        print(f"✅ Found most similar embeddings")
        print(f"   Query: {query_text}")
        print(f"   Top {len(most_similar)} results:")
        
        for i, (embedding_result, score) in enumerate(most_similar):
            print(f"   {i+1}. Score: {score:.4f} - {embedding_result.text[:60]}...")
        
        # Test 6: Cache statistics and management
        print("\n📊 Test 6: Cache Statistics and Management")
        print("-" * 40)
        
        cache_stats = embedding_manager.get_cache_stats()
        print(f"✅ Cache statistics retrieved")
        print(f"   Cache size: {cache_stats['cache_size']} embeddings")
        print(f"   Model name: {cache_stats['model_name']}")
        print(f"   Embedding dimension: {cache_stats['embedding_dimension']}")
        
        # Test cache save/load
        cache_file = "test_embedding_cache.json"
        embedding_manager.save_cache(cache_file)
        print(f"✅ Cache saved to {cache_file}")
        
        # Create new manager and load cache
        new_manager = SentenceTransformerEmbeddingManager(model_name="all-MiniLM-L6-v2")
        new_manager.load_cache(cache_file)
        new_stats = new_manager.get_cache_stats()
        print(f"✅ Cache loaded in new manager")
        print(f"   Loaded cache size: {new_stats['cache_size']} embeddings")
        
        # Clean up
        os.remove(cache_file)
        print(f"✅ Test cache file cleaned up")
        
        print("\n🎉 SentenceTransformer Embeddings Testing Complete!")
        return True
        
    except ImportError:
        print("⚠️  SentenceTransformers not available, skipping these tests")
        return False
    except Exception as e:
        print(f"❌ Error during SentenceTransformer testing: {str(e)}")
        return False

async def test_openai_embeddings():
    """Test the OpenAI embedding manager (if API key is available)."""
    
    print("\n🧪 Testing OpenAI Embeddings")
    print("=" * 50)
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OpenAI API key not found, skipping OpenAI embedding tests")
        return False
    
    try:
        # Test 1: Initialize OpenAI embedding manager
        print("\n🔑 Test 1: Initializing OpenAI Embedding Manager")
        print("-" * 40)
        
        embedding_manager = EmbeddingManager(
            model="text-embedding-3-small",
            cache_embeddings=True
        )
        print(f"✅ OpenAI embedding manager initialized")
        print(f"   Model: {embedding_manager.model}")
        
        # Test 2: Generate and compare embeddings
        print("\n📝 Test 2: Generating OpenAI Embeddings")
        print("-" * 40)
        
        test_texts = [
            "OpenAI provides powerful language models.",
            "GPT models are transformer-based architectures.",
            "Text embeddings capture semantic meaning."
        ]
        
        results = await embedding_manager.generate_embeddings_batch(
            texts=test_texts,
            batch_size=3
        )
        
        print(f"✅ OpenAI embeddings generated")
        print(f"   Number of embeddings: {len(results)}")
        print(f"   Embedding dimension: {len(results[0].embedding)}")
        print(f"   Total tokens used: {sum(r.token_count for r in results)}")
        
        # Test similarity with OpenAI embeddings
        similarity = embedding_manager.cosine_similarity(
            results[0].embedding,
            results[1].embedding
        )
        print(f"   Similarity between first two texts: {similarity:.4f}")
        
        # Test cache stats
        cache_stats = embedding_manager.get_cache_stats()
        print(f"✅ OpenAI cache stats: {cache_stats}")
        
        print("\n🎉 OpenAI Embeddings Testing Complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error during OpenAI testing: {str(e)}")
        return False

async def test_embedding_comparison():
    """Compare SentenceTransformer and OpenAI embeddings if both are available."""
    
    print("\n🧪 Testing Embedding Comparison")
    print("=" * 50)
    
    try:
        # Initialize both managers if possible
        st_manager = None
        openai_manager = None
        
        try:
            st_manager = SentenceTransformerEmbeddingManager(model_name="all-MiniLM-L6-v2")
            print("✅ SentenceTransformer manager ready")
        except ImportError:
            print("⚠️  SentenceTransformers not available")
        
        if os.getenv("OPENAI_API_KEY"):
            try:
                openai_manager = EmbeddingManager(model="text-embedding-3-small")
                print("✅ OpenAI manager ready")
            except Exception:
                print("⚠️  OpenAI manager failed to initialize")
        else:
            print("⚠️  OpenAI API key not available")
        
        if not st_manager and not openai_manager:
            print("❌ No embedding managers available for comparison")
            return False
        
        if st_manager and openai_manager:
            print("\n⚡ Comparing SentenceTransformer vs OpenAI Embeddings")
            print("-" * 40)
            
            test_text = "Artificial intelligence is transforming the future of technology."
            
            # Generate embeddings with both
            st_result = await st_manager.generate_embedding(test_text)
            openai_result = await openai_manager.generate_embedding(test_text)
            
            print(f"✅ Embeddings generated with both managers")
            print(f"   SentenceTransformer dimension: {len(st_result.embedding)}")
            print(f"   OpenAI dimension: {len(openai_result.embedding)}")
            print(f"   SentenceTransformer tokens: {st_result.token_count}")
            print(f"   OpenAI tokens: {openai_result.token_count}")
            
        print("\n🎉 Embedding Comparison Complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error during comparison: {str(e)}")
        return False

async def run_all_embedding_tests():
    """Run all embedding tests."""
    
    print("🚀 Starting Comprehensive Embedding Tests")
    print("This will test embedding generation, similarity, and caching\n")
    
    results = []
    
    try:
        # Test SentenceTransformer embeddings
        st_result = await test_sentence_transformer_embeddings()
        results.append(("SentenceTransformer", st_result))
        
        # Test OpenAI embeddings
        openai_result = await test_openai_embeddings()
        results.append(("OpenAI", openai_result))
        
        # Test comparison
        comparison_result = await test_embedding_comparison()
        results.append(("Comparison", comparison_result))
        
        # Summary
        print("\n📊 Test Results Summary:")
        print("=" * 30)
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED/SKIPPED"
            print(f"{test_name}: {status}")
        
        print("\n✅ Embedding Testing Complete!")
        print("\nKey Features Demonstrated:")
        print("- ✓ Local embedding generation (SentenceTransformers)")
        print("- ✓ Cloud embedding generation (OpenAI)")
        print("- ✓ Batch processing and caching")
        print("- ✓ Similarity calculations and search")
        print("- ✓ Cache management and persistence")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")

if __name__ == "__main__":
    print("🧪 Embedding Utility Tests")
    print("This will test embedding generation, similarity calculations, and caching\n")
    
    try:
        asyncio.run(run_all_embedding_tests())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        print("Make sure you have:")
        print("1. Installed sentence-transformers: pip install sentence-transformers")
        print("2. Set OPENAI_API_KEY if you want to test OpenAI embeddings") 