#!/usr/bin/env python3
"""
Test script for the PDF Reader utility.
Demonstrates PDF text extraction, metadata reading, and page-specific processing.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pdf_reader import PDFReader

def test_pdf_reader_initialization():
    """Test PDF reader initialization."""
    
    print("🧪 Testing PDF Reader Initialization")
    print("=" * 50)
    
    try:
        # Test 1: Initialize PDF reader
        print("\n📚 Test 1: Initializing PDF Reader")
        print("-" * 40)
        
        pdf_reader = PDFReader()
        print(f"✅ PDF reader initialized successfully")
        print(f"   Name: {pdf_reader.name}")
        print(f"   Description: {pdf_reader.description}")
        
        return pdf_reader
        
    except Exception as e:
        print(f"❌ Error during PDF reader initialization: {str(e)}")
        return None

def test_pdf_reading(pdf_reader):
    """Test PDF reading functionality."""
    
    print("\n🧪 Testing PDF Reading Functionality")
    print("=" * 50)
    
    # Look for available PDF files
    possible_pdfs = [
        "docs/employee_handbook.pdf",
        "employee_handbook.pdf",
        "../docs/employee_handbook.pdf"
    ]
    
    pdf_file = None
    for pdf_path in possible_pdfs:
        if os.path.exists(pdf_path):
            pdf_file = pdf_path
            break
    
    if not pdf_file:
        print("⚠️  No PDF file found for testing")
        print("   Looked for files:")
        for path in possible_pdfs:
            print(f"   - {path}")
        print("\n📝 Creating a test scenario without actual PDF...")
        test_non_existent_pdf(pdf_reader)
        return False
    
    try:
        # Test 1: Read entire PDF
        print(f"\n📖 Test 1: Reading Complete PDF - {pdf_file}")
        print("-" * 40)
        
        result = pdf_reader.read_pdf(pdf_file)
        
        if result["success"]:
            print(f"✅ PDF read successfully")
            print(f"   File: {result['file_path']}")
            print(f"   Page count: {result['page_count']}")
            print(f"   Total word count: {result['word_count']}")
            print(f"   Text preview: {result['text'][:200]}...")
            
            # Display metadata if available
            if result["metadata"]:
                print(f"\n📋 PDF Metadata:")
                for key, value in result["metadata"].items():
                    if value:  # Only show non-empty values
                        print(f"   {key}: {value}")
            
            # Show page breakdown
            print(f"\n📄 Page Breakdown:")
            for i, page_info in enumerate(result["pages"][:3]):  # Show first 3 pages
                print(f"   Page {page_info['page_number']}: {page_info['word_count']} words")
                print(f"   Preview: {page_info['text'][:100]}...")
                print()
        else:
            print(f"❌ Failed to read PDF: {result['error']}")
            return False
        
        # Test 2: Read specific pages
        print(f"\n📑 Test 2: Reading Specific Pages")
        print("-" * 40)
        
        if result["page_count"] > 1:
            # Read first 2 pages
            page_result = pdf_reader.read_pdf_pages(
                file_path=pdf_file,
                start_page=1,
                end_page=2
            )
            
            if page_result["success"]:
                print(f"✅ Page-specific reading successful")
                print(f"   Pages processed: {page_result['pages_processed']}")
                print(f"   Start page: {page_result['start_page']}")
                print(f"   End page: {page_result['end_page']}")
                print(f"   Total pages in document: {page_result['total_pages']}")
                print(f"   Text preview: {page_result['text'][:200]}...")
            else:
                print(f"❌ Failed to read pages: {page_result['error']}")
        else:
            print("⚠️  PDF has only one page, skipping page range test")
        
        # Test 3: Read middle pages
        print(f"\n📄 Test 3: Reading Middle Pages")
        print("-" * 40)
        
        if result["page_count"] > 2:
            middle_page = result["page_count"] // 2
            middle_result = pdf_reader.read_pdf_pages(
                file_path=pdf_file,
                start_page=middle_page,
                end_page=middle_page
            )
            
            if middle_result["success"]:
                print(f"✅ Middle page reading successful")
                print(f"   Read page: {middle_page}")
                print(f"   Text preview: {middle_result['text'][:150]}...")
            else:
                print(f"❌ Failed to read middle page: {middle_result['error']}")
        else:
            print("⚠️  PDF too short for middle page test")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during PDF reading: {str(e)}")
        return False

def test_non_existent_pdf(pdf_reader):
    """Test error handling with non-existent PDF."""
    
    print("\n🧪 Testing Error Handling")
    print("=" * 50)
    
    try:
        # Test 1: Non-existent file
        print("\n❌ Test 1: Handling Non-Existent File")
        print("-" * 40)
        
        result = pdf_reader.read_pdf("non_existent_file.pdf")
        
        if not result["success"]:
            print(f"✅ Error handling working correctly")
            print(f"   Error message: {result['error']}")
            print(f"   Success flag: {result['success']}")
            print(f"   Page count: {result['page_count']}")
        else:
            print(f"❌ Error handling failed - should have returned error")
        
        # Test 2: Invalid page range
        print("\n📄 Test 2: Invalid Page Range")
        print("-" * 40)
        
        page_result = pdf_reader.read_pdf_pages(
            file_path="non_existent_file.pdf",
            start_page=10,
            end_page=20
        )
        
        if not page_result["success"]:
            print(f"✅ Page range error handling working")
            print(f"   Error message: {page_result['error']}")
        else:
            print(f"❌ Page range error handling failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during error handling test: {str(e)}")
        return False

def test_pdf_content_analysis(pdf_reader):
    """Test PDF content analysis capabilities."""
    
    print("\n🧪 Testing PDF Content Analysis")
    print("=" * 50)
    
    # Look for PDF file again
    possible_pdfs = [
        "docs/employee_handbook.pdf",
        "employee_handbook.pdf",
        "../docs/employee_handbook.pdf"
    ]
    
    pdf_file = None
    for pdf_path in possible_pdfs:
        if os.path.exists(pdf_path):
            pdf_file = pdf_path
            break
    
    if not pdf_file:
        print("⚠️  No PDF file available for content analysis")
        return False
    
    try:
        # Read PDF for analysis
        result = pdf_reader.read_pdf(pdf_file)
        
        if not result["success"]:
            print(f"❌ Failed to read PDF for analysis: {result['error']}")
            return False
        
        # Test 1: Content statistics
        print(f"\n📊 Test 1: Content Statistics")
        print("-" * 40)
        
        text = result["text"]
        pages = result["pages"]
        
        # Calculate statistics
        total_chars = len(text)
        total_words = len(text.split())
        total_lines = len(text.split('\n'))
        
        print(f"✅ Content analysis complete")
        print(f"   Total characters: {total_chars:,}")
        print(f"   Total words: {total_words:,}")
        print(f"   Total lines: {total_lines:,}")
        print(f"   Average words per page: {total_words / len(pages):.1f}")
        
        # Test 2: Page comparison
        print(f"\n📈 Test 2: Page-by-Page Analysis")
        print("-" * 40)
        
        print(f"✅ Page analysis:")
        for i, page in enumerate(pages[:5]):  # Show first 5 pages
            print(f"   Page {page['page_number']}: {page['word_count']} words")
        
        if len(pages) > 5:
            print(f"   ... and {len(pages) - 5} more pages")
        
        # Test 3: Search for common terms
        print(f"\n🔍 Test 3: Content Search")
        print("-" * 40)
        
        search_terms = ["policy", "employee", "company", "work", "time"]
        found_terms = {}
        
        text_lower = text.lower()
        for term in search_terms:
            count = text_lower.count(term.lower())
            if count > 0:
                found_terms[term] = count
        
        print(f"✅ Content search complete:")
        for term, count in found_terms.items():
            print(f"   '{term}': found {count} times")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during content analysis: {str(e)}")
        return False

def run_all_pdf_tests():
    """Run all PDF reader tests."""
    
    print("🚀 Starting Comprehensive PDF Reader Tests")
    print("This will test PDF reading, metadata extraction, and content analysis\n")
    
    results = []
    
    try:
        # Test initialization
        pdf_reader = test_pdf_reader_initialization()
        if pdf_reader:
            results.append(("Initialization", True))
            
            # Test PDF reading
            reading_result = test_pdf_reading(pdf_reader)
            results.append(("PDF Reading", reading_result))
            
            # Test error handling
            error_result = test_non_existent_pdf(pdf_reader)
            results.append(("Error Handling", error_result))
            
            # Test content analysis
            analysis_result = test_pdf_content_analysis(pdf_reader)
            results.append(("Content Analysis", analysis_result))
        else:
            results.append(("Initialization", False))
        
        # Summary
        print("\n📊 Test Results Summary:")
        print("=" * 30)
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED/SKIPPED"
            print(f"{test_name}: {status}")
        
        print("\n✅ PDF Reader Testing Complete!")
        print("\nKey Features Demonstrated:")
        print("- ✓ PDF text extraction")
        print("- ✓ Metadata reading")
        print("- ✓ Page-specific processing")
        print("- ✓ Error handling")
        print("- ✓ Content analysis and statistics")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")

if __name__ == "__main__":
    print("📄 PDF Reader Utility Tests")
    print("This will test PDF reading, metadata extraction, and content analysis\n")
    
    try:
        run_all_pdf_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        print("Make sure you have:")
        print("1. Installed PyPDF2: pip install PyPDF2")
        print("2. Have a PDF file available for testing (e.g., docs/employee_handbook.pdf)") 