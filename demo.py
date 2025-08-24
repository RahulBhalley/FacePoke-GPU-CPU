#!/usr/bin/env python3
"""
Simple demo script for FacePoke Gradio interface
"""

import os
import sys
import time

def main():
    print("🎭 FacePoke - Simple Portrait Animation Demo")
    print("=" * 50)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected!")
        print("📝 For best results, activate the virtual environment:")
        print("   source activate_env.sh")
        print()
    
    # Check if required files exist
    required_files = ['gradio_app.py', 'run_gradio.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files found!")
    print()
    
    print("🚀 Starting FacePoke Gradio interface...")
    print("📡 Interface will be available at: http://localhost:7860")
    print("⏱️  Initialization may take a few minutes...")
    print()
    print("💡 Tips:")
    print("   - Upload a clear, front-facing portrait photo")
    print("   - Choose from 5 different emotions")
    print("   - Download your animated portrait")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    try:
        # Import and run the Gradio app
        from gradio_app import create_interface
        
        interface = create_interface()
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            quiet=False
        )
        
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Error starting demo: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
