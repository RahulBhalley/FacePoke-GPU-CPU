"""
FacePoke API

Author: Julian Bilcke
Date: September 30, 2024
"""

import sys
import asyncio
import torch
from aiohttp import web, WSMsgType
import json
from json import JSONEncoder
import numpy as np
import uuid
import logging
import os
import signal
from typing import Dict, Any, List, Optional
import base64
import io

from PIL import Image

# by popular demand, let's add support for avif
import pillow_avif

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set asyncio logger to DEBUG level
#logging.getLogger("asyncio").setLevel(logging.INFO)

#logger.debug(f"Python version: {sys.version}")

# SIGSEGV handler
def SIGSEGV_signal_arises(signalNum, stack):
    logger.critical(f"{signalNum} : SIGSEGV arises")
    logger.critical(f"Stack trace: {stack}")

signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

from loader import initialize_models
from engine import Engine, base64_data_uri_to_PIL_Image

# Global constants
DATA_ROOT = os.environ.get('DATA_ROOT', '/tmp/data')
MODELS_DIR = os.path.join(DATA_ROOT, "models")

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, Image.Image):
            return {
                'width': obj.width,
                'height': obj.height,
                'format': obj.format
            }
        elif isinstance(obj, (bytes, bytearray)):
            return None  # Skip binary data
        elif hasattr(obj, 'tolist'):  # Handle other array-like objects
            return obj.tolist()
        elif hasattr(obj, '__dict__'):  # Handle general objects
            return {k: v for k, v in obj.__dict__.items() 
                    if not k.startswith('_') and 
                    not callable(v) and 
                    not isinstance(v, (bytes, bytearray))}
        else:
            return super(NumpyEncoder, self).default(obj)

async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    engine = request.app['engine']
    try:
        #logger.info("New WebSocket connection established")
        while True:
            msg = await ws.receive()

            if msg.type in (WSMsgType.CLOSE, WSMsgType.ERROR):
                #logger.warning(f"WebSocket connection closed: {msg.type}")
                break

            try:
                if msg.type == WSMsgType.BINARY:
                    res = await engine.load_image(msg.data)
                    json_res = json.dumps(res, cls=NumpyEncoder)
                    await ws.send_str(json_res)

                elif msg.type == WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    logger.info(f"Received WebSocket text message: {data}")
                    
                    # Check if we have a valid UUID
                    uuid = data.get('uuid')  # Frontend uses 'uuid'
                    if not uuid:
                        logger.error("No UUID provided in WebSocket message")
                        continue
                        
                    # Check if we have valid params
                    params = data.get('params')
                    if not params:
                        logger.error("No params provided in WebSocket message")
                        continue
                        
                    logger.info(f"Transforming image {uuid} with params: {params}")
                    webp_bytes = await engine.transform_image(uuid, params)
                    await ws.send_bytes(webp_bytes)

            except Exception as e:
                logger.error(f"Error in engine: {str(e)}")
                logger.exception("Full traceback:")
                await ws.send_json({"error": str(e)})

    except Exception as e:
        logger.error(f"Error in websocket_handler: {str(e)}")
        logger.exception("Full traceback:")
    return ws

async def index(request: web.Request) -> web.Response:
    """Serve the index.html file"""
    content = open(os.path.join(os.path.dirname(__file__), "public", "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)

async def js_index(request: web.Request) -> web.Response:
    """Serve the index.js file"""
    content = open(os.path.join(os.path.dirname(__file__), "public", "index.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)

async def hf_logo(request: web.Request) -> web.Response:
    """Serve the hf-logo.svg file"""
    content = open(os.path.join(os.path.dirname(__file__), "public", "hf-logo.svg"), "r").read()
    return web.Response(content_type="image/svg+xml", text=content)

async def initialize_app() -> web.Application:
    """Initialize and configure the web application."""
    try:
        logger.info("Initializing application...")
        logger.info("Starting model initialization...")
        try:
            # Memory cleanup before model loading
            import gc
            gc.collect()
            torch.cuda.empty_cache()
            
            # No timeout - let it take as long as needed
            live_portrait = await initialize_models()
            logger.info("✅ Model initialization completed successfully")
            
            # Clear any unused memory
            gc.collect()
            torch.cuda.empty_cache()
        except asyncio.TimeoutError:
            logger.error("Model initialization timed out after 60 seconds")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize models: {str(e)}")
            raise

        logger.info("🚀 Creating Engine instance...")
        try:
            logger.info("  ⏳ Initializing Engine with LivePortrait...")
            engine = Engine(live_portrait=live_portrait)
            logger.info("✅ Engine instance created successfully")
            logger.info("  ⏳ Setting up application routes...")
            
            # Configure routes
            app = web.Application()
            app['engine'] = engine
            
            app.router.add_get("/", index)
            app.router.add_get("/index.js", js_index)
            app.router.add_get("/hf-logo.svg", hf_logo)
            app.router.add_get("/ws", websocket_handler)
            app.router.add_post("/api/apply-emotion", apply_emotion)
            
            logger.info("✅ Application routes configured")
            return app
        except Exception as e:
            logger.error(f"Failed to create engine: {str(e)}")
            raise


    except Exception as e:
        logger.error(f"🚨 Error during application initialization: {str(e)}")
        logger.exception("Full traceback:")
        raise

# Emotion presets mapping
EMOTION_PARAMS = {
    'angry': {
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
    'sad': {
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
    'surprised': {
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
    'thinking': {
        'rotate_pitch': -18.60,
        'rotate_yaw': -25.15,
        'rotate_roll': 0,
        'eyebrow': 13.03,
        'eyes': -5,
        'eee': -5.89,
        'aaa': -1.52,
        'pupil_x': 8,
        'pupil_y': 0
    },
    'happy': {
        'rotate_pitch': -3,
        'rotate_yaw': -5,
        'rotate_roll': 0,
        'eyebrow': 13,
        'eyes': 2.5,
        'eee': 12,
        'aaa': 13,
        'pupil_x': 0,
        'pupil_y': 0
    }
}

async def apply_emotion(request: web.Request) -> web.Response:
    """Apply an emotion preset to an image"""
    try:
        logger.info("Starting emotion application process...")
        # Parse multipart form data
        reader = await request.multipart()
        
        # Get the image file
        field = await reader.next()
        if field.name == 'image':
            logger.info("Reading image data...")
            image_data = await field.read()
            image = Image.open(io.BytesIO(image_data))
            logger.info(f"Image loaded successfully, format: {image.format}, size: {image.size}")
        else:
            logger.error("No image field found in request")
            return web.Response(status=400, text='Image file is required')
            
        # Get the emotion name
        field = await reader.next()
        if field.name == 'emotion':
            logger.info("Reading emotion parameter...")
            emotion = (await field.read()).decode().lower()
            logger.info(f"Requested emotion: {emotion}")
            if emotion not in EMOTION_PARAMS:
                logger.error(f"Invalid emotion: {emotion}. Valid emotions: {list(EMOTION_PARAMS.keys())}")
                return web.Response(status=400, text=f'Invalid emotion. Must be one of: {list(EMOTION_PARAMS.keys())}')
            logger.info(f"Using emotion parameters: {EMOTION_PARAMS[emotion]}")
        else:
            logger.error("No emotion field found in request")
            return web.Response(status=400, text='Emotion name is required')
            
        # Load image into engine
        logger.info("Loading image into engine...")
        engine = request.app['engine']
        res = await engine.load_image_api(image_data)
        logger.info(f"Image loaded into engine with uuid: {res['uuid']}")
        logger.info(f"Cache status after load: {list(engine.processed_cache.keys())}")
        
        # Apply emotion transformation
        logger.info("Applying emotion transformation...")
        webp_bytes = await engine.transform_image(res['uuid'], EMOTION_PARAMS[emotion])
        logger.info("Emotion transformation complete")
        
        # Return the modified image
        logger.info("Returning modified image...")
        return web.Response(
            body=webp_bytes,
            content_type='image/webp'
        )
        
    except Exception as e:
        logger.error(f"Error in apply_emotion: {str(e)}")
        logger.exception("Full traceback:")
        return web.Response(status=500, text=str(e))

if __name__ == "__main__":
    try:
        import argparse
        parser = argparse.ArgumentParser(description='FacePoke Application')
        parser.add_argument('--cpu', action='store_true', help='Force CPU usage even if GPU is available')
        args = parser.parse_args()

        logger.info("Starting FacePoke application")
        logger.info("Initializing application components...")
        
        # Pass CPU flag to InferenceConfig through environment variable
        if args.cpu:
            os.environ['FACEPOKE_FORCE_CPU'] = '1'
            logger.info("🔧 Forcing CPU usage as requested")
        
        app = asyncio.run(initialize_app())
        logger.info("✅ Application initialization complete")
        logger.info("🚀 Starting web server on port 8080...")
        web.run_app(app, host="0.0.0.0", port=8080, access_log_format='%{REMOTE_ADDR}s - "%r" %s %b "%{Referer}i" "%{User-Agent}i"')
    except Exception as e:
        logger.critical(f"🚨 FATAL: Failed to start the app: {str(e)}")
        logger.exception("Full traceback:")
