#!/usr/bin/env python3
"""
Simple startup script for FacePoke Gradio interface
"""

import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='FacePoke Gradio Interface')
    parser.add_argument('--cpu', action='store_true', help='Force CPU usage even if GPU is available')
    parser.add_argument('--port', type=int, default=7860, help='Port to run the Gradio interface on (default: 7860)')
    parser.add_argument('--share', action='store_true', help='Create a public link for the interface')
    
    args = parser.parse_args()
    
    # Set environment variables
    if args.cpu:
        os.environ['FACEPOKE_FORCE_CPU'] = '1'
        print("🔧 Forcing CPU usage as requested")
    
    # Import and run the Gradio app
    from gradio_app import create_interface
    
    print("🚀 Starting FacePoke Gradio interface...")
    print(f"📡 Interface will be available at: http://localhost:{args.port}")
    
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=args.port,
        share=args.share,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()
