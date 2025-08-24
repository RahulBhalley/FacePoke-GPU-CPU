#!/usr/bin/env python3
"""
Simple test script for the Gradio interface
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    try:
        print("🧪 Testing imports...")
        
        import gradio as gr
        print("✅ Gradio imported successfully")
        
        from PIL import Image
        print("✅ PIL imported successfully")
        
        import torch
        print("✅ PyTorch imported successfully")
        
        # Test our custom modules
        from gradio_app import EMOTION_PARAMS, create_interface
        print("✅ Custom modules imported successfully")
        
        print(f"✅ Found {len(EMOTION_PARAMS)} emotion presets")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_interface_creation():
    """Test that the Gradio interface can be created"""
    try:
        print("\n🧪 Testing interface creation...")
        
        from gradio_app import create_interface
        
        interface = create_interface()
        print("✅ Gradio interface created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Interface creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing FacePoke Gradio Interface\n")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return False
    
    # Test interface creation
    if not test_interface_creation():
        print("\n❌ Interface creation failed!")
        return False
    
    print("\n🎉 All tests passed!")
    print("\n📝 To run the interface:")
    print("   python run_gradio.py")
    print("\n📝 To run with CPU only:")
    print("   python run_gradio.py --cpu")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
