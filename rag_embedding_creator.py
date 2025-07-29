#!/usr/bin/env python3
"""
RAG Embedding Creator - Creates embeddings for multiple PDFs for comparison
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import json

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
os.environ['PYTORCH_DEVICE'] = 'cpu'

class RAGEmbeddingCreator:
    def __init__(self):
        self.embeddings = None
        self.vectorstores = {}
        self.metadata = {}
        
    def initialize_embeddings(self):
        """Initialize HuggingFace embeddings with CPU-only configuration."""
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'device': 'cpu'}
            )
            print("✅ HuggingFace embeddings initialized (CPU-only)")
            return True
        except Exception as e:
            print(f"❌ Error initializing embeddings: {e}")
            return False
    
    def process_pdf(self, pdf_path: str, user_id: str, review_year: str) -> bool:
        """Process a single PDF and create embeddings."""
        print(f"\n📄 Processing: {pdf_path}")
        
        if not os.path.exists(pdf_path):
            print(f"❌ Error: PDF file not found at {pdf_path}")
            return False
        
        try:
            from langchain_community.document_loaders import PyPDFLoader
            from langchain_community.vectorstores import FAISS
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            
            # Load PDF
            print(f"📖 Loading PDF: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            print(f"✅ Loaded {len(documents)} pages")
            
            # Create text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            # Create chunks
            print("✂️ Creating chunks...")
            chunks = text_splitter.split_documents(documents)
            print(f"✅ Created {len(chunks)} chunks")
            
            # Create vector store
            print("🗄️ Creating FAISS vector store...")
            texts = [chunk.page_content for chunk in chunks]
            vectorstore = FAISS.from_texts(texts, self.embeddings)
            
            # Save vector store
            vectorstore_name = f"{user_id}_review_{review_year}"
            vectorstore_path = f"rag/vectorstore/{vectorstore_name}"
            
            # Ensure directory exists
            os.makedirs("rag/vectorstore", exist_ok=True)
            
            vectorstore.save_local(vectorstore_path)
            print(f"✅ Vector store saved to: {vectorstore_path}")
            
            # Store metadata
            self.vectorstores[vectorstore_name] = {
                'path': vectorstore_path,
                'chunks_count': len(chunks),
                'pages_count': len(documents),
                'pdf_path': pdf_path,
                'user_id': user_id,
                'review_year': review_year
            }
            
            # Save metadata
            self.save_metadata()
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
            return False
    
    def save_metadata(self):
        """Save metadata about all processed vector stores."""
        metadata_path = "rag/vectorstore/metadata.json"
        os.makedirs("rag/vectorstore", exist_ok=True)
        
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        print(f"✅ Metadata saved to: {metadata_path}")
    
    def create_embeddings_for_comparison(self):
        """Create embeddings for both review PDFs."""
        print("=" * 60)
        print("RAG EMBEDDING CREATOR - REVIEW COMPARISON")
        print("=" * 60)
        
        # Initialize embeddings
        if not self.initialize_embeddings():
            return False
        
        # Process both PDFs
        pdfs_to_process = [
            {
                'path': 'rag/docs/review_2024.pdf',
                'user_id': 'user1',
                'review_year': '2024'
            },
            {
                'path': 'rag/docs/review_2025.pdf',
                'user_id': 'user1', 
                'review_year': '2025'
            }
        ]
        
        success_count = 0
        for pdf_info in pdfs_to_process:
            if self.process_pdf(pdf_info['path'], pdf_info['user_id'], pdf_info['review_year']):
                success_count += 1
        
        print("\n" + "=" * 60)
        print("EMBEDDING CREATION SUMMARY")
        print("=" * 60)
        print(f"✅ Successfully processed: {success_count}/{len(pdfs_to_process)} PDFs")
        
        for name, info in self.vectorstores.items():
            print(f"📁 {name}:")
            print(f"   📄 PDF: {info['pdf_path']}")
            print(f"   📝 Pages: {info['pages_count']}")
            print(f"   ✂️  Chunks: {info['chunks_count']}")
            print(f"   💾 Saved to: {info['path']}")
        
        print("\n🎉 Embeddings ready for comparison!")
        return success_count == len(pdfs_to_process)

def main():
    creator = RAGEmbeddingCreator()
    success = creator.create_embeddings_for_comparison()
    
    if success:
        print("\n🚀 Ready for review comparison!")
    else:
        print("\n❌ Some PDFs failed to process. Please check the errors above.")

if __name__ == "__main__":
    main() 