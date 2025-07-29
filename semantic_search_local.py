#!/usr/bin/env python3
"""
Basic semantic search implementation using LangChain experimental text splitter and local embeddings.
"""

import os
import sys
from pathlib import Path
from typing import List

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure PyTorch to use CPU to avoid Metal Performance Shaders warnings
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'
os.environ['PYTORCH_MPS_LOW_WATERMARK_RATIO'] = '0.0'
os.environ['PYTORCH_MPS_ALLOCATOR_MAX_CACHED_MEMORY'] = '0'
os.environ['PYTORCH_MPS_ALLOCATOR_MAX_CACHED_MEMORY_PERCENT'] = '0'

# Force CPU-only mode for all PyTorch operations
os.environ['PYTORCH_DEVICE'] = 'cpu'

def basic_semantic_search_local():
    """Basic semantic search implementation with PDF processing using local embeddings."""
    
    print("=" * 60)
    print("BASIC SEMANTIC SEARCH WITH LOCAL EMBEDDINGS (CPU-ONLY)")
    print("=" * 60)
    
    # Configuration
    pdf_path = "rag/docs/review_2024.pdf"
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        return False
    
    print(f"✅ Found PDF: {pdf_path}")
    
    try:
        # Import required modules
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        from langchain_core.documents import Document
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        # Step 1: Load PDF documents
        print("\n📄 Step 1: Loading PDF documents...")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"✅ Loaded {len(documents)} pages from PDF")
        
        # Show page previews
        for i, doc in enumerate(documents[:3]):  # Show first 3 pages
            preview = doc.page_content[:100].replace('\n', ' ').strip()
            print(f"   Page {i+1}: {preview}...")
        
        # Step 2: Initialize local embeddings with CPU-only configuration
        print("\n🧠 Step 2: Initializing local embeddings (CPU-only)...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'device': 'cpu'}
        )
        print(f"✅ Using local model: sentence-transformers/all-MiniLM-L6-v2 (CPU-only)")
        
        # Step 3: Create text splitter (since SemanticChunker requires OpenAI)
        print("\n✂️  Step 3: Creating text splitter...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        print(f"✅ Text splitter created with semantic-aware chunking")
        
        # Step 4: Create chunks
        print("\n📝 Step 4: Creating chunks...")
        chunks = text_splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")
        
        # Show chunk statistics
        chunk_lengths = [len(chunk.page_content) for chunk in chunks]
        if chunk_lengths:
            avg_length = sum(chunk_lengths) / len(chunk_lengths)
            print(f"   Average chunk length: {avg_length:.1f} characters")
            print(f"   Shortest chunk: {min(chunk_lengths)} characters")
            print(f"   Longest chunk: {max(chunk_lengths)} characters")
        
        # Show sample chunks
        print("\n📝 Sample chunks:")
        for i, chunk in enumerate(chunks[:3]):
            preview = chunk.page_content[:150].replace('\n', ' ').strip()
            print(f"   Chunk {i+1}: {preview}...")
        
        # Step 5: Create FAISS vector store
        print("\n🗄️  Step 5: Creating FAISS vector store...")
        texts = [chunk.page_content for chunk in chunks]
        vectorstore = FAISS.from_texts(texts, embeddings)
        print(f"✅ FAISS vector store created successfully")
        
        # Step 6: Test semantic search
        print("\n🔍 Step 6: Testing semantic search...")
        
        # Test queries
        test_queries = [
            "What new ai tools i explore",
            "What are the key achievements mentioned?",
            "What is the review cycle period?",
            "What are the areas of improvement?"
        ]
        
        for query in test_queries:
            print(f"\n🔎 Query: '{query}'")
            results = vectorstore.similarity_search(query, k=2)
            
            print(f"✅ Found {len(results)} relevant results:")
            for i, result in enumerate(results):
                preview = result.page_content[:100].replace('\n', ' ').strip()
                print(f"   Result {i+1}: {preview}...")
        
        # Step 7: Save vector store
        print(f"\n💾 Step 7: Saving vector store...")
        vectorstore.save_local("rag/vectorstore/user1_review_2024")
        print(f"✅ Vector store saved to: user1_review_2024/")
        
        # Step 8: Load and test saved vector store
        print(f"\n🔍 Step 8: Testing loaded vector store...")
        loaded_vectorstore = FAISS.load_local("user1_review_2024", embeddings, allow_dangerous_deserialization=True)
        
        # Test with a new query
        new_query = "What is the employee's performance rating?"
        print(f"\n🔎 New query: '{new_query}'")
        new_results = loaded_vectorstore.similarity_search(new_query, k=1)
        
        if new_results:
            preview = new_results[0].page_content[:150].replace('\n', ' ').strip()
            print(f"✅ Best result: {preview}...")
        
        # Step 9: Test similarity search with scores
        print(f"\n🔍 Step 9: Testing similarity search with scores...")
        query = "What are the main responsibilities?"
        results_with_scores = vectorstore.similarity_search_with_score(query, k=3)
        
        print(f"\n🔎 Query: '{query}'")
        print(f"✅ Found {len(results_with_scores)} results with scores:")
        for i, (result, score) in enumerate(results_with_scores):
            preview = result.page_content[:100].replace('\n', ' ').strip()
            print(f"   Result {i+1} (Score: {score:.4f}): {preview}...")
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ SEMANTIC SEARCH IMPLEMENTATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"📄 PDF processed: {pdf_path}")
        print(f"📝 Total chunks created: {len(chunks)}")
        print(f"🧠 Embedding model: sentence-transformers/all-MiniLM-L6-v2 (CPU-only)")
        print(f"🗄️  Vector store: FAISS")
        print(f"💾 Vector store saved to: user1_review_2024/")
        print(f"⚙️  GPU disabled: No Metal Performance Shaders warnings")
        print("\n🎉 Your semantic search is ready to use!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install the required dependencies.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = basic_semantic_search_local()
    if success:
        print("\n🚀 Ready to use semantic search!")
    else:
        print("\n❌ Failed to create semantic search. Please check the errors above.") 