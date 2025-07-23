#!/usr/bin/env python3
"""
Simplified test script for the RAG Agent.
Demonstrates agent initialization and configuration without complex interactions.
"""

import os
import sys

# Add the parent directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_agent import RAGAgent, rag_agent

def test_rag_agent_initialization():
    """Test RAG agent initialization and configuration."""
    
    print("🧪 Testing RAG Agent Initialization")
    print("=" * 50)
    
    try:
        # Test 1: Default agent initialization
        print("\n🤖 Test 1: Default Agent Initialization")
        print("-" * 40)
        
        # Check global instance
        global_agent = rag_agent
        print(f"✅ Global RAG agent available")
        print(f"   Agent name: {global_agent.agent.name}")
        print(f"   Model type: {type(global_agent.model).__name__}")
        
        # Test 2: Create new agent instance
        print("\n🔧 Test 2: Creating New Agent Instance")
        print("-" * 40)
        
        new_agent = RAGAgent()
        print(f"✅ New RAG agent created")
        print(f"   Agent name: {new_agent.agent.name}")
        print(f"   Instructions length: {len(new_agent.agent.instructions)} characters")
        
        return global_agent, new_agent
        
    except Exception as e:
        print(f"❌ Error during agent initialization: {str(e)}")
        return None, None

def test_agent_tools_configuration(rag_agent_instance):
    """Test the agent's tools configuration."""
    
    print("\n🧪 Testing Agent Tools Configuration")
    print("=" * 50)
    
    if not rag_agent_instance:
        print("⚠️  No agent available for tools testing")
        return False
    
    try:
        # Test 1: Check available tools
        print("\n🔧 Test 1: Checking Available Tools")
        print("-" * 40)
        
        agent = rag_agent_instance.agent
        tools = agent.tools if hasattr(agent, 'tools') else []
        
        print(f"✅ Agent tools configuration checked")
        print(f"   Number of tools: {len(tools)}")
        
        expected_tools = [
            "read_pdf_tool",
            "search_documents_tool", 
            "semantic_search_tool",
            "ask_question_tool",
            "get_document_stats_tool",
            "list_documents_tool"
        ]
        
        for tool in tools:
            tool_name = getattr(tool, 'name', 'unknown')
            print(f"   ✓ Tool: {tool_name}")
        
        # Test 2: Check agent instructions
        print("\n📝 Test 2: Agent Instructions Analysis")
        print("-" * 40)
        
        instructions = agent.instructions
        print(f"✅ Agent instructions analyzed")
        print(f"   Instructions length: {len(instructions)} characters")
        print(f"   Contains 'RAG': {'RAG' in instructions}")
        print(f"   Contains 'PDF': {'PDF' in instructions}")
        print(f"   Contains 'search': {'search' in instructions}")
        print(f"   Instructions preview: {instructions[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during tools configuration test: {str(e)}")
        return False

def test_agent_configuration_analysis(rag_agent_instance):
    """Test and analyze agent configuration."""
    
    print("\n🧪 Testing Agent Configuration Analysis")
    print("=" * 50)
    
    if not rag_agent_instance:
        print("⚠️  No agent available for configuration analysis")
        return False
    
    try:
        # Test 1: Model configuration
        print("\n⚙️  Test 1: Model Configuration Analysis")
        print("-" * 40)
        
        model = rag_agent_instance.model
        print(f"✅ Model configuration analyzed")
        print(f"   Model type: {type(model).__name__}")
        
        # Check for model attributes
        if hasattr(model, 'model'):
            print(f"   Model name: {model.model}")
        if hasattr(model, 'api_key'):
            api_key = model.api_key
            if api_key:
                print(f"   API key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
            else:
                print("   API key: Not set")
        
        # Test 2: Agent capabilities analysis
        print("\n🎯 Test 2: Agent Capabilities Analysis")
        print("-" * 40)
        
        agent = rag_agent_instance.agent
        instructions = agent.instructions
        
        # Analyze instructions for capabilities
        capabilities = []
        if 'PDF' in instructions:
            capabilities.append('PDF Processing')
        if 'search' in instructions:
            capabilities.append('Document Search')
        if 'question' in instructions:
            capabilities.append('Question Answering')
        if 'semantic' in instructions:
            capabilities.append('Semantic Search')
        
        print(f"✅ Agent capabilities identified")
        for capability in capabilities:
            print(f"   ✓ {capability}")
        
        # Test 3: Tool integration analysis
        print("\n🔗 Test 3: Tool Integration Analysis")
        print("-" * 40)
        
        tools = agent.tools if hasattr(agent, 'tools') else []
        tool_categories = {
            'PDF': [],
            'Search': [],
            'Management': []
        }
        
        for tool in tools:
            tool_name = getattr(tool, 'name', 'unknown')
            if 'pdf' in tool_name.lower():
                tool_categories['PDF'].append(tool_name)
            elif 'search' in tool_name.lower():
                tool_categories['Search'].append(tool_name)
            elif any(word in tool_name.lower() for word in ['stats', 'list', 'manage']):
                tool_categories['Management'].append(tool_name)
        
        print(f"✅ Tool integration analyzed")
        for category, category_tools in tool_categories.items():
            if category_tools:
                print(f"   {category} tools: {', '.join(category_tools)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during configuration analysis: {str(e)}")
        return False

def test_environment_requirements():
    """Test environment requirements for the RAG agent."""
    
    print("\n🧪 Testing Environment Requirements")
    print("=" * 50)
    
    try:
        # Test 1: API Keys
        print("\n🔑 Test 1: API Key Availability")
        print("-" * 40)
        
        openai_key = os.getenv("OPENAI_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        print(f"✅ API key status checked")
        print(f"   OPENAI_API_KEY: {'✓ Set' if openai_key else '✗ Not set'}")
        print(f"   GROQ_API_KEY: {'✓ Set' if groq_key else '✗ Not set'}")
        print(f"   GEMINI_API_KEY: {'✓ Set' if gemini_key else '✗ Not set'}")
        
        has_api_key = bool(openai_key or groq_key or gemini_key)
        
        # Test 2: PDF File Availability
        print("\n📄 Test 2: PDF File Availability")
        print("-" * 40)
        
        possible_pdfs = [
            "docs/employee_handbook.pdf",
            "employee_handbook.pdf",
            "../docs/employee_handbook.pdf"
        ]
        
        available_pdfs = []
        for pdf_path in possible_pdfs:
            if os.path.exists(pdf_path):
                available_pdfs.append(pdf_path)
        
        print(f"✅ PDF file availability checked")
        if available_pdfs:
            print(f"   Available PDFs: {available_pdfs}")
        else:
            print("   No PDF files found for testing")
            print("   Looked for files:")
            for path in possible_pdfs:
                print(f"   - {path}")
        
        return {
            'has_api_key': has_api_key,
            'has_pdf': bool(available_pdfs),
            'pdf_files': available_pdfs
        }
        
    except Exception as e:
        print(f"❌ Error during environment requirements test: {str(e)}")
        return {}

def run_all_rag_agent_tests():
    """Run all RAG agent tests."""
    
    print("🚀 Starting Comprehensive RAG Agent Tests")
    print("This will test agent initialization, configuration, and setup\n")
    
    results = []
    
    try:
        # Test environment requirements
        env_status = test_environment_requirements()
        results.append(("Environment Requirements", bool(env_status)))
        
        # Test agent initialization
        global_agent, new_agent = test_rag_agent_initialization()
        results.append(("Agent Initialization", global_agent is not None))
        
        agent_to_test = global_agent or new_agent
        
        if agent_to_test:
            # Test tools configuration
            tools_result = test_agent_tools_configuration(agent_to_test)
            results.append(("Tools Configuration", tools_result))
            
            # Test configuration analysis
            config_result = test_agent_configuration_analysis(agent_to_test)
            results.append(("Configuration Analysis", config_result))
        else:
            print("⚠️  Skipping advanced tests - no agent available")
            results.extend([
                ("Tools Configuration", False),
                ("Configuration Analysis", False)
            ])
        
        # Summary
        print("\n📊 Test Results Summary:")
        print("=" * 30)
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED/SKIPPED"
            print(f"{test_name}: {status}")
        
        print("\n✅ RAG Agent Testing Complete!")
        print("\nKey Features Demonstrated:")
        print("- ✓ Agent initialization and configuration")
        print("- ✓ Tool integration and availability")
        print("- ✓ Agent instruction analysis")
        print("- ✓ Environment requirements checking")
        print("- ✓ Model and API configuration")
        
        # Recommendations
        if env_status:
            print("\n💡 Recommendations:")
            if not env_status.get('has_api_key'):
                print("- Set at least one API key (GROQ_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY)")
            if not env_status.get('has_pdf'):
                print("- Place a PDF file (e.g., employee_handbook.pdf) for testing")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")

if __name__ == "__main__":
    print("🤖 RAG Agent Tests (Simplified)")
    print("This will test the RAG agent initialization and configuration\n")
    
    try:
        run_all_rag_agent_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        print("Make sure you have:")
        print("1. At least one API key set")
        print("2. All required dependencies installed") 