#!/usr/bin/env python3
"""
Test script to verify the web app works
"""

import sys
import os

# Add source directories
sys.path.append('round1a/src')
sys.path.append('round1b/src')

def test_imports():
    """Test that all imports work"""
    try:
        from simple_extractor import extract_pdf_outline
        from simple_persona import process_documents
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_flask_app():
    """Test that Flask app can be imported"""
    try:
        from app import app
        print("✅ Flask app imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Flask app import error: {e}")
        print("💡 Install Flask: pip install flask PyMuPDF")
        return False

def main():
    print("🧪 Testing PDF Intelligence Web App...")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        return False
    
    # Test Flask app
    if not test_flask_app():
        return False
    
    print("\n🎉 All tests passed!")
    print("\n🚀 To run the web app:")
    print("   python run_webapp.py")
    print("\n🌐 Then open: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
