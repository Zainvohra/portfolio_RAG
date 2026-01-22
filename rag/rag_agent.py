import asyncio
from typing import List, Dict, Any, Optional
from agents import Agent, run_demo_loop
from llm_config import llm_model

# Import our RAG tools
from rag_tools import rag_search_tool


class RAGAgent:
    """Agentic RAG Assistant for PDF processing and question answering."""

    def __init__(self, model=None):
        self.model = model or llm_model

        # Create the agentic RAG assistant with proper tools
        self.agent = Agent(
            name="Employee Handbook RAG Assistant",
            instructions="""You are an intelligent RAG (Retrieval Augmented Generation) assistant specialized in answering questions about the employee handbook.

Your primary function is to help users find information from the company's employee handbook. When users ask questions, you should:

1. Use the rag_search_tool to search the employee handbook content
2. Always use the index name 'employee_handbook' when calling the search tool
3. Provide clear, helpful answers based on the retrieved information
4. If the information isn't found in the handbook, clearly state that
5. Focus only on employee handbook related queries

You have access to semantic search capabilities that can find relevant information even when the exact words don't match the query.
            """,
            model=self.model,
            tools=[
                rag_search_tool
            ]
        )


# Create a global instance
rag_agent = RAGAgent()

if __name__ == "__main__":
    """Run the agentic RAG agent."""
    print("Starting Agentic RAG Assistant...")
    try:
        asyncio.run(run_demo_loop(rag_agent.agent))
    except KeyboardInterrupt:
        print("\n\nSession ended by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
