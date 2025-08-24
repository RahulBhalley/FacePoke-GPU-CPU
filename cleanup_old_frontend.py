#!/usr/bin/env python3
"""
Cleanup script to remove the old React frontend files
"""

import os
import shutil

def cleanup_old_frontend():
    """Remove old React frontend files"""
    
    # Files and directories to remove
    items_to_remove = [
        'client/',
        'public/',
        'app.py',  # Old aiohttp server
    ]
    
    print("🧹 Cleaning up old React frontend...")
    
    for item in items_to_remove:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"✅ Removed directory: {item}")
            else:
                os.remove(item)
                print(f"✅ Removed file: {item}")
        else:
            print(f"⚠️  Item not found: {item}")
    
    print("\n🎉 Cleanup complete!")
    print("📝 The project now uses the simple Gradio interface:")
    print("   - gradio_app.py - Main Gradio interface")
    print("   - run_gradio.py - Startup script")
    print("\n🚀 To run the app:")
    print("   python run_gradio.py")

if __name__ == "__main__":
    cleanup_old_frontend()
