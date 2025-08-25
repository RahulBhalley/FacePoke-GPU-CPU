"""
Simple Gradio Interface for FacePoke

A clean, simple interface for the FacePoke portrait animation system.
"""

import os
# Enable MPS fallback to CPU for unsupported operations
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

import gradio as gr
import asyncio
import logging
from PIL import Image
import io
import sys
import argparse

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from loader import initialize_models
from engine import Engine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global variables
live_portrait = None
engine = None

# Emotion presets
EMOTION_PARAMS = {
    'Happy': {
        'rotate_pitch': -3,
        'rotate_yaw': -5,
        'rotate_roll': 0,
        'eyebrow': 13,
        'eyes': 2.5,
        'eee': 12,
        'aaa': 13,
        'pupil_x': 0,
        'pupil_y': 0
    },
    'Sad': {
        'rotate_pitch': 15,
        'rotate_yaw': 0,
        'rotate_roll': 0,
        'eyebrow': 5,
        'eyes': -5,
        'eee': -5,
        'aaa': -10,
        'pupil_x': 0,
        'pupil_y': 0
    },
    'Angry': {
        'rotate_pitch': 10,
        'rotate_yaw': 0,
        'rotate_roll': 0,
        'eyebrow': -8,
        'eyes': -10,
        'eee': -10,
        'aaa': -20,
        'pupil_x': 5.5,
        'pupil_y': 0
    },
    'Surprised': {
        'rotate_pitch': -10,
        'rotate_yaw': 0,
        'rotate_roll': 0,
        'eyebrow': 12,
        'eyes': 15,
        'eee': 0,
        'aaa': 80,
        'pupil_x': 0,
        'pupil_y': 5
    },
    'Thinking': {
        'rotate_pitch': -18.60,
        'rotate_yaw': -25.15,
        'rotate_roll': 0,
        'eyebrow': 13.03,
        'eyes': -5,
        'eee': -5.89,
        'aaa': -1.52,
        'pupil_x': 8,
        'pupil_y': 0
    }
}

async def initialize_models_async():
    """Initialize models asynchronously"""
    global live_portrait, engine
    try:
        logger.info("Initializing models...")
        live_portrait = await initialize_models()
        engine = Engine(live_portrait=live_portrait)
        
        # Get device information
        device_info = str(engine.device)
        logger.info(f"✅ Models initialized successfully on {device_info}")
        
        return f"✅ Models initialized successfully on {device_info}"
    except Exception as e:
        logger.error(f"❌ Failed to initialize models: {str(e)}")
        raise

def apply_emotion(image, emotion_name):
    """Apply preset emotion to the uploaded image"""
    global engine
    
    if engine is None:
        return None, "❌ Models not initialized. Please wait for initialization to complete."
    
    if image is None:
        return None, "❌ Please upload an image first."
    
    if emotion_name not in EMOTION_PARAMS:
        return None, f"❌ Invalid emotion: {emotion_name}"
    
    try:
        # Convert PIL image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Load image into engine
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            res = loop.run_until_complete(engine.load_image_api(img_byte_arr))
            
            # Apply emotion transformation
            webp_bytes = loop.run_until_complete(
                engine.transform_image(res['uuid'], EMOTION_PARAMS[emotion_name])
            )
            
            # Convert webp bytes back to PIL image
            result_image = Image.open(io.BytesIO(webp_bytes))
            
            return result_image, f"✅ Applied {emotion_name} emotion successfully!"
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error applying emotion: {str(e)}")
        return None, f"❌ Error: {str(e)}"

def apply_custom_edits(image, rotate_pitch, rotate_yaw, rotate_roll, eyebrow, eyes, eee, aaa, pupil_x, pupil_y):
    """Apply custom edits using slider values"""
    global engine
    
    if engine is None:
        return None, "❌ Models not initialized. Please wait for initialization to complete."
    
    if image is None:
        return None, "❌ Please upload an image first."
    
    # Create custom emotion parameters from sliders
    custom_params = {
        'rotate_pitch': rotate_pitch,
        'rotate_yaw': rotate_yaw,
        'rotate_roll': rotate_roll,
        'eyebrow': eyebrow,
        'eyes': eyes,
        'eee': eee,
        'aaa': aaa,
        'pupil_x': pupil_x,
        'pupil_y': pupil_y
    }
    
    try:
        # Convert PIL image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Load image into engine
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            res = loop.run_until_complete(engine.load_image_api(img_byte_arr))
            
            # Apply emotion transformation
            webp_bytes = loop.run_until_complete(
                engine.transform_image(res['uuid'], custom_params)
            )
            
            # Convert webp bytes back to PIL image
            result_image = Image.open(io.BytesIO(webp_bytes))
            
            return result_image, f"✅ Applied custom edits successfully!"
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error applying custom edits: {str(e)}")
        return None, f"❌ Error: {str(e)}"

def update_sliders_from_emotion(emotion_name):
    """Update slider values when emotion is selected"""
    if emotion_name in EMOTION_PARAMS:
        params = EMOTION_PARAMS[emotion_name]
        return (
            params['rotate_pitch'],
            params['rotate_yaw'],
            params['rotate_roll'],
            params['eyebrow'],
            params['eyes'],
            params['eee'],
            params['aaa'],
            params['pupil_x'],
            params['pupil_y']
        )
    return (0, 0, 0, 0, 0, 0, 0, 0, 0)

def create_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(
        title="FacePoke - Simple Portrait Animation",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🎭 FacePoke - Simple Portrait Animation
        
        Upload a portrait photo and apply different emotions to animate it!
        """)
        
        # Device info display
        device_info = gr.Textbox(
            label="Device Information",
            value="Initializing...",
            interactive=False
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                gr.Markdown("### 📸 Upload Image")
                input_image = gr.Image(
                    label="Upload Portrait",
                    type="pil",
                    height=300
                )
                
                # Emotion section
                gr.Markdown("### 🎭 Preset Emotions")
                emotion_dropdown = gr.Dropdown(
                    choices=list(EMOTION_PARAMS.keys()),
                    value="Happy",
                    label="Choose Emotion",
                    info="Select the emotion to apply to your portrait"
                )
                
                apply_emotion_btn = gr.Button(
                    "🎭 Apply Emotion",
                    variant="primary",
                    size="lg"
                )
                
                status_text = gr.Textbox(
                    label="Status",
                    interactive=False,
                    value="Ready to process images!"
                )
            
            with gr.Column(scale=1):
                # Output section
                gr.Markdown("### 🎨 Result")
                output_image = gr.Image(
                    label="Animated Portrait",
                    height=300
                )
        
        # Custom edits section
        with gr.Row():
            with gr.Column(scale=1):
                # Left side - Preset emotions (already defined above)
                pass
            
            with gr.Column(scale=1):
                # Right side - Custom sliders
                gr.Markdown("### 🎛️ Custom Face Edits")
                
                rotate_pitch = gr.Slider(
                    minimum=-30, maximum=30, value=0, step=0.1,
                    label="Rotate Pitch",
                    info="Head tilt forward/backward"
                )
                
                rotate_yaw = gr.Slider(
                    minimum=-30, maximum=30, value=0, step=0.1,
                    label="Rotate Yaw",
                    info="Head turn left/right"
                )
                
                rotate_roll = gr.Slider(
                    minimum=-30, maximum=30, value=0, step=0.1,
                    label="Rotate Roll",
                    info="Head tilt left/right"
                )
                
                eyebrow = gr.Slider(
                    minimum=-20, maximum=20, value=0, step=0.1,
                    label="Eyebrow",
                    info="Eyebrow movement"
                )
                
                eyes = gr.Slider(
                    minimum=-20, maximum=20, value=0, step=0.1,
                    label="Eyes",
                    info="Eye opening/closing"
                )
                
                eee = gr.Slider(
                    minimum=-20, maximum=20, value=0, step=0.1,
                    label="EEE",
                    info="Mouth shape for 'eee' sound"
                )
                
                aaa = gr.Slider(
                    minimum=-30, maximum=100, value=0, step=0.1,
                    label="AAA",
                    info="Mouth shape for 'aaa' sound"
                )
                
                pupil_x = gr.Slider(
                    minimum=-10, maximum=10, value=0, step=0.1,
                    label="Pupil X",
                    info="Pupil horizontal movement"
                )
                
                pupil_y = gr.Slider(
                    minimum=-10, maximum=10, value=0, step=0.1,
                    label="Pupil Y",
                    info="Pupil vertical movement"
                )
                
                apply_edits_btn = gr.Button(
                    "✏️ Apply Edits",
                    variant="secondary",
                    size="lg"
                )
        
        # Examples
        gr.Markdown("### 💡 Tips")
        gr.Markdown("""
        - Use clear, front-facing portrait photos for best results
        - Make sure the face is well-lit and clearly visible
        - The system works best with high-quality images
        - Supported formats: JPG, PNG, WEBP
        - Use preset emotions for quick results, or fine-tune with custom sliders
        """)
        
        # Event handlers
        apply_emotion_btn.click(
            fn=apply_emotion,
            inputs=[input_image, emotion_dropdown],
            outputs=[output_image, status_text]
        )
        
        apply_edits_btn.click(
            fn=apply_custom_edits,
            inputs=[input_image, rotate_pitch, rotate_yaw, rotate_roll, eyebrow, eyes, eee, aaa, pupil_x, pupil_y],
            outputs=[output_image, status_text]
        )
        
        # Update sliders when emotion is selected
        emotion_dropdown.change(
            fn=update_sliders_from_emotion,
            inputs=[emotion_dropdown],
            outputs=[rotate_pitch, rotate_yaw, rotate_roll, eyebrow, eyes, eee, aaa, pupil_x, pupil_y]
        )
        
        # Initialize models on startup
        interface.load(initialize_models_async, outputs=device_info)
    
    return interface

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="FacePoke - Simple Portrait Animation with Gradio Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python gradio_app.py                           # Run with default settings
  python gradio_app.py --port 8080               # Run on port 8080
  python gradio_app.py --host 127.0.0.1          # Run on localhost only
  python gradio_app.py --share                   # Enable public sharing
  python gradio_app.py --force-cpu               # Force CPU usage
  python gradio_app.py --quiet                   # Run in quiet mode
        """
    )
    
    # Server settings
    parser.add_argument(
        '--host', 
        type=str, 
        default="0.0.0.0",
        help="Server host address (default: 0.0.0.0)"
    )
    parser.add_argument(
        '--port', 
        type=int, 
        default=7860,
        help="Server port (default: 7860)"
    )
    parser.add_argument(
        '--share', 
        action='store_true',
        help="Enable public sharing (creates a public URL)"
    )
    
    # Device settings
    parser.add_argument(
        '--force-cpu', 
        action='store_true',
        help="Force CPU usage even if GPU is available"
    )
    
    # Logging settings
    parser.add_argument(
        '--quiet', 
        action='store_true',
        help="Run in quiet mode (suppress most output)"
    )
    parser.add_argument(
        '--debug', 
        action='store_true',
        help="Enable debug logging"
    )
    
    # Interface settings
    parser.add_argument(
        '--show-error', 
        action='store_true',
        default=True,
        help="Show error details in interface (default: True)"
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # Configure logging based on arguments
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    # Initialize models
    logger.info("Starting FacePoke Gradio app...")
    
    # Check for CPU flag
    force_cpu = args.force_cpu or os.environ.get('FACEPOKE_FORCE_CPU', '0') == '1'
    if force_cpu:
        logger.info("🔧 Forcing CPU usage as requested")
        os.environ['FACEPOKE_FORCE_CPU'] = '1'
    
    # Log startup configuration
    logger.info(f"Server configuration: {args.host}:{args.port}")
    logger.info(f"Public sharing: {'Enabled' if args.share else 'Disabled'}")
    logger.info(f"Force CPU: {'Yes' if force_cpu else 'No'}")
    logger.info(f"Debug mode: {'Enabled' if args.debug else 'Disabled'}")
    
    # Create and launch interface
    interface = create_interface()
    interface.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        show_error=args.show_error,
        quiet=args.quiet
    )
