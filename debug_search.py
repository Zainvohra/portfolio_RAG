#!/usr/bin/env python3
"""
Debug script to test vector store loading and search
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure PyTorch to use CPU
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'
os.environ['PYTORCH_MPS_LOW_WATERMARK_RATIO'] = '0.0'
os.environ['PYTORCH_MPS_ALLOCATOR_MAX_CACHED_MEMORY'] = '0'
os.environ['PYTORCH_MPS_ALLOCATOR_MAX_CACHED_MEMORY_PERCENT'] = '0'
os.environ['PYTORCH_DEVICE'] = 'cpu'

def debug_vectorstore():
    """Debug vector store loading and search"""
    try:
        from rag.utils import VectorStoreManager
        
        print("🔍 Debugging VectorStoreManager...")
        
        # Initialize
        vs_manager = VectorStoreManager()
        print("✅ VectorStoreManager initialized")
        
        # Try to load the vector store
        index_name = "user1_review_2024"
        print(f"📁 Loading vector store: {index_name}")
        
        vectorstore = vs_manager.load_vectorstore(index_name)
        
        if vectorstore is None:
            print("❌ Failed to load vector store")
            return
        
        print("✅ Vector store loaded successfully")
        
        # Try a simple search
        print("🔍 Testing semantic search...")
        results = vs_manager.semantic_search("test", k=1)
        print(f"📊 Search returned {len(results)} results")
        
        if results:
            print("✅ Search is working")
            print(f"📝 First result: {results[0].page_content[:100]}...")
        else:
            print("⚠️  Search returned no results")
            
            # Try to get all documents
            print("🔍 Trying to get all documents...")
            all_results = vs_manager.semantic_search("", k=1000)
            print(f"📊 Total documents in store: {len(all_results)}")
            
            if all_results:
                print("✅ Documents found in store")
                print(f"📝 Sample content: {all_results[0].page_content[:200]}...")
            else:
                print("❌ No documents found in store")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_vectorstore() 