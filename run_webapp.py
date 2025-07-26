#!/usr/bin/env python3
"""
Local runner for the PDF Intelligence Web App
Run this to test the web interface locally
"""

import os
import sys

# Add the source directories to Python path
sys.path.append('round1a/src')
sys.path.append('round1b/src')

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('results', exist_ok=True)

if __name__ == '__main__':
    try:
        from app import app
        print("🚀 Starting PDF Intelligence Web App...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have Flask installed: pip install flask PyMuPDF")
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
