#!/usr/bin/env python3
"""
Test script for the Agentic RAG implementation.
Demonstrates how the agent automatically uses tools to process PDFs and answer questions.
"""

import asyncio
import os
import sys

# Add the parent directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import Runner
from rag_agent import rag_agent

# Please run tests from the project root using a test runner like `pytest`.
# This ensures all imports work as expected without modifying sys.path.
async def test_agentic_rag():
    """Test the agentic RAG implementation."""
    
    print("🧪 Testing Agentic RAG Implementation")
    print("=" * 50)
    
    # # Test 1: Ask the agent to process the employee handbook
    # print("\n📖 Test 1: Processing Employee Handbook")
    # print("-" * 40)
    
    # # The agent should automatically use read_pdf_tool when we mention the PDF
    # result1 = await Runner.run(
    #     rag_agent.agent,
    #     "Please process the employee_handbook.pdf file and tell me what you found."
    # )
    # print(f"Agent Response 1:\n{result1}\n")
    
    # Test: Combined processing and question
    print("\n❓ Test: Process PDF and Answer Question")
    print("-" * 40)
    
    # First, ask the agent to process the PDF
    print("📖 Processing employee handbook...")
    result1 = await Runner.run(
        rag_agent.agent,
        "Please process the docs/employee_handbook.pdf file."
    )
    print(f"Processing Response:\n{result1}\n")
    
    # Then ask about the vacation policy
    print("❓ Asking about vacation policy...")
    result2 = await Runner.run(
        rag_agent.agent,
        "What is the company's vacation policy?"
    )
    print(f"Vacation Policy Response:\n{result2}\n")
    
    # # Test 3: Search for specific information
    # print("\n🔍 Test 3: Searching for Benefits Information")
    # print("-" * 40)
    
    # # The agent should automatically use search_documents_tool
    # result3 = await Runner.run(
    #     rag_agent.agent,
    #     "Search for information about employee benefits and health insurance."
    # )
    # print(f"Agent Response 3:\n{result3}\n")
    
    # # Test 4: Check document stats
    # print("\n📊 Test 4: Checking Document Statistics")
    # print("-" * 40)
    
    # # The agent should automatically use get_document_stats_tool
    # result4 = await Runner.run(
    #     rag_agent.agent,
    #     "Show me statistics about the processed documents."
    # )
    # print(f"Agent Response 4:\n{result4}\n")
    
    # # Test 5: Complex question requiring context
    # print("\n🧠 Test 5: Complex Question with Context")
    # print("-" * 40)
    
    # # The agent should automatically search and provide contextual answer
    # result5 = await Runner.run(
    #     rag_agent.agent,
    #     "What are the procedures for requesting time off? Include any approval processes and deadlines."
    # )
    # print(f"Agent Response 5:\n{result5}\n")
    
    # print("✅ Agentic RAG Testing Complete!")
    # print("\nKey Features Demonstrated:")
    # print("- ✓ Automatic PDF processing when files are mentioned")
    # print("- ✓ Intelligent tool selection for different query types")
    # print("- ✓ Contextual document search and retrieval")
    # print("- ✓ Question answering with relevant context")
    # print("- ✓ Document management and statistics")


async def interactive_demo_loop():
    """Interactive demo loop for testing the RAG system using the SDK's run_demo_loop."""
    

    # Use the existing run_interactive method from rag_agent
    await rag_agent.run_interactive()


if __name__ == "__main__":
    print("🚀 Starting Agentic RAG Tests")
    print("This will demonstrate how the agent automatically uses tools\n")
    
    try:
        # asyncio.run(interactive_demo_loop())
        asyncio.run(test_agentic_rag())

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        print("Make sure you have:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Set your GROQ_API_KEY environment variable")
        print("3. The employee_handbook.pdf file in the current directory") 


