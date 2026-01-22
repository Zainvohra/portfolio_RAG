#!/usr/bin/env python3
"""
Portfolio Embedding Creator - Creates embeddings for portfolio data from PDF files
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import json

# Add the project root to Python path
# project_root = Path(__file__).parent
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure PyTorch to use CPU to avoid Metal Performance Shaders warnings
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'
os.environ['PYTORCH_MPS_LOW_WATERMARK_RATIO'] = '0.0'
os.environ['PYTORCH_MPS_ALLOCATOR_MAX_CACHED_MEMORY'] = '0'
os.environ['PYTORCH_MPS_ALLOCATOR_MAX_CACHED_MEMORY_PERCENT'] = '0'
os.environ['PYTORCH_DEVICE'] = 'cpu'

from rag.utils.embeddings import EmbeddingManager
from rag.utils.vector_store import VectorStoreManager
from rag.utils.text_chunker import chunk_pdf_documents


class PortfolioEmbeddingCreator:
    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vectorstores = {}
        self.metadata = {}
        
    def process_pdf(self, pdf_path: str, index_name: str = "portfolio_data") -> bool:
        """Process a single PDF file and create embeddings."""
        print(f"\n📄 Processing: {pdf_path}")
        
        if not os.path.exists(pdf_path):
            print(f"❌ Error: PDF file not found at {pdf_path}")
            return False
        
        try:
            # Create chunks from PDF file using existing utilities
            print(f"📖 Loading PDF: {pdf_path}")
            chunks = chunk_pdf_documents(
                pdf_path,
                chunk_size=1000,
                chunk_overlap=200
            )
            print(f"✅ Created {len(chunks)} chunks")
            
            # Create vector store manager
            vs_manager = VectorStoreManager(
                embedding_manager=self.embedding_manager,
                vectorstore_dir_path=os.path.join(project_root, "rag", "vectorstore")
                # vectorstore_dir_path=os.path.join(project_root, "vectorstore")
            )
            
            # Create vector store from chunks
            print("🗄️ Creating FAISS vector store...")
            vectorstore = vs_manager.create_vectorstore_from_chunks(chunks)
            
            # Save vector store
            vs_manager.save_vectorstore(index_name=index_name)
            print(f"✅ Vector store saved as: {index_name}")
            
            # Store metadata
            self.vectorstores[index_name] = {
                'path': f"vectorstore/{index_name}",
                'chunks_count': len(chunks),
                'pdf_path': pdf_path,
                'index_name': index_name
            }
            
            # Save metadata
            self.save_metadata()
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_metadata(self):
        """Save metadata about all processed vector stores."""
        metadata_path = os.path.join(project_root, "vectorstore", "portfolio_metadata.json")
        os.makedirs(os.path.join(project_root, "vectorstore"), exist_ok=True)
        
        with open(metadata_path, 'w') as f:
            json.dump(self.vectorstores, f, indent=2)
        print(f"✅ Metadata saved to: {metadata_path}")
    
    def create_embeddings_for_portfolio(self, pdf_file_path: str, index_name: str = "portfolio_data"):
        """Create embeddings for portfolio data from a PDF file."""
        print("=" * 60)
        print("PORTFOLIO EMBEDDING CREATOR")
        print("=" * 60)
        
        # Process the PDF file
        success = self.process_pdf(pdf_file_path, index_name)
        
        print("\n" + "=" * 60)
        print("EMBEDDING CREATION SUMMARY")
        print("=" * 60)
        
        if success:
            print(f"✅ Successfully processed portfolio data")
            for name, info in self.vectorstores.items():
                print(f"📁 {name}:")
                print(f"   📄 PDF: {info['pdf_path']}")
                print(f"   ✂️  Chunks: {info['chunks_count']}")
                print(f"   💾 Saved to: {info['path']}")
            print("\n🎉 Portfolio embeddings ready!")
        else:
            print("❌ Failed to process portfolio data. Please check the errors above.")
        
        return success


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Create embeddings for portfolio data")
    parser.add_argument(
        "--file",
        type=str,
        default="rag/docs/portfolio_data.pdf",
        # default="docs/portfolio_data.pdf",
        help="Path to the portfolio data PDF file (default: docs/portfolio_data.pdf)"
    )
    parser.add_argument(
        "--index",
        type=str,
        default="portfolio_data",
        help="Index name for the vector store (default: portfolio_data)"
    )
    
    args = parser.parse_args()
    
    # Resolve relative paths relative to the script location
    if not os.path.isabs(args.file):
        args.file = os.path.join(project_root, args.file)
    
    creator = PortfolioEmbeddingCreator()
    success = creator.create_embeddings_for_portfolio(args.file, args.index)
    
    if success:
        print("\n🚀 Portfolio embeddings ready for use!")
    else:
        print("\n❌ Failed to create embeddings. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

