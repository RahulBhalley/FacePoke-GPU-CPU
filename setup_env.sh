#!/bin/bash
# Setup script for FacePoke virtual environment

echo "🎭 Setting up FacePoke virtual environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "📝 Please install Python 3.10 or later."
    exit 1
fi

# Check if virtual environment already exists
if [ -d "facepoke_env" ]; then
    echo "⚠️  Virtual environment already exists!"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing environment..."
        rm -rf facepoke_env
    else
        echo "📝 Using existing environment."
        echo "🚀 To activate: source activate_env.sh"
        exit 0
    fi
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv facepoke_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source facepoke_env/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements_gradio.txt

# Run comprehensive dependency check
echo ""
echo "🔍 Checking all dependencies..."
python check_dependencies.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To activate the environment:"
echo "   source activate_env.sh"
echo ""
echo "🧪 To test the installation:"
echo "   python test_gradio.py"
echo ""
echo "🔍 To check dependencies:"
echo "   python check_dependencies.py"
echo ""
echo "🎭 To run the interface:"
echo "   python run_gradio.py"
