# RAG System Test Suite

This directory contains comprehensive tests for all RAG system components, inspired by the style of `test_agentic_rag.py`. Each test demonstrates practical usage rather than unit testing.

## 🚀 Quick Start

### Run All Tests
```bash
python tests/run_all_tests.py
```

### Run Individual Tests
```bash
# Utils tests
python tests/test_embeddings.py
python tests/test_pdf_reader.py
python tests/test_text_chunker.py
python tests/test_vector_store.py

# Root-level tests
python tests/test_rag_tools.py
python tests/test_simple_rag_agent.py
python tests/test_llm_config.py

# Original test
python tests/test_agentic_rag.py
```

## 📁 Test Files Overview

### Utils Tests

#### `test_embeddings.py`
Tests the embeddings utility with both SentenceTransformers and OpenAI.
- ✅ SentenceTransformer embedding generation (local, free)
- ✅ OpenAI embedding generation (requires API key)
- ✅ Batch processing and caching
- ✅ Similarity calculations and search
- ✅ Cache management and persistence

#### `test_pdf_reader.py`
Tests PDF reading and text extraction capabilities.
- ✅ PDF text extraction
- ✅ Metadata reading
- ✅ Page-specific processing
- ✅ Error handling
- ✅ Content analysis and statistics

#### `test_text_chunker.py`
Tests different text chunking strategies.
- ✅ Recursive chunking with overlap
- ✅ Sentence-based chunking
- ✅ Paragraph-based chunking
- ✅ Semantic chunking with structure detection
- ✅ Chunk statistics and analysis
- ✅ Edge case handling

#### `test_vector_store.py`
Tests advanced vector storage and semantic search.
- ✅ Document storage and indexing
- ✅ Basic vector similarity search
- ✅ Advanced semantic search with query expansion
- ✅ Re-ranking and result diversification
- ✅ Document management operations
- ✅ Persistence and data loading

### Root-Level Tests

#### `test_rag_tools.py`
Tests the RAG tools module using underlying components.
- ✅ PDF reading and text extraction
- ✅ Text chunking with different strategies
- ✅ Embedding generation and vector storage
- ✅ Basic vector similarity search
- ✅ Advanced semantic search with re-ranking
- ✅ Document management and statistics
- ✅ Question answering workflow simulation

#### `test_simple_rag_agent.py`
Tests RAG agent initialization and configuration (simplified).
- ✅ Agent initialization and configuration
- ✅ Tool integration and availability
- ✅ Agent instruction analysis
- ✅ Environment requirements checking
- ✅ Model and API configuration

#### `test_llm_config.py`
Tests LLM configuration and model setup.
- ✅ Environment variable validation
- ✅ Model configuration (Groq, Gemini)
- ✅ OpenAI tracing setup
- ✅ LiteLLM model integration
- ✅ API key management
- ✅ Agent creation with configured models

### Original Test

#### `test_agentic_rag.py`
The original agentic RAG test (already existed).
- ✅ Complete RAG workflow demonstration
- ✅ Agent-based PDF processing and question answering

## 🔧 Setup Requirements

### Required Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Set at least one API key:
```bash
export GROQ_API_KEY="your_groq_key"
export GEMINI_API_KEY="your_gemini_key"
export OPENAI_API_KEY="your_openai_key"  # Optional, for tracing
```

### Optional Test Data
Place a PDF file for testing:
```
docs/employee_handbook.pdf
```

## 📊 Test Runner Features

The `run_all_tests.py` script provides:

- **System Requirements Check**: Validates Python version, dependencies, and API keys
- **Sequential Execution**: Runs all tests in logical order
- **Comprehensive Reporting**: Shows pass/fail status for each test
- **Error Handling**: Captures and displays errors from individual tests
- **Final Summary**: Provides overall results and recommendations

## 🎯 Test Philosophy

These tests follow the philosophy of `test_agentic_rag.py`:

1. **General Tests, Not Unit Tests**: Focus on demonstrating practical usage
2. **Descriptive Output**: Clear, emoji-rich output showing what's being tested
3. **Real Functionality**: Actually run the code to test functionality
4. **Integration Testing**: Test how components work together
5. **User-Friendly**: Provide helpful error messages and setup guidance

## 🔍 Understanding Test Results

### ✅ PASSED
The test completed successfully and demonstrated the expected functionality.

### ❌ FAILED
The test encountered an error. Common causes:
- Missing API keys
- Missing dependencies
- File not found (e.g., PDF for testing)
- Network connectivity issues

### ⚠️ SKIPPED
The test was skipped due to missing requirements but this is expected (e.g., no API key for optional features).

## 💡 Tips

1. **Start with `run_all_tests.py`** to get an overview of system status
2. **Check the requirements section** if tests fail
3. **Run individual tests** to focus on specific components
4. **Review the output** for detailed information about what each test validates
5. **Use the simplified agent test** if you encounter issues with the full agent interaction

## 🆘 Troubleshooting

### Common Issues

**ImportError**: Missing dependencies
```bash
pip install sentence-transformers PyPDF2 openai
```

**API Key Errors**: Missing or invalid API keys
```bash
export GROQ_API_KEY="your_actual_key"
```

**File Not Found**: Missing PDF for testing
```bash
# Place any PDF file as docs/employee_handbook.pdf
```

**Network Errors**: Connectivity issues or rate limiting
- Check internet connection
- Verify API key is valid
- Try again later if rate limited

### Getting Help

1. Review the test output for specific error messages
2. Check the main README.md for system setup instructions
3. Ensure all environment variables are set correctly
4. Verify all dependencies are installed

## 📈 Extending Tests

To add new tests:

1. Create a new test file following the existing pattern
2. Use descriptive print statements with emojis
3. Focus on demonstrating practical usage
4. Add error handling and helpful messages
5. Update `run_all_tests.py` to include the new test 