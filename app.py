import os
import time
import threading
import numpy as np
import cv2
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import mss
import pyautogui
from PIL import Image
from io import BytesIO
import base64

# Import NDI library
try:
    import NDIlib as ndi
except ImportError:
    print("Error: NDI SDK not found. Please install NDI SDK and ndi-python.")
    print("Try: pip install ndi-python")
    exit(1)

app = FastAPI(title="NDI Screen Capture", description="Capture and stream tablet screen over NDI")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Global variables
capturing = False
capture_thread = None
ndi_sender = None
frame_rate = 30
screen_width, screen_height = pyautogui.size()

def initialize_ndi():
    """Initialize NDI sender"""
    if not ndi.initialize():
        return False, "Failed to initialize NDI"
    
    # Create NDI sender
    ndi_send_settings = ndi.SendCreate()
    ndi_send_settings.ndi_name = "Tablet Screen Capture"
    
    sender = ndi.send_create(ndi_send_settings)
    if sender is None:
        ndi.destroy()
        return False, "Failed to create NDI sender"
    
    # Create NDI video frame
    video_frame = ndi.VideoFrameV2()
    video_frame.xres = screen_width
    video_frame.yres = screen_height
    video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_RGBA
    
    return True, {"sender": sender, "video_frame": video_frame}

def capture_screen_to_ndi():
    """Capture screen and send to NDI"""
    global capturing
    
    # Initialize NDI
    success, result = initialize_ndi()
    if not success:
        print(f"NDI Initialization failed: {result}")
        return
    
    sender = result["sender"]
    video_frame = result["video_frame"]
    
    # Initialize screen capture
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": screen_width, "height": screen_height}
    
    try:
        while capturing:
            start_time = time.time()
            
            # Capture screen
            img = sct.grab(monitor)
            frame = np.array(img)
            
            # Convert to RGBA format for NDI
            if frame.shape[2] == 3:  # If RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            
            # Set NDI video frame data
            video_frame.data = frame.tobytes()
            
            # Send frame via NDI
            ndi.send_send_video_v2(sender, video_frame)
            
            # Control frame rate
            elapsed = time.time() - start_time
            sleep_time = max(0, 1.0/frame_rate - elapsed)
            time.sleep(sleep_time)
    
    finally:
        # Clean up NDI
        if sender:
            ndi.send_destroy(sender)
        ndi.destroy()

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """Serve the index page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status")
async def get_status():
    """Get the current streaming status"""
    return {"capturing": capturing, "frame_rate": frame_rate}

@app.post("/start")
async def start_capture():
    """Start the screen capture and NDI streaming"""
    global capturing, capture_thread
    
    if capturing:
        return {"status": "already_running", "message": "Screen capture already running"}
    
    capturing = True
    capture_thread = threading.Thread(target=capture_screen_to_ndi)
    capture_thread.daemon = True
    capture_thread.start()
    
    return {"status": "started", "message": "Screen capture started"}

@app.post("/stop")
async def stop_capture():
    """Stop the screen capture and NDI streaming"""
    global capturing
    
    if not capturing:
        return {"status": "not_running", "message": "Screen capture is not running"}
    
    capturing = False
    
    # Wait for thread to finish
    if capture_thread and capture_thread.is_alive():
        capture_thread.join(timeout=3.0)
    
    return {"status": "stopped", "message": "Screen capture stopped"}

@app.post("/set_frame_rate")
async def set_frame_rate(rate: int):
    """Set the frame rate for NDI streaming"""
    global frame_rate
    
    if rate < 1:
        return {"status": "error", "message": "Frame rate must be at least 1"}
    
    if rate > 60:
        return {"status": "error", "message": "Frame rate cannot exceed 60"}
    
    frame_rate = rate
    return {"status": "success", "message": f"Frame rate set to {rate} fps"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for preview stream"""
    await websocket.accept()
    
    # Initialize screen capture
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": screen_width, "height": screen_height}
    preview_fps = 5  # Lower frame rate for preview
    
    try:
        while True:
            # Check if client is still connected
            if websocket.client_state.DISCONNECTED:
                break
            
            # Capture screen
            img = sct.grab(monitor)
            frame = np.array(img)
            
            # Resize for preview to save bandwidth
            scale_percent = 50
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            
            # Convert to JPEG for lower bandwidth
            img_pil = Image.fromarray(resized)
            buffer = BytesIO()
            img_pil.save(buffer, format="JPEG", quality=70)
            
            # Encode as base64 to send over WebSocket
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            await websocket.send_text(f"data:image/jpeg;base64,{img_str}")
            
            # Control frame rate
            time.sleep(1/preview_fps)
    
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")

@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on application shutdown"""
    global capturing
    capturing = False
    if ndi_sender:
        ndi.send_destroy(ndi_sender)
    ndi.destroy()

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 