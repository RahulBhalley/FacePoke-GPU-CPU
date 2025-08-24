#!/usr/bin/env python3
"""
Simple status check for FacePoke Gradio interface
"""

import requests
import time
import sys

def check_gradio_status():
    """Check if the Gradio interface is running and responding"""
    
    try:
        # Check if the server is running
        response = requests.get("http://localhost:7860", timeout=5)
        if response.status_code == 200:
            print("✅ Gradio interface is running at http://localhost:7860")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Gradio interface")
        print("📝 Make sure the server is running with: python run_gradio.py")
        return False
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return False

def main():
    print("🎭 FacePoke Status Check")
    print("=" * 30)
    
    # Check if server is running
    if not check_gradio_status():
        sys.exit(1)
    
    print("\n📝 Instructions:")
    print("1. Open http://localhost:7860 in your browser")
    print("2. Wait for models to initialize (may take a few minutes)")
    print("3. Upload a portrait photo")
    print("4. Choose an emotion and click 'Apply Emotion'")
    print("5. Download your animated portrait!")
    
    print("\n🔧 If you see 'Models not initialized' message:")
    print("   - Wait a few minutes for the models to load")
    print("   - The models are downloaded automatically on first run")
    print("   - Check the terminal for download progress")
    
    print("\n🎉 Enjoy your simple FacePoke experience!")

if __name__ == "__main__":
    main()
