#!/bin/bash
# Simple script to activate the FacePoke virtual environment

echo "🎭 Activating FacePoke virtual environment..."

# Check if virtual environment exists
if [ ! -d "facepoke_env" ]; then
    echo "❌ Virtual environment not found!"
    echo "📝 Please run setup_env.sh first to create the environment."
    exit 1
fi

# Activate the virtual environment
source facepoke_env/bin/activate

echo "✅ Virtual environment activated!"
echo "🐍 Python: $(which python)"
echo "📦 Pip: $(which pip)"
echo ""
echo "🚀 To run the FacePoke Gradio interface:"
echo "   python run_gradio.py"
echo ""
echo "🧪 To test the installation:"
echo "   python test_gradio.py"
echo ""
echo "🔧 To deactivate the environment:"
echo "   deactivate"
