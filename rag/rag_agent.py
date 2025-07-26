import asyncio
from typing import List, Dict, Any, Optional
from agents import Agent, run_demo_loop
from llm_config import llm_model

# Import our RAG tools
from rag_tools import (
)


class RAGAgent:
    """Agentic RAG Assistant for PDF processing and question answering."""

    def __init__(self, model=None):
        self.model = model or llm_model

        # Create the agentic RAG assistant with proper tools
        self.agent = Agent(
            name="RAG Assistant",
            instructions="""You are an intelligent RAG (Retrieval Augmented Generation) assistant with access to powerful document processing and search tools.
    
            """,
            model=self.model,
            tools=[
                rag_tools
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