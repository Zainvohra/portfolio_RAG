#!/usr/bin/env python3
"""
Search Tool - Implement the same approach as rag_search_tool
Uses VectorStoreManager to fetch answers for queries
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import json

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


def search_tool(index_name: str, query: str, k: int = 3) -> Dict[str, Any]:
    """
    Load a vector store by index name and perform semantic search on the query.
    Same approach as rag_search_tool in rag_tools.py
    
    Args:
        index_name (str): Name of the vector store index to load
        query (str): User query to search for
        k (int): Number of results to return (default: 3)
        
    Returns:
        Dict[str, Any]: Search results with status and documents
    """
    try:
        print("🔍 Called with params: ", index_name, query)
        
        # Import VectorStoreManager (same as rag_tools.py)
        from rag.utils import VectorStoreManager
        
        # Initialize vector store manager (same approach)
        vs_manager = VectorStoreManager()
        
        # Load the vector store (same method)
        vectorstore = vs_manager.load_vectorstore(index_name)
        
        if vectorstore is None:
            return {
                "status": "error",
                "message": f"Failed to load vector store with index '{index_name}'. Please ensure the index exists.",
                "results": []
            }
        
        # Perform semantic search (same method)
        search_results = vs_manager.semantic_search(query, k=k)
        
        # Format results (same approach)
        formatted_results = []
        for i, doc in enumerate(search_results):
            formatted_results.append({
                "rank": i + 1,
                "content": doc.page_content,
                "metadata": getattr(doc, 'metadata', {})
            })
        
        return {
            "status": "success",
            "message": f"Found {len(formatted_results)} results for query: '{query}'",
            "results": formatted_results,
            "query": query,
            "index_used": index_name
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during search: {str(e)}",
            "results": []
        }


class SearchTool:
    """Search tool class that implements the same approach as rag_search_tool"""
    
    def __init__(self):
        self.vs_manager = None
        
    def initialize(self):
        """Initialize the VectorStoreManager"""
        try:
            from rag.utils import VectorStoreManager
            self.vs_manager = VectorStoreManager()
            print("✅ VectorStoreManager initialized")
            return True
        except Exception as e:
            print(f"❌ Error initializing VectorStoreManager: {e}")
            return False
    
    def search(self, index_name: str, query: str, k: int = 3) -> Dict[str, Any]:
        """
        Search using the same approach as rag_search_tool
        
        Args:
            index_name (str): Name of the vector store index to load
            query (str): User query to search for
            k (int): Number of results to return (default: 3)
            
        Returns:
            Dict[str, Any]: Search results with status and documents
        """
        return search_tool(index_name, query, k)
    
    def search_user1_review(self, review_year: str, query: str, k: int = 3) -> Dict[str, Any]:
        """
        Search user1's review for a specific year
        
        Args:
            review_year (str): Review year (e.g., '2024', '2025')
            query (str): User query to search for
            k (int): Number of results to return (default: 3)
            
        Returns:
            Dict[str, Any]: Search results with status and documents
        """
        index_name = f"user1_review_{review_year}"
        return self.search(index_name, query, k)
    
    def interactive_search(self):
        """Run interactive search mode"""
        print("=" * 60)
        print("🔍 SEARCH TOOL")
        print("=" * 60)
        print("Search vector stores using the same approach as rag_search_tool")
        print("Type 'quit' to exit")
        print("=" * 60)
        
        while True:
            try:
                # Get user input
                user_input = input("\n❓ Enter search query (or 'quit'): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if not user_input:
                    print("Please enter a query.")
                    continue
                
                # Parse query and index
                parts = user_input.split('|', 1)
                if len(parts) == 2:
                    index_name = parts[0].strip()
                    query = parts[1].strip()
                else:
                    # Use user1_review_2024 as default
                    index_name = "user1_review_2024"
                    query = user_input
                
                # Perform search
                result = self.search(index_name, query)
                
                print("\n" + "=" * 60)
                print("🔍 SEARCH RESULTS:")
                print("=" * 60)
                
                if result["status"] == "success":
                    print(f"✅ {result['message']}")
                    print(f"📊 Index used: {result['index_used']}")
                    print(f"🔍 Query: '{result['query']}'")
                    print("\n📝 Results:")
                    
                    for i, doc in enumerate(result["results"]):
                        print(f"\n{i+1}. Rank {doc['rank']}:")
                        content = doc['content'][:300].replace('\n', ' ').strip()
                        print(f"   {content}...")
                        
                        if doc['metadata']:
                            print(f"   📋 Metadata: {doc['metadata']}")
                else:
                    print(f"❌ {result['message']}")
                
                print("=" * 60)
                
                # Save results to file
                self.save_search_result(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return True
    
    def save_search_result(self, result: Dict[str, Any]):
        """Save search results to a file"""
        try:
            os.makedirs("search_results", exist_ok=True)
            
            timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_results/search_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")


def main():
    """Main function to run the search tool"""
    search_tool_instance = SearchTool()
    
    # Check if command line arguments are provided
    if len(sys.argv) > 2:
        index_name = sys.argv[1]
        query = sys.argv[2]
        k = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        
        result = search_tool(index_name, query, k)
        print(json.dumps(result, indent=2))
    else:
        # Run interactive mode
        search_tool_instance.interactive_search()


if __name__ == "__main__":
    main() 