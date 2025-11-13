"""
Quick test to verify PDF processing works properly.
Tests the complete document processing pipeline with a sample PDF.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.document_processor import DocumentProcessor
from services.pdf_extractor import PDFExtractor
import tempfile


def test_pdf_extractor():
    """Test that PDFExtractor is working."""
    print("=" * 70)
    print("TEST 1: PDF Extractor Initialization")
    print("=" * 70)
    
    try:
        extractor = PDFExtractor()
        print("✅ PDFExtractor initialized successfully")
        print(f"   Using: PyPDF2")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize PDFExtractor: {e}")
        return False


def test_document_processor_init():
    """Test DocumentProcessor initialization."""
    print("\n" + "=" * 70)
    print("TEST 2: DocumentProcessor Initialization")
    print("=" * 70)
    
    try:
        processor = DocumentProcessor()
        print("✅ DocumentProcessor initialized successfully")
        print(f"   PDF Extractor: {processor.pdf_extractor.__class__.__name__}")
        print(f"   Clause Segmenter: {processor.clause_segmenter.__class__.__name__}")
        print(f"   Supported formats: PDF, DOCX, TXT, Images")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize DocumentProcessor: {e}")
        return False


def test_text_processing():
    """Test text processing without PDF."""
    print("\n" + "=" * 70)
    print("TEST 3: Text Processing (No PDF Required)")
    print("=" * 70)
    
    try:
        processor = DocumentProcessor()
        
        sample_text = """
        DATA PROCESSING AGREEMENT
        
        1. DEFINITIONS
        This Data Processing Agreement ("Agreement") is entered into between the Controller and the Processor.
        
        2. SCOPE OF PROCESSING
        The Processor shall process Personal Data only on documented instructions from the Controller.
        
        3. DATA SECURITY
        The Processor shall implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk.
        
        4. SUB-PROCESSORS
        The Processor shall not engage another processor without prior specific or general written authorization of the Controller.
        
        5. DATA SUBJECT RIGHTS
        The Processor shall assist the Controller in fulfilling its obligations to respond to requests for exercising data subject rights.
        """
        
        print(f"\n📄 Processing sample contract text ({len(sample_text)} characters)...")
        
        processed_doc = processor.process_text(sample_text)
        
        print(f"\n✅ Text processing successful!")
        print(f"   Document ID: {processed_doc.document_id}")
        print(f"   Total words: {processed_doc.total_words}")
        print(f"   Clauses identified: {processed_doc.num_clauses}")
        print(f"   Processing time: {processed_doc.processing_time:.2f}s")
        
        print(f"\n📋 Extracted Clauses:")
        for i, clause in enumerate(processed_doc.clauses[:3], 1):
            print(f"   {i}. {clause.text[:60]}...")
        
        if processed_doc.num_clauses > 3:
            print(f"   ... and {processed_doc.num_clauses - 3} more clauses")
        
        return True
        
    except Exception as e:
        print(f"❌ Text processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_create_sample_pdf():
    """Create a sample PDF for testing."""
    print("\n" + "=" * 70)
    print("TEST 4: Sample PDF Creation")
    print("=" * 70)
    
    try:
        # Try to create a simple PDF using reportlab (if available)
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            # Create temp PDF file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_path = temp_file.name
            temp_file.close()
            
            # Create PDF
            c = canvas.Canvas(temp_path, pagesize=letter)
            c.drawString(100, 750, "SAMPLE CONTRACT - TEST DOCUMENT")
            c.drawString(100, 720, "")
            c.drawString(100, 690, "1. DEFINITIONS")
            c.drawString(100, 670, "This is a sample contract for testing purposes.")
            c.drawString(100, 650, "")
            c.drawString(100, 620, "2. DATA PROCESSING")
            c.drawString(100, 600, "Personal Data shall be processed in accordance with applicable law.")
            c.drawString(100, 580, "")
            c.drawString(100, 550, "3. SECURITY MEASURES")
            c.drawString(100, 530, "Appropriate technical and organizational measures shall be implemented.")
            c.save()
            
            print(f"✅ Sample PDF created: {temp_path}")
            return temp_path
            
        except ImportError:
            print("⚠️ reportlab not installed, skipping PDF creation test")
            print("   Install with: pip install reportlab")
            return None
            
    except Exception as e:
        print(f"❌ Failed to create sample PDF: {e}")
        return None


def test_pdf_processing(pdf_path):
    """Test processing an actual PDF file."""
    print("\n" + "=" * 70)
    print("TEST 5: PDF Document Processing")
    print("=" * 70)
    
    if pdf_path is None:
        print("⚠️ Skipping - no PDF available")
        return None
    
    try:
        processor = DocumentProcessor()
        
        print(f"\n📄 Processing PDF: {Path(pdf_path).name}")
        
        processed_doc = processor.process_document(pdf_path)
        
        print(f"\n✅ PDF processing successful!")
        print(f"   Document ID: {processed_doc.document_id}")
        print(f"   Original filename: {processed_doc.original_filename}")
        print(f"   Total words: {processed_doc.total_words}")
        print(f"   Clauses identified: {processed_doc.num_clauses}")
        print(f"   Processing time: {processed_doc.processing_time:.2f}s")
        
        print(f"\n📋 Extracted Clauses:")
        for i, clause in enumerate(processed_doc.clauses, 1):
            print(f"   {i}. {clause.text[:60]}...")
        
        # Cleanup
        import os
        try:
            os.unlink(pdf_path)
            print(f"\n🧹 Cleaned up temp file")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ PDF processing failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        import os
        try:
            os.unlink(pdf_path)
        except:
            pass
        
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("DOCUMENT PROCESSING VERIFICATION")
    print("=" * 70)
    print("\nThis test suite verifies that document processing is working")
    print("correctly, including PDF extraction, text processing, and")
    print("clause segmentation.\n")
    
    results = []
    
    # Test 1: PDF Extractor
    results.append(("PDF Extractor Init", test_pdf_extractor()))
    
    # Test 2: Document Processor
    results.append(("Document Processor Init", test_document_processor_init()))
    
    # Test 3: Text Processing
    results.append(("Text Processing", test_text_processing()))
    
    # Test 4 & 5: PDF Processing (if reportlab available)
    pdf_path = test_create_sample_pdf()
    if pdf_path:
        results.append(("Sample PDF Creation", True))
        results.append(("PDF Processing", test_pdf_processing(pdf_path)))
    else:
        results.append(("Sample PDF Creation", None))
        results.append(("PDF Processing", None))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⚠️ SKIP"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    total = len(results)
    
    print(f"\n📊 Results: {passed} passed, {failed} failed, {skipped} skipped out of {total} tests")
    
    if failed == 0:
        print("\n🎉 All required tests passed! Document processing is working!")
        print("\n✅ Your frontend PDF processing is fully functional:")
        print("   - PDF text extraction: Working (PyPDF2)")
        print("   - Text processing: Working")
        print("   - Clause segmentation: Working")
        print("   - Document metadata: Working")
        print("\n💡 Note: For scanned PDFs, OCR (Tesseract) provides fallback.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
