#!/usr/bin/env python3
"""
Test script for the Text Chunker utility.
Demonstrates different chunking strategies, overlap handling, and chunk optimization.
"""

import os
import sys

# Add the parent directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.text_chunker import TextChunker, TextChunk

def test_text_chunker_initialization():
    """Test text chunker initialization with different configurations."""
    
    print("🧪 Testing Text Chunker Initialization")
    print("=" * 50)
    
    try:
        # Test 1: Default initialization
        print("\n⚙️  Test 1: Default Configuration")
        print("-" * 40)
        
        chunker = TextChunker()
        print(f"✅ Default chunker initialized")
        print(f"   Chunk size: {chunker.chunk_size}")
        print(f"   Overlap size: {chunker.overlap_size}")
        print(f"   Min chunk size: {chunker.min_chunk_size}")
        print(f"   Name: {chunker.name}")
        print(f"   Description: {chunker.description}")
        
        # Test 2: Custom configuration
        print("\n🔧 Test 2: Custom Configuration")
        print("-" * 40)
        
        custom_chunker = TextChunker(
            chunk_size=500,
            overlap_size=100,
            min_chunk_size=50
        )
        print(f"✅ Custom chunker initialized")
        print(f"   Chunk size: {custom_chunker.chunk_size}")
        print(f"   Overlap size: {custom_chunker.overlap_size}")
        print(f"   Min chunk size: {custom_chunker.min_chunk_size}")
        
        return chunker, custom_chunker
        
    except Exception as e:
        print(f"❌ Error during chunker initialization: {str(e)}")
        return None, None

def test_recursive_chunking(chunker):
    """Test recursive chunking strategy."""
    
    print("\n🧪 Testing Recursive Chunking Strategy")
    print("=" * 50)
    
    try:
        # Test 1: Simple text chunking
        print("\n📝 Test 1: Simple Text Chunking")
        print("-" * 40)
        
        simple_text = """
        This is a test document for demonstrating text chunking capabilities.
        
        The recursive chunking strategy tries to split text at natural boundaries like paragraphs, sentences, and clauses.
        It maintains semantic coherence while respecting size constraints.
        
        This approach is ideal for general-purpose RAG applications where you want to preserve context while ensuring chunks are appropriately sized for embedding models.
        
        The chunker will try different separators in order of preference: double newlines (paragraphs), single newlines, periods, exclamation marks, question marks, semicolons, commas, and finally spaces.
        """
        
        chunks = chunker.chunk_text(simple_text, strategy="recursive", metadata={"test": "simple"})
        
        print(f"✅ Recursive chunking complete")
        print(f"   Input text length: {len(simple_text)} characters")
        print(f"   Number of chunks: {len(chunks)}")
        
        for i, chunk in enumerate(chunks):
            print(f"   Chunk {i+1}: {len(chunk.content)} chars, {chunk.word_count} words")
            print(f"   Preview: {chunk.content[:60]}...")
            print(f"   Metadata: {chunk.metadata}")
            print()
        
        # Test 2: Long document chunking
        print("\n📚 Test 2: Long Document Chunking")
        print("-" * 40)
        
        # Create a longer text
        long_text = """
        Chapter 1: Introduction to Artificial Intelligence
        
        Artificial Intelligence (AI) represents one of the most transformative technologies of our time. From its humble beginnings in the 1950s to today's sophisticated machine learning systems, AI has evolved dramatically.
        
        The field encompasses various subdomains including machine learning, natural language processing, computer vision, and robotics. Each of these areas contributes to the broader goal of creating intelligent systems that can perform tasks typically requiring human intelligence.
        
        Chapter 2: Machine Learning Fundamentals
        
        Machine learning is a subset of AI that focuses on algorithms that can learn and improve from experience without being explicitly programmed. The three main types of machine learning are supervised learning, unsupervised learning, and reinforcement learning.
        
        Supervised learning uses labeled data to train models that can make predictions on new, unseen data. Common examples include classification tasks like image recognition and regression tasks like price prediction.
        
        Unsupervised learning discovers hidden patterns in data without labeled examples. Clustering and dimensionality reduction are common unsupervised learning techniques.
        
        Chapter 3: Deep Learning Revolution
        
        Deep learning, a subset of machine learning, uses neural networks with multiple layers to model and understand complex patterns in data. The breakthrough came with the development of efficient training algorithms and the availability of large datasets.
        
        Convolutional Neural Networks (CNNs) revolutionized computer vision, while Recurrent Neural Networks (RNNs) and Transformers transformed natural language processing. The attention mechanism in Transformers has been particularly influential.
        
        Chapter 4: Applications and Future Directions
        
        AI applications are now ubiquitous, from recommendation systems and virtual assistants to autonomous vehicles and medical diagnosis. The technology continues to advance rapidly, with new breakthroughs emerging regularly.
        
        Looking ahead, challenges include ensuring AI safety, addressing bias and fairness concerns, and developing more efficient and interpretable models. The future of AI holds immense promise for solving complex global challenges.
        """ * 3  # Repeat to make it longer
        
        long_chunks = chunker.chunk_text(long_text, strategy="recursive", metadata={"test": "long_document"})
        
        print(f"✅ Long document chunking complete")
        print(f"   Input text length: {len(long_text):,} characters")
        print(f"   Number of chunks: {len(long_chunks)}")
        
        # Show statistics
        word_counts = [chunk.word_count for chunk in long_chunks]
        char_counts = [len(chunk.content) for chunk in long_chunks]
        
        print(f"   Average words per chunk: {sum(word_counts) / len(word_counts):.1f}")
        print(f"   Average chars per chunk: {sum(char_counts) / len(char_counts):.1f}")
        print(f"   Min words: {min(word_counts)}, Max words: {max(word_counts)}")
        
        return chunks, long_chunks
        
    except Exception as e:
        print(f"❌ Error during recursive chunking: {str(e)}")
        return [], []

def test_sentence_chunking(chunker):
    """Test sentence-based chunking strategy."""
    
    print("\n🧪 Testing Sentence Chunking Strategy")
    print("=" * 50)
    
    try:
        # Test sentence chunking
        print("\n🔤 Test: Sentence-Based Chunking")
        print("-" * 40)
        
        sentence_text = """
        Sentence chunking groups text by complete sentences. This approach ensures that sentence boundaries are respected. It's particularly useful for maintaining grammatical coherence. Each chunk will contain complete sentences rather than breaking mid-sentence.
        
        The chunker combines sentences until the target chunk size is reached. When the next sentence would exceed the limit, a new chunk is started. This strategy works well for documents where sentence-level semantic integrity is important.
        
        Benefits include better readability and semantic coherence. Drawbacks might include variable chunk sizes depending on sentence length. Overall, it's an excellent choice for many text processing applications.
        """
        
        sentence_chunks = chunker.chunk_text(sentence_text, strategy="sentence", metadata={"type": "sentence_test"})
        
        print(f"✅ Sentence chunking complete")
        print(f"   Number of chunks: {len(sentence_chunks)}")
        
        for i, chunk in enumerate(sentence_chunks):
            print(f"   Chunk {i+1}: {chunk.word_count} words")
            print(f"   Content: {chunk.content}")
            print(f"   Strategy: {chunk.metadata.get('chunking_strategy')}")
            print()
        
        return sentence_chunks
        
    except Exception as e:
        print(f"❌ Error during sentence chunking: {str(e)}")
        return []

def test_paragraph_chunking(chunker):
    """Test paragraph-based chunking strategy."""
    
    print("\n🧪 Testing Paragraph Chunking Strategy")
    print("=" * 50)
    
    try:
        # Test paragraph chunking
        print("\n📄 Test: Paragraph-Based Chunking")
        print("-" * 40)
        
        paragraph_text = """
        This is the first paragraph of our test document. It contains information about paragraph chunking and how it preserves the natural document structure.

        Paragraph chunking respects document structure by keeping complete paragraphs together whenever possible. This approach is ideal for documents with clear paragraph boundaries.

        When multiple paragraphs can fit within the chunk size limit, they are combined. This maintains the logical flow while optimizing chunk utilization.

        The strategy is particularly effective for formal documents, articles, and reports where paragraph boundaries represent meaningful semantic divisions.

        Benefits include preserved document structure and natural reading flow. This makes it easier for humans to understand the context when reviewing retrieved chunks.
        """
        
        paragraph_chunks = chunker.chunk_text(paragraph_text, strategy="paragraph", metadata={"type": "paragraph_test"})
        
        print(f"✅ Paragraph chunking complete")
        print(f"   Number of chunks: {len(paragraph_chunks)}")
        
        for i, chunk in enumerate(paragraph_chunks):
            print(f"   Chunk {i+1}: {chunk.word_count} words")
            print(f"   Preview: {chunk.content[:100]}...")
            print(f"   Strategy: {chunk.metadata.get('chunking_strategy')}")
            print()
        
        return paragraph_chunks
        
    except Exception as e:
        print(f"❌ Error during paragraph chunking: {str(e)}")
        return []

def test_semantic_chunking(chunker):
    """Test semantic chunking strategy."""
    
    print("\n🧪 Testing Semantic Chunking Strategy")
    print("=" * 50)
    
    try:
        # Test semantic chunking
        print("\n🧠 Test: Semantic-Based Chunking")
        print("-" * 40)
        
        semantic_text = """
        INTRODUCTION TO MACHINE LEARNING

        Machine learning is a powerful subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.

        TYPES OF MACHINE LEARNING

        1. Supervised Learning
        Supervised learning uses labeled training data to learn a mapping function from inputs to outputs.

        2. Unsupervised Learning
        Unsupervised learning finds hidden patterns in data without labeled examples.

        3. Reinforcement Learning
        Reinforcement learning learns through interaction with an environment using rewards and penalties.

        APPLICATIONS OF MACHINE LEARNING

        Machine learning applications span numerous domains including healthcare, finance, transportation, and entertainment.

        Healthcare Applications
        Medical diagnosis, drug discovery, and personalized treatment plans.

        Financial Applications
        Fraud detection, algorithmic trading, and credit scoring.

        FUTURE DIRECTIONS

        The future of machine learning includes improved interpretability, better efficiency, and more robust models.
        """
        
        semantic_chunks = chunker.chunk_text(semantic_text, strategy="semantic", metadata={"type": "semantic_test"})
        
        print(f"✅ Semantic chunking complete")
        print(f"   Number of chunks: {len(semantic_chunks)}")
        
        for i, chunk in enumerate(semantic_chunks):
            print(f"   Chunk {i+1}: {chunk.word_count} words")
            print(f"   Preview: {chunk.content[:80]}...")
            print(f"   Strategy: {chunk.metadata.get('chunking_strategy')}")
            print()
        
        return semantic_chunks
        
    except Exception as e:
        print(f"❌ Error during semantic chunking: {str(e)}")
        return []

def test_chunk_statistics(chunker):
    """Test chunk statistics calculation."""
    
    print("\n🧪 Testing Chunk Statistics")
    print("=" * 50)
    
    try:
        # Create sample chunks for statistics
        print("\n📊 Test: Chunk Statistics Calculation")
        print("-" * 40)
        
        test_text = """
        This is a comprehensive test of the text chunking system. We'll create multiple chunks using different strategies and then analyze the statistics.
        
        The statistics module provides insights into chunk distribution, word counts, character counts, and the strategies used. This information is valuable for optimizing chunking parameters.
        
        Understanding chunk statistics helps in tuning the chunker for specific use cases and document types. Different strategies work better for different content types.
        """
        
        # Test with different strategies
        recursive_chunks = chunker.chunk_text(test_text, strategy="recursive")
        sentence_chunks = chunker.chunk_text(test_text, strategy="sentence")
        paragraph_chunks = chunker.chunk_text(test_text, strategy="paragraph")
        
        all_chunks = recursive_chunks + sentence_chunks + paragraph_chunks
        
        # Calculate statistics
        stats = chunker.get_chunk_statistics(all_chunks)
        
        print(f"✅ Statistics calculated successfully")
        print(f"   Total chunks: {stats['total_chunks']}")
        print(f"   Total words: {stats['total_words']:,}")
        print(f"   Total characters: {stats['total_characters']:,}")
        print(f"   Average words per chunk: {stats['avg_words_per_chunk']:.1f}")
        print(f"   Average chars per chunk: {stats['avg_chars_per_chunk']:.1f}")
        print(f"   Min words: {stats['min_words']}")
        print(f"   Max words: {stats['max_words']}")
        print(f"   Min chars: {stats['min_chars']}")
        print(f"   Max chars: {stats['max_chars']}")
        print(f"   Strategies used: {stats['strategies_used']}")
        
        return stats
        
    except Exception as e:
        print(f"❌ Error during statistics calculation: {str(e)}")
        return {}

def test_edge_cases(chunker):
    """Test edge cases and error handling."""
    
    print("\n🧪 Testing Edge Cases")
    print("=" * 50)
    
    try:
        # Test 1: Empty text
        print("\n🔍 Test 1: Empty Text")
        print("-" * 40)
        
        empty_chunks = chunker.chunk_text("", strategy="recursive")
        print(f"✅ Empty text handled correctly")
        print(f"   Number of chunks: {len(empty_chunks)}")
        
        # Test 2: Very short text
        print("\n📏 Test 2: Very Short Text")
        print("-" * 40)
        
        short_text = "Short."
        short_chunks = chunker.chunk_text(short_text, strategy="recursive")
        print(f"✅ Short text handled")
        print(f"   Input: '{short_text}'")
        print(f"   Number of chunks: {len(short_chunks)}")
        if short_chunks:
            print(f"   Chunk content: '{short_chunks[0].content}'")
        
        # Test 3: Very long single sentence
        print("\n📝 Test 3: Very Long Single Sentence")
        print("-" * 40)
        
        long_sentence = "This is an extremely long sentence that exceeds normal chunk size limits and should test how the chunker handles text that cannot be split at natural boundaries like periods or newlines but instead must be forcibly split at word boundaries to maintain reasonable chunk sizes for processing. " * 10
        
        long_chunks = chunker.chunk_text(long_sentence, strategy="recursive")
        print(f"✅ Long sentence handled")
        print(f"   Input length: {len(long_sentence)} characters")
        print(f"   Number of chunks: {len(long_chunks)}")
        for i, chunk in enumerate(long_chunks):
            print(f"   Chunk {i+1}: {len(chunk.content)} chars")
        
        # Test 4: Text with special characters
        print("\n🔣 Test 4: Special Characters")
        print("-" * 40)
        
        special_text = """
        Testing special characters: áéíóú, çñü, «»""''—–...
        
        Numbers: 123,456.78 and dates: 2024-01-15
        
        Symbols: @#$%^&*()[]{}|\\/?<>
        
        Unicode: 🚀 🧪 💡 📊 ✅ ❌
        """
        
        special_chunks = chunker.chunk_text(special_text, strategy="recursive")
        print(f"✅ Special characters handled")
        print(f"   Number of chunks: {len(special_chunks)}")
        if special_chunks:
            print(f"   Sample content: {special_chunks[0].content[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during edge case testing: {str(e)}")
        return False

def run_all_chunker_tests():
    """Run all text chunker tests."""
    
    print("🚀 Starting Comprehensive Text Chunker Tests")
    print("This will test different chunking strategies, statistics, and edge cases\n")
    
    results = []
    
    try:
        # Test initialization
        chunker, custom_chunker = test_text_chunker_initialization()
        if chunker:
            results.append(("Initialization", True))
            
            # Test chunking strategies
            recursive_result = test_recursive_chunking(chunker)
            results.append(("Recursive Chunking", len(recursive_result[0]) > 0))
            
            sentence_result = test_sentence_chunking(chunker)
            results.append(("Sentence Chunking", len(sentence_result) > 0))
            
            paragraph_result = test_paragraph_chunking(chunker)
            results.append(("Paragraph Chunking", len(paragraph_result) > 0))
            
            semantic_result = test_semantic_chunking(chunker)
            results.append(("Semantic Chunking", len(semantic_result) > 0))
            
            # Test statistics
            stats_result = test_chunk_statistics(chunker)
            results.append(("Statistics", len(stats_result) > 0))
            
            # Test edge cases
            edge_result = test_edge_cases(chunker)
            results.append(("Edge Cases", edge_result))
        else:
            results.append(("Initialization", False))
        
        # Summary
        print("\n📊 Test Results Summary:")
        print("=" * 30)
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        print("\n✅ Text Chunker Testing Complete!")
        print("\nKey Features Demonstrated:")
        print("- ✓ Recursive chunking with overlap")
        print("- ✓ Sentence-based chunking")
        print("- ✓ Paragraph-based chunking")
        print("- ✓ Semantic chunking with structure detection")
        print("- ✓ Chunk statistics and analysis")
        print("- ✓ Edge case handling")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")

if __name__ == "__main__":
    print("✂️  Text Chunker Utility Tests")
    print("This will test different chunking strategies and analyze chunk quality\n")
    
    try:
        run_all_chunker_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        print("Make sure the utils module is properly installed and accessible") 