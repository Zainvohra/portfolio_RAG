#!/usr/bin/env python3
"""
Semantic chunking and embedding creation for PDF documents.
This script processes PDF files, creates semantic chunks, and generates embeddings.
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

def create_semantic_chunks_and_embeddings():
    """Create semantic chunks and embeddings for the PDF file."""
    
    print("=" * 60)
    print("SEMANTIC CHUNKING AND EMBEDDING CREATION")
    print("=" * 60)
    
    # Configuration
    pdf_path = "rag/docs/review_2024.pdf"
    vectorstore_name = "user1_review_2024"
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        return False
    
    print(f"✅ Found PDF: {pdf_path}")
    
    try:
        # Import required modules
        # from rag.utils.pdf_reader import read_pdf_documents
        # from rag.utils.text_chunker import chunk_pdf_documents
        # from rag.utils.embeddings import EmbeddingManager
        # from rag.utils.vector_store import VectorStoreManager

        from langchain_experimental.text_splitter import SemanticChunker
        from langchain_openai import OpenAIEmbeddings
        
        # Step 1: Load PDF documents
        print("\n📄 Step 1: Loading PDF documents...")
        # documents = read_pdf_documents(pdf_path)
        print(f"✅ Loaded {len(documents)} pages from PDF")
        
        
        # Show page previews
        # for i, doc in enumerate(documents[:3]):  # Show first 3 pages
        #     preview = doc.page_content[:100].replace('\n', ' ').strip()
        #     print(f"   Page {i+1}: {preview}...")
        
        # # Step 2: Create semantic chunks
        # print("\n✂️  Step 2: Creating semantic chunks...")
        # print("   Using RecursiveCharacterTextSplitter with:")
        # print("   - Chunk size: 1000 characters")
        # print("   - Chunk overlap: 200 characters")
        
        # text_splitter = SemanticChunker(
        #     embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        #     breakpoint_threshold_type="percentile",
        # )
        # chunks = text_splitter.create_documents(documents)
        # # chunks = text_splitter.split_documents(documents)
        # # chunks = chunk_pdf_documents(pdf_path, chunk_size=1000, chunk_overlap=200)
        # print(f"✅ Created {len(chunks)} semantic chunks")
        
        # # Show chunk statistics
        # chunk_lengths = [len(chunk.page_content) for chunk in chunks]
        # avg_length = sum(chunk_lengths) / len(chunk_lengths)
        # print(f"   Average chunk length: {avg_length:.1f} characters")
        # print(f"   Shortest chunk: {min(chunk_lengths)} characters")
        # print(f"   Longest chunk: {max(chunk_lengths)} characters")
        
        # # Show sample chunks
        # print("\n📝 Sample chunks:")
        # for i, chunk in enumerate(chunks[:3]):
        #     preview = chunk.page_content[:150].replace('\n', ' ').strip()
        #     print(f"   Chunk {i+1}: {preview}...")
        
        # # Step 3: Initialize embedding manager
        # print("\n🧠 Step 3: Initializing embedding model...")
        # embedding_manager = EmbeddingManager(model_name="sentence-transformers/all-MiniLM-L6-v2")
        # print(f"✅ Using model: sentence-transformers/all-MiniLM-L6-v2")
        
        # # Test embedding creation
        # print("\n🔍 Step 4: Testing embedding creation...")
        # test_chunk = chunks[0].page_content[:200]
        # test_embedding = embedding_manager.create_query_embedding(test_chunk)
        # print(f"✅ Test embedding created successfully")
        # print(f"   Embedding dimensions: {len(test_embedding)}")
        # print(f"   Sample values: {test_embedding[:5]}")
        
        # # Step 5: Create vector store
        # print("\n🗄️  Step 5: Creating FAISS vector store...")
        # vs_manager = VectorStoreManager()
        # vectorstore = vs_manager.create_vectorstore_from_chunks(chunks)
        # print(f"✅ Vector store created successfully")
        
        # # Step 6: Save vector store
        # print(f"\n💾 Step 6: Saving vector store as '{vectorstore_name}'...")
        # vs_manager.save_vectorstore(vectorstore_name)
        # print(f"✅ Vector store saved successfully")
        
        # # Step 7: Verify vector store
        # print(f"\n🔍 Step 7: Verifying vector store...")
        # loaded_vs = vs_manager.load_vectorstore(vectorstore_name)
        # if loaded_vs:
        #     print(f"✅ Vector store loaded successfully")
            
        #     # Test semantic search
        #     test_query = "What is the main topic of this document?"
        #     print(f"\n🔎 Testing semantic search with query: '{test_query}'")
        #     search_results = vs_manager.semantic_search(test_query, k=2)
            
        #     print(f"✅ Found {len(search_results)} relevant results:")
        #     for i, result in enumerate(search_results):
        #         preview = result.page_content[:100].replace('\n', ' ').strip()
        #         print(f"   Result {i+1}: {preview}...")
        # else:
        #     print("❌ Failed to load vector store")
        #     return False
        
        # # Summary
        # print("\n" + "=" * 60)
        # print("✅ SEMANTIC CHUNKING AND EMBEDDING COMPLETED SUCCESSFULLY")
        # print("=" * 60)
        # print(f"📄 PDF processed: {pdf_path}")
        # print(f"📝 Total chunks created: {len(chunks)}")
        # print(f"🧠 Embedding model: sentence-transformers/all-MiniLM-L6-v2")
        # print(f"🗄️  Vector store name: {vectorstore_name}")
        # print(f"💾 Vector store saved to: rag/vectorstore/")
        # print("\n🎉 Your PDF is now ready for semantic search and RAG operations!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install the required dependencies.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = create_semantic_chunks_and_embeddings()
    if success:
        print("\n🚀 Ready to use your embeddings!")
    else:
        print("\n❌ Failed to create embeddings. Please check the errors above.")

