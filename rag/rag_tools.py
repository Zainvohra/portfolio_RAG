from typing import List, Dict, Any
from agents import function_tool
from rag.utils import VectorStoreManager

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


@function_tool
def rag_review_tool(query: str, review_year: str = "2024", k: int = 3) -> Dict[str, Any]:
    """
    Search in user1's performance reviews (2024 and 2025).
    
    Args:
        query (str): User query to search for in reviews
        review_year (str): Review year to search in ("2024" or "2025")
        k (int): Number of results to return (default: 3)
        
    Returns:
        Dict[str, Any]: Search results with status and documents
    """
    try:
        print(f"Review search called with params: {review_year}, {query}")
        
        # Validate review year
        if review_year not in ["2024", "2025"]:
            return {
                "status": "error",
                "message": f"Invalid review year '{review_year}'. Must be '2024' or '2025'.",
                "results": []
            }
        
        # Initialize vector store manager
        vs_manager = VectorStoreManager()
        
        # Construct index name
        index_name = f"user1_review_{review_year}"
        
        # Load the vector store
        vectorstore = vs_manager.load_vectorstore(index_name)
        
        if vectorstore is None:
            return {
                "status": "error",
                "message": f"Failed to load user1 review for {review_year}. Please ensure the review exists.",
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
                "metadata": getattr(doc, 'metadata', {}),
                "review_year": review_year
            })
        
        return {
            "status": "success",
            "message": f"Found {len(formatted_results)} results in user1's {review_year} review for query: '{query}'",
            "results": formatted_results,
            "query": query,
            "review_year": review_year,
            "index_used": index_name
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during review search: {str(e)}",
            "results": []
        }


@function_tool
def rag_review_comparison_tool(query: str, k: int = 3) -> Dict[str, Any]:
    """
    Compare user1's performance reviews (2024 vs 2025) for the same query.
    Perfect for finding new tools, skills, or changes between reviews.
    
    Args:
        query (str): User query to search for in both reviews
        k (int): Number of results to return per review (default: 3)
        
    Returns:
        Dict[str, Any]: Comparison results with both 2024 and 2025 findings
    """
    try:
        print(f"Review comparison called with params: {query}")
        
        # Initialize vector store manager
        vs_manager = VectorStoreManager()
        
        comparison_results = {
            "status": "success",
            "message": f"Comparison results for query: '{query}'",
            "query": query,
            "2024_review": {"results": [], "index_used": "user1_review_2024"},
            "2025_review": {"results": [], "index_used": "user1_review_2025"}
        }
        
        # Search in both reviews
        for review_year in ["2024", "2025"]:
            index_name = f"user1_review_{review_year}"
            
            # Load the vector store
            vectorstore = vs_manager.load_vectorstore(index_name)
            
            if vectorstore is None:
                comparison_results[f"{review_year}_review"]["error"] = f"Failed to load {review_year} review"
                continue
            
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
            
            comparison_results[f"{review_year}_review"]["results"] = formatted_results
            comparison_results[f"{review_year}_review"]["count"] = len(formatted_results)
        
        return comparison_results
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during review comparison: {str(e)}",
            "query": query
        }


# Export the tools for agent use
rag_tools = [rag_search_tool, rag_review_tool, rag_review_comparison_tool]
