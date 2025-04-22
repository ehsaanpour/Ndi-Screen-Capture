#!/usr/bin/env python
import os
import subprocess
import sys
import platform

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 7):
        print(f"Error: Python 3.7 or higher is required. You have Python {major}.{minor}")
        return False
    return True

def install_requirements():
    """Install required packages using pip"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False

def check_ndi_sdk():
    """Check if NDI SDK is installed"""
    try:
        import NDIlib
        print("NDI SDK already installed.")
        return True
    except ImportError:
        print("NDI SDK not found. You need to install it manually.")
        system = platform.system()
        if system == "Windows":
            print("Download NDI SDK: https://ndi.tv/sdk/")
            print("After installation, run: pip install ndi-python")
        elif system == "Darwin":  # macOS
            print("Download NDI SDK: https://ndi.tv/sdk/")
            print("After installation, run: pip install ndi-python")
        elif system == "Linux":
            print("For Ubuntu, install Avahi first:")
            print("  sudo apt install avahi-daemon")
            print("  sudo systemctl enable --now avahi-daemon")
            print("Then download and install NDI SDK: https://ndi.tv/sdk/")
            print("After installation, run: pip install ndi-python")
        return False

def setup_environment():
    """Create necessary directories"""
    os.makedirs("static", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    return True

def main():
    """Main installation function"""
    print("NDI Screen Capture - Installation")
    print("=================================")
    
    if not check_python_version():
        return 1
    
    if not install_requirements():
        return 1
    
    if not check_ndi_sdk():
        print("\nWarning: NDI SDK installation required.")
        print("You'll need to install it manually before running the application.")
    
    if not setup_environment():
        return 1
    
    print("\nInstallation completed successfully!")
    print("\nTo start the application, run:")
    print("  python run.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 