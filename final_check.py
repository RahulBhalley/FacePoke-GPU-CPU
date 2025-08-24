#!/usr/bin/env python3
"""
Final comprehensive check for FacePoke Gradio interface
"""

import requests
import time
import sys

def check_server():
    """Check if the Gradio server is running"""
    try:
        response = requests.get("http://localhost:7860", timeout=5)
        if response.status_code == 200:
            print("✅ Gradio server is running at http://localhost:7860")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

def main():
    print("🎭 FacePoke - Final Status Check")
    print("=" * 40)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "check_dependencies.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All dependencies are installed")
        else:
            print("❌ Some dependencies are missing")
            print(result.stdout)
            return False
    except Exception as e:
        print(f"❌ Error checking dependencies: {e}")
        return False
    
    # Check server
    print("\n🌐 Checking server...")
    if not check_server():
        print("📝 Starting server...")
        print("   python run_gradio.py")
        return False
    
    print("\n🎉 Everything is working!")
    print("\n📝 How to use:")
    print("1. Open http://localhost:7860 in your browser")
    print("2. Wait for models to initialize (first time only)")
    print("3. Upload a portrait photo")
    print("4. Choose an emotion (Happy, Sad, Angry, Surprised, Thinking)")
    print("5. Click 'Apply Emotion'")
    print("6. Download your animated portrait!")
    
    print("\n🔧 Available commands:")
    print("   python run_gradio.py          # Start the interface")
    print("   python check_dependencies.py  # Check all dependencies")
    print("   python test_gradio.py         # Test the interface")
    print("   python check_status.py        # Check server status")
    
    print("\n🎭 Simple as fuck! Enjoy!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
