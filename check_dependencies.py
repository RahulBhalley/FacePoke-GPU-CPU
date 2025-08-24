#!/usr/bin/env python3
"""
Comprehensive dependency check for FacePoke
"""

import sys
import importlib

def check_dependency(module_name, package_name=None):
    """Check if a dependency is available"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError:
        print(f"❌ {package_name or module_name} - MISSING")
        return False

def main():
    print("🔍 Checking FacePoke Dependencies")
    print("=" * 40)
    
    # Core dependencies
    print("\n📦 Core Dependencies:")
    core_deps = [
        ("gradio", "Gradio"),
        ("torch", "PyTorch"),
        ("torchvision", "TorchVision"),
        ("torchaudio", "TorchAudio"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy"),
        ("cv2", "OpenCV"),
        ("scipy", "SciPy"),
        ("imageio", "ImageIO"),
        ("tqdm", "TQDM"),
        ("rich", "Rich"),
        ("yaml", "PyYAML"),
        ("aiohttp", "aiohttp"),
        ("async_lru", "async-lru"),
        ("tyro", "tyro"),
        ("omegaconf", "OmegaConf"),
        ("pydantic", "Pydantic"),
    ]
    
    core_missing = []
    for module, name in core_deps:
        if not check_dependency(module, name):
            core_missing.append(name)
    
    # ONNX dependencies
    print("\n🤖 ONNX Dependencies:")
    onnx_deps = [
        ("onnxruntime", "ONNX Runtime"),
        ("onnx", "ONNX"),
    ]
    
    onnx_missing = []
    for module, name in onnx_deps:
        if not check_dependency(module, name):
            onnx_missing.append(name)
    
    # ML dependencies
    print("\n🧠 ML Dependencies:")
    ml_deps = [
        ("diffusers", "Diffusers"),
        ("accelerate", "Accelerate"),
        ("transformers", "Transformers"),
        ("huggingface_hub", "HuggingFace Hub"),
        ("safetensors", "Safetensors"),
        ("einops", "Einops"),
    ]
    
    ml_missing = []
    for module, name in ml_deps:
        if not check_dependency(module, name):
            ml_missing.append(name)
    
    # Custom modules
    print("\n🔧 Custom Modules:")
    custom_deps = [
        ("liveportrait", "LivePortrait"),
        ("engine", "Engine"),
        ("loader", "Loader"),
    ]
    
    custom_missing = []
    for module, name in custom_deps:
        if not check_dependency(module, name):
            custom_missing.append(name)
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 SUMMARY:")
    
    all_missing = core_missing + onnx_missing + ml_missing + custom_missing
    
    if not all_missing:
        print("🎉 All dependencies are installed!")
        print("\n🚀 You can now run:")
        print("   python run_gradio.py")
        return True
    else:
        print(f"❌ Missing {len(all_missing)} dependencies:")
        for dep in all_missing:
            print(f"   - {dep}")
        
        print("\n🔧 To install missing dependencies:")
        print("   pip install -r requirements_gradio.txt")
        
        if onnx_missing:
            print("\n🤖 For ONNX dependencies:")
            print("   pip install onnx onnxruntime")
        
        if ml_missing:
            print("\n🧠 For ML dependencies:")
            print("   pip install diffusers accelerate transformers huggingface-hub safetensors einops")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
