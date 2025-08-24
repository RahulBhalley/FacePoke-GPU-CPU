---
title: FacePoke
emoji: 🙂‍↔️👈
colorFrom: yellow
colorTo: red
sdk: docker
pinned: true
license: mit
header: mini
app_file: gradio_app.py
app_port: 7860
disable_embedding: true
short_description: Simple portrait animation with emotions!
---

# FacePoke - Simple Portrait Animation

## Table of Contents

- [Introduction](#introduction)
- [Acknowledgements](#acknowledgements)
- [Installation](#installation)
  - [Local Setup](#local-setup)
  - [Docker Deployment](#docker-deployment)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Introduction

A **simple and clean** portrait animation app that lets you apply different emotions to your photos.

**Simple as fuck!** 🎭

**Repository**: [GitHub - jbilcke-hf/FacePoke](https://github.com/jbilcke-hf/FacePoke)

## Acknowledgements

This project is based on LivePortrait: https://arxiv.org/abs/2407.03168

It uses the face transformation routines from https://github.com/PowerHouseMan/ComfyUI-AdvancedLivePortrait

## Installation

### Before you install

FacePoke has been tested in a Linux environment, using `Python 3.10` and `CUDA 12.4` (NVIDIA GPU). The application supports both GPU and CPU environments, with GPU being used by default when available.

### Local Setup

1. Make sure you have Git and Git LFS installed globally (https://git-lfs.com):

   ```bash
   git lfs install
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/jbilcke-hf/FacePoke.git
   cd FacePoke
   ```

3. Set up the virtual environment (recommended):

   ```bash
   # Create and setup virtual environment
   ./setup_env.sh
   
   # Activate the environment
   source activate_env.sh
   ```

   Or manually:
   ```bash
   python3 -m venv facepoke_env
   source facepoke_env/bin/activate
   pip install -r requirements_gradio.txt
   ```

4. Start the simple Gradio interface:
   ```bash
   # Run with GPU (default)
   python run_gradio.py

   # Force CPU usage
   python run_gradio.py --cpu

   # Run on different port
   python run_gradio.py --port 8080

   # Create public link
   python run_gradio.py --share
   ```

   The application will use GPU by default if available. Use the `--cpu` flag to force CPU usage if needed.

## Usage

1. **Upload a portrait photo** - Use a clear, front-facing photo for best results
2. **Choose an emotion** - Select from Happy, Sad, Angry, Surprised, or Thinking
3. **Click "Apply Emotion"** - Watch your portrait come to life!
4. **Download the result** - Save your animated portrait

### Tips for Best Results

- Use clear, well-lit portrait photos
- Make sure the face is clearly visible
- Front-facing photos work best
- High-quality images produce better results

## Docker Deployment

The Dockerfile is configured to run the Gradio interface on port 7860.

```bash
# Build the Docker image
docker build -t facepoke .

# Run with GPU support
docker run --gpus all -p 7860:7860 facepoke

# Run with CPU only
docker run -p 7860:7860 facepoke
```

## Development

### Project Structure

- `gradio_app.py` - Simple Gradio interface
- `run_gradio.py` - Startup script with CLI options
- `app.py` - Original aiohttp server (legacy)
- `engine.py` - Core animation engine
- `loader.py` - Model loading utilities
- `liveportrait/` - LivePortrait pipeline implementation

### Environment Management

The project uses a virtual environment to keep dependencies isolated:

```bash
# Create and setup environment
./setup_env.sh

# Activate environment
source activate_env.sh

# Deactivate environment
deactivate

# Test installation
python test_gradio.py
```

### Running in Development

```bash
# Start with debug logging
python run_gradio.py --port 7860

# Force CPU for testing
python run_gradio.py --cpu --port 7860
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
