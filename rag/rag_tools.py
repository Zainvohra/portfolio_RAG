from typing import List, Dict, Any
from agents import function_tool
from utils import VectorStoreManager



@function_tool
def rag_search_tool(index_name: str, query: str, k: int = 3) -> Dict[str, Any]:
    """
    Load a vector store by index name and perform semantic search on the query.
    
    Args:
        index_name (str): Name of the vector store index to load
        query (str): User query to search for
        k (int): Number of results to return (default: 3)
        
    Returns:
        Dict[str, Any]: Search results with status and documents
    """
    try:
        print("Called with params: ", index_name, query)
        # Initialize vector store manager
        vs_manager = VectorStoreManager()
        
        # Load the vector store
        vectorstore = vs_manager.load_vectorstore(index_name)
        
        if vectorstore is None:
            return {
                "status": "error",
                "message": f"Failed to load vector store with index '{index_name}'. Please ensure the index exists.",
                "results": []
            }
        
        # Perform semantic search
        search_results = vs_manager.semantic_search(query, k=k)
        
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


# Export the tool for agent use
rag_tools = [rag_search_tool]
