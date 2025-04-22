#!/usr/bin/env python
import os
import subprocess
import sys
import time
from create_placeholder import create_placeholder_image

def main():
    """
    Run the NDI Screen Capture application
    """
    print("Starting NDI Screen Capture...")
    
    # Create the static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)
    
    # Create the placeholder image if it doesn't exist
    if not os.path.exists("static/placeholder.png"):
        print("Generating placeholder image...")
        create_placeholder_image("static/placeholder.png")
    
    # Check if NDI SDK is installed
    try:
        import NDIlib as ndi
        print("NDI SDK found. Version:", ndi.__version__ if hasattr(ndi, "__version__") else "Unknown")
    except ImportError:
        print("Error: NDI SDK not found.")
        print("Please install the NDI SDK from https://ndi.tv/sdk/")
        print("Then install the Python wrapper with: pip install ndi-python")
        return 1
    
    # Start the FastAPI application
    print("Starting web server...")
    print("Access the application at http://localhost:8000")
    print("Press Ctrl+C to stop")
    
    try:
        # Use uvicorn to run the FastAPI app
        import uvicorn
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error starting the server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 