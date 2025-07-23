#!/usr/bin/env python3
"""
Comprehensive test runner for all RAG system components.
Runs tests for each utils file and root-level files inspired by test_agentic_rag.py.
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path

def run_test_file(test_file, description):
    """Run a single test file and capture its output."""
    
    print(f"\n{'='*80}")
    print(f"🧪 Running {description}")
    print(f"   File: {test_file}")
    print(f"{'='*80}")
    
    try:
        # Get the directory of this script
        test_dir = Path(__file__).parent
        test_path = test_dir / test_file
        
        if not test_path.exists():
            print(f"❌ Test file not found: {test_path}")
            return False
        
        # Run the test file
        result = subprocess.run(
            [sys.executable, str(test_path)],
            capture_output=True,
            text=True,
            cwd=test_dir.parent  # Run from project root
        )
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {str(e)}")
        return False

async def run_async_test_file(test_file, description):
    """Run an async test file."""
    
    print(f"\n{'='*80}")
    print(f"🧪 Running {description} (Async)")
    print(f"   File: {test_file}")
    print(f"{'='*80}")
    
    try:
        # Import and run the test module
        test_dir = Path(__file__).parent
        sys.path.insert(0, str(test_dir))
        
        # Import the test module
        module_name = test_file.replace('.py', '')
        test_module = __import__(module_name)
        
        # Look for the main async function
        if hasattr(test_module, 'run_all_embedding_tests'):
            await test_module.run_all_embedding_tests()
        elif hasattr(test_module, 'run_all_vector_store_tests'):
            await test_module.run_all_vector_store_tests()
        elif hasattr(test_module, 'run_all_llm_config_tests'):
            await test_module.run_all_llm_config_tests()
        else:
            print(f"⚠️  No async test function found in {test_file}")
            return False
        
        print(f"✅ {description} completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error running {description}: {str(e)}")
        return False

def display_banner():
    """Display the test runner banner."""
    
    print("🚀 RAG System Comprehensive Test Suite")
    print("=" * 80)
    print("This will run tests for all RAG system components:")
    print()
    print("📁 Utils Tests:")
    print("   - Embeddings utility (SentenceTransformers & OpenAI)")
    print("   - PDF Reader utility")
    print("   - Text Chunker utility")
    print("   - Vector Store utility")
    print()
    print("🔧 Root-Level Tests:")
    print("   - RAG Tools module")
    print("   - RAG Agent")
    print("   - LLM Configuration")
    print("   - Original agentic RAG test")
    print()
    print("Each test demonstrates practical usage following the style of test_agentic_rag.py")
    print("=" * 80)

def check_requirements():
    """Check system requirements before running tests."""
    
    print("\n🔍 Checking System Requirements")
    print("-" * 40)
    
    requirements = {
        'python': sys.version_info >= (3, 8),
        'dependencies': []
    }
    
    # Check Python version
    if requirements['python']:
        print(f"✅ Python {sys.version.split()[0]} (>= 3.8 required)")
    else:
        print(f"❌ Python {sys.version.split()[0]} (>= 3.8 required)")
    
    # Check for required packages
    required_packages = [
        'asyncio',
        'pathlib',
        'subprocess'
    ]
    
    optional_packages = [
        ('sentence_transformers', 'For local embeddings'),
        ('PyPDF2', 'For PDF processing'),
        ('openai', 'For OpenAI embeddings')
    ]
    
    print("\n📦 Required packages:")
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            requirements['dependencies'].append(package)
    
    print("\n📦 Optional packages:")
    for package, description in optional_packages:
        try:
            __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ⚠️  {package} - {description} (recommended)")
    
    # Check environment variables
    print("\n🔑 Environment Variables:")
    env_vars = ['OPENAI_API_KEY', 'GROQ_API_KEY', 'GEMINI_API_KEY']
    has_api_key = False
    
    for var in env_vars:
        if os.getenv(var):
            print(f"   ✅ {var} is set")
            has_api_key = True
        else:
            print(f"   ⚠️  {var} not set")
    
    if not has_api_key:
        print("   ℹ️  At least one API key is recommended for full functionality")
    
    return len(requirements['dependencies']) == 0

async def run_all_tests():
    """Run all test files in sequence."""
    
    display_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ System requirements not met. Please install missing dependencies.")
        return
    
    print(f"\n{'='*80}")
    print("🚀 Starting Test Execution")
    print(f"{'='*80}")
    
    # Define test files and their descriptions
    sync_tests = [
        ("test_pdf_reader.py", "PDF Reader Utility Tests"),
        ("test_text_chunker.py", "Text Chunker Utility Tests"),
        ("test_rag_tools.py", "RAG Tools Tests"),
        ("test_simple_rag_agent.py", "RAG Agent Tests (Simplified)"),
        ("test_agentic_rag.py", "Original Agentic RAG Tests")
    ]
    
    async_tests = [
        ("test_embeddings.py", "Embeddings Utility Tests"),
        ("test_vector_store.py", "Vector Store Utility Tests"),
        ("test_llm_config.py", "LLM Configuration Tests")
    ]
    
    results = []
    
    # Run synchronous tests
    print("\n📋 Running Synchronous Tests...")
    for test_file, description in sync_tests:
        success = run_test_file(test_file, description)
        results.append((description, success))
    
    # Run asynchronous tests
    print("\n📋 Running Asynchronous Tests...")
    for test_file, description in async_tests:
        try:
            success = await run_async_test_file(test_file, description)
            results.append((description, success))
        except Exception as e:
            print(f"❌ Failed to run {description}: {str(e)}")
            results.append((description, False))
    
    # Display final summary
    print(f"\n{'='*80}")
    print("📊 FINAL TEST SUMMARY")
    print(f"{'='*80}")
    
    passed = 0
    failed = 0
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status:<12} {test_name}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Results: {passed} passed, {failed} failed, {len(results)} total")
    
    if failed == 0:
        print("\n🎉 All tests completed successfully!")
        print("\nKey features validated:")
        print("- ✓ PDF reading and text extraction")
        print("- ✓ Text chunking with multiple strategies")
        print("- ✓ Embedding generation (local and cloud)")
        print("- ✓ Vector storage and semantic search")
        print("- ✓ RAG tools and agent integration")
        print("- ✓ LLM configuration and model setup")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the output above for details.")
        print("\nCommon issues:")
        print("- Missing API keys (set GROQ_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY)")
        print("- Missing dependencies (install with pip install -r requirements.txt)")
        print("- No PDF file for testing (place employee_handbook.pdf in docs/ directory)")
    
    print(f"\n{'='*80}")

def main():
    """Main entry point."""
    
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main() 