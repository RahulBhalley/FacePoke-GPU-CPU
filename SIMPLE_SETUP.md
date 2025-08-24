# 🎭 FacePoke - Simple Setup Guide

## What Changed?

✅ **Removed complex React frontend** - No more TypeScript, Bun, or complex build process  
✅ **Added simple Gradio interface** - Clean, modern UI with just Python  
✅ **Created isolated environment** - Virtual environment to keep dependencies clean  
✅ **Simplified deployment** - One command to run everything  

## Quick Start

### 1. Setup Environment
```bash
# Create and setup virtual environment
./setup_env.sh

# Activate environment
source activate_env.sh
```

### 2. Run the App
```bash
# Start the simple interface
python run_gradio.py

# Or use the demo script
python demo.py
```

### 3. Use the Interface
- Open http://localhost:7860 in your browser
- Upload a portrait photo
- Choose an emotion (Happy, Sad, Angry, Surprised, Thinking)
- Click "Apply Emotion"
- Download your animated portrait!

## Files Overview

### New Simple Files
- `gradio_app.py` - Main Gradio interface
- `run_gradio.py` - Startup script with CLI options
- `demo.py` - Simple demo script
- `requirements_gradio.txt` - Simplified dependencies
- `setup_env.sh` - Environment setup script
- `activate_env.sh` - Environment activation script
- `test_gradio.py` - Test script

### Removed Complex Files
- `client/` - React frontend (removed)
- `public/` - Built frontend files (removed)
- `app.py` - Complex aiohttp server (kept for reference)

## Environment Management

```bash
# Create environment
./setup_env.sh

# Activate environment
source activate_env.sh

# Deactivate environment
deactivate

# Test installation
python test_gradio.py
```

## Simple as Fuck! 🎭

- **No build process** - Just run Python
- **No complex dependencies** - Just pip install
- **No TypeScript/React** - Just simple Python
- **No WebSocket complexity** - Just HTTP requests
- **Clean, modern UI** - Gradio handles everything

## Troubleshooting

### Environment Issues
```bash
# Recreate environment
rm -rf facepoke_env
./setup_env.sh
```

### Missing Dependencies
If you see any "No module named" errors:
```bash
# Run comprehensive dependency check
python check_dependencies.py

# Install all missing dependencies
pip install -r requirements_gradio.txt

# Or install specific missing dependencies
pip install onnx onnxruntime diffusers accelerate transformers huggingface-hub safetensors einops
```

### Port Issues
```bash
# Use different port
python run_gradio.py --port 8080
```

### CPU Only
```bash
# Force CPU usage
python run_gradio.py --cpu
```

### Models Not Initializing
If you see "Models not initialized" message:
- Wait a few minutes for models to download (first run only)
- Check terminal for download progress
- Models are cached after first download

## That's It! 🎉

Simple, clean, and easy to use. No more complex frontend setup!
