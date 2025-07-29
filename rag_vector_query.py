#!/usr/bin/env python3
"""
RAG Vector Query - Query embedding vector stores using the same method as RAGAgent
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

class RAGVectorQuery:
    """Query embedding vector stores using the same method as RAGAgent."""
    
    def __init__(self):
        self.vectorstore_manager = None
        
    def initialize_vectorstore_manager(self):
        """Initialize the vector store manager."""
        try:
            from rag.utils import VectorStoreManager
            
            self.vectorstore_manager = VectorStoreManager()
            print("✅ Vector store manager initialized")
            return True
        except Exception as e:
            print(f"❌ Error initializing vector store manager: {e}")
            return False
    
    def query_vectorstore(self, index_name: str, query: str, k: int = 3) -> Dict[str, Any]:
        """
        Query a user review vector store using the same method as RAGAgent.
        
        Args:
            index_name (str): Name of the user review vector store index to load
            query (str): User query to search for
            k (int): Number of results to return (default: 3)
            
        Returns:
            Dict[str, Any]: Search results with status and documents
        """
        try:
            print(f"🔍 Querying user review vector store '{index_name}' with query: '{query}'")
            
            # Load the vector store
            vectorstore = self.vectorstore_manager.load_vectorstore(index_name)
            
            if vectorstore is None:
                return {
                    "status": "error",
                    "message": f"Failed to load user review vector store with index '{index_name}'. Please ensure the index exists.",
                    "results": []
                }
            
            # Perform semantic search
            search_results = self.vectorstore_manager.semantic_search(query, k=k)
            
            # Format results
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
    
    def list_available_indexes(self) -> List[str]:
        """List all available vector store indexes for user1."""
        try:
            vectorstore_dir = "rag/vectorstore"
            if not os.path.exists(vectorstore_dir):
                return []
            
            indexes = []
            for item in os.listdir(vectorstore_dir):
                if item.endswith('.faiss'):
                    index_name = item.replace('.faiss', '')
                    # Only show user1 review indexes
                    if index_name.startswith('user1_review'):
                        indexes.append(index_name)
            
            return indexes
        except Exception as e:
            print(f"❌ Error listing indexes: {e}")
            return []
    
    def interactive_query_mode(self):
        """Run interactive query mode."""
        print("=" * 60)
        print("🔍 USER1 REVIEW VECTOR QUERY TOOL")
        print("=" * 60)
        print("Query user1 review embedding vector stores using the same method as RAGAgent.")
        print("Type 'quit' to exit, 'list' to see available user1 review indexes.")
        print("=" * 60)
        
        # Initialize
        if not self.initialize_vectorstore_manager():
            print("❌ Failed to initialize vector store manager.")
            return False
        
        # List available indexes
        indexes = self.list_available_indexes()
        if not indexes:
            print("❌ No user1 review vector store indexes found. Please create embeddings first.")
            print("   Expected format: user1_review_2024, user1_review_2025, etc.")
            return False
        
        print(f"✅ Available user1 review indexes: {', '.join(indexes)}")
        
        while True:
            try:
                # Get user input
                user_input = input("\n❓ Enter query (or 'list'/'quit'): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'list':
                    indexes = self.list_available_indexes()
                    print(f"\n📋 Available user1 review indexes: {', '.join(indexes)}")
                    continue
                
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
                
                # Perform query
                result = self.query_vectorstore(index_name, query)
                
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
                self.save_query_result(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return True
    
    def save_query_result(self, result: Dict[str, Any]):
        """Save query results to a file."""
        try:
            os.makedirs("rag/query_results", exist_ok=True)
            
            timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rag/query_results/query_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")
    
    def batch_query(self, index_name: str, queries: List[str], k: int = 3) -> List[Dict[str, Any]]:
        """
        Perform batch queries on a user review vector store.
        
        Args:
            index_name (str): Name of the user review vector store index
            queries (List[str]): List of queries to perform
            k (int): Number of results per query
            
        Returns:
            List[Dict[str, Any]]: List of query results
        """
        results = []
        
        for i, query in enumerate(queries):
            print(f"🔍 Processing query {i+1}/{len(queries)}: '{query}'")
            result = self.query_vectorstore(index_name, query, k)
            results.append(result)
        
        return results
    
    def query_user1_review(self, review_year: str, query: str, k: int = 3) -> Dict[str, Any]:
        """
        Query user1's review for a specific year.
        
        Args:
            review_year (str): Review year (e.g., '2024', '2025')
            query (str): Query to search for
            k (int): Number of results to return
            
        Returns:
            Dict[str, Any]: Search results with status and documents
        """
        index_name = f"user1_review_{review_year}"
        return self.query_vectorstore(index_name, query, k)
    
    def get_user1_review_summary(self, review_year: str) -> Dict[str, Any]:
        """
        Get a summary of user1's review for a specific year.
        
        Args:
            review_year (str): Review year (e.g., '2024', '2025')
            
        Returns:
            Dict[str, Any]: Summary information about the review
        """
        index_name = f"user1_review_{review_year}"
        
        try:
            vectorstore = self.vectorstore_manager.load_vectorstore(index_name)
            if vectorstore is None:
                return {
                    "status": "error",
                    "message": f"User1 review '{index_name}' not found",
                    "review_year": review_year
                }
            
            # Get all documents to create summary
            all_docs = self.vectorstore_manager.semantic_search("", k=1000)  # Get all docs
            
            return {
                "status": "success",
                "message": f"Found user1 review for {review_year}",
                "review_year": review_year,
                "total_chunks": len(all_docs),
                "index_name": index_name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error accessing user1 review: {str(e)}",
                "review_year": review_year
            }


def main():
    """Main function to run the User1 Review Vector Query tool."""
    query_tool = RAGVectorQuery()
    
    # Check if command line arguments are provided
    if len(sys.argv) > 2:
        index_name = sys.argv[1]
        query = sys.argv[2]
        k = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        
        if query_tool.initialize_vectorstore_manager():
            result = query_tool.query_vectorstore(index_name, query, k)
            print(json.dumps(result, indent=2))
        else:
            print("❌ Failed to initialize vector store manager.")
    else:
        # Run interactive mode
        query_tool.interactive_query_mode()


if __name__ == "__main__":
    main() 