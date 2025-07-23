import asyncio
from typing import List, Dict, Any, Optional
from agents import Agent, run_demo_loop
from llm_config import llm_model

# Import our RAG tools
from rag_tools import (
    read_pdf_tool,
    search_documents_tool,
    semantic_search_tool,
    ask_question_tool,
    get_document_stats_tool,
    list_documents_tool
)


class RAGAgent:
    """Agentic RAG Assistant for PDF processing and question answering."""
    
    def __init__(self, model=None):
        self.model = model or llm_model
        
        # Create the agentic RAG assistant with proper tools
        self.agent = Agent(
            name="RAG Assistant",
            instructions="""You are an intelligent RAG (Retrieval Augmented Generation) assistant with access to powerful document processing and search tools.

**CRITICAL WORKFLOW - FOLLOW THIS ORDER:**

1. **ALWAYS START BY CHECKING DOCUMENTS**: Before answering ANY question, use list_documents_tool to check what documents are processed
2. **AUTO-LOAD EMPLOYEE HANDBOOK**: If no documents are processed OR if the employee_handbook is not in the list, automatically process 'docs/employee_handbook.pdf' using read_pdf_tool
3. **THEN ANSWER QUESTIONS**: After ensuring documents are processed, use ask_question_tool to answer the user's question

**Your capabilities include:**
1. **Processing PDF documents** - Use read_pdf_tool to process and index PDF files
2. **Basic document search** - Use search_documents_tool for simple vector similarity search
3. **Advanced semantic search** - Use semantic_search_tool for enhanced search with query expansion and re-ranking
4. **Answering questions** - Use ask_question_tool to answer questions based on document content (uses advanced search by default)
5. **Document management** - Use get_document_stats_tool and list_documents_tool to manage processed documents

**MANDATORY STARTUP SEQUENCE FOR EVERY QUERY:**
```
Step 1: Call list_documents_tool() to check processed documents
Step 2: If employee_handbook is NOT in the list, call read_pdf_tool("docs/employee_handbook.pdf")
Step 3: Then proceed with answering the user's question using ask_question_tool()
```

**For any user question:**
- FIRST: Check processed documents with list_documents_tool
- IF NEEDED: Process employee handbook with read_pdf_tool
- THEN: Answer using ask_question_tool with retrieved context
- ALWAYS provide comprehensive answers with sources and similarity scores

**Be proactive and autonomous:**
- Automatically ensure the employee handbook is processed before answering questions
- Use advanced semantic search for complex or ambiguous queries
- If no relevant information is found, clearly explain this and suggest processing more documents
- Cite sources, similarity scores, and re-ranking scores when providing answers
- Never skip the document checking step - this is mandatory for every interaction

You must follow this workflow religiously to ensure users get accurate answers based on processed documents.""",
            model=self.model,
            tools=[
                read_pdf_tool,
                search_documents_tool,
                semantic_search_tool,
                ask_question_tool,
                get_document_stats_tool,
                list_documents_tool
            ]
        )
    
    async def run_interactive(self):
        """Run interactive RAG session using the agentic framework."""
        print("🤖 Agentic RAG Assistant started! Ask me anything about documents or mention a PDF to process.\n")
        print("💡 I can automatically:")
        print("   - Process PDF files you mention")
        print("   - Search through processed documents (basic vector search)")
        print("   - Advanced semantic search with query expansion and re-ranking")
        print("   - Answer questions using retrieved context")
        print("   - Manage your document knowledge base")
        print("\nType your question (or 'quit' to exit).\n")
        await run_demo_loop(self.agent)


# Create a global instance
rag_agent = RAGAgent()


if __name__ == "__main__":
    """Run the agentic RAG agent."""
    print("Starting Agentic RAG Assistant...")
    try:
        asyncio.run(rag_agent.run_interactive())
    except KeyboardInterrupt:
        print("\n\nSession ended by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure you have:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Set your GROQ_API_KEY environment variable") 
        print("3. Have a PDF file in the current directory") 