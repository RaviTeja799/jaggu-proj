"""
Quick test to verify all imports work correctly.
"""
import sys
from pathlib import Path

# Add the project directory to the path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

print("Testing imports...")
print("=" * 60)

try:
    print("1. Testing config import...")
    from config import config
    print(f"   ✓ Config loaded: {config.app_name}")
    
    print("\n2. Testing utils import...")
    from utils import get_logger
    logger = get_logger("test")
    print("   ✓ Logger initialized")
    
    print("\n3. Testing models import...")
    from models.clause import Clause
    from models.processed_document import ProcessedDocument
    print("   ✓ Models imported")
    
    print("\n4. Testing services import...")
    from services.document_processor import DocumentProcessor
    print("   ✓ DocumentProcessor imported")
    
    from services.nlp_analyzer import NLPAnalyzer
    print("   ✓ NLPAnalyzer imported")
    
    from services.compliance_checker import ComplianceChecker
    print("   ✓ ComplianceChecker imported")
    
    from services.recommendation_engine import RecommendationEngine
    print("   ✓ RecommendationEngine imported")
    
    from services.export_service import ExportService
    print("   ✓ ExportService imported")
    
    print("\n5. Testing data imports...")
    from data import gdpr_requirements, hipaa_requirements, ccpa_requirements, sox_requirements
    print("   ✓ Regulatory requirements imported")
    
    print("\n" + "=" * 60)
    print("✅ ALL IMPORTS SUCCESSFUL!")
    print("=" * 60)
    print("\nYour project is ready to use!")
    print("\nTo start the application, run:")
    print("   streamlit run app.py")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
