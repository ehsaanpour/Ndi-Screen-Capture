# NDI Screen Capture Web App

A web-based application to capture and stream your tablet's screen via NDI (Network Device Interface) over WiFi.

## Features

- Capture the tablet's screen and transmit it as an NDI source
- Adjustable frame rate for different performance needs
- Live preview within the web interface
- Compatible with any NDI-enabled receiving device
- Simple and intuitive user interface

## Prerequisites

Before using this application, you need to:

1. Install the NDI SDK on your device: [Download from NDI.tv](https://ndi.tv/sdk/)
2. Ensure Python 3.7+ is installed
3. Your device should be connected to the same WiFi network as your NDI receivers

## Installation

1. Clone this repository or download it:

```bash
git clone https://github.com/yourusername/ndi-screen-capture.git
cd ndi-screen-capture
```

2. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:

```bash
cd ndi_screen_capture
python app.py
```

2. Open a web browser and go to `http://localhost:8000` (or the appropriate IP address if accessing from another device on the network)

3. Click "Start Streaming" in the web interface to begin capturing and streaming your screen

4. Your screen is now available as an NDI source named "Tablet Screen Capture" that can be received by any NDI-compatible software or hardware on the same network

5. Adjust the frame rate using the slider if needed

6. Click "Stop Streaming" when you're done

## Receiving the NDI Stream

To view the stream on another device:

1. Install NDI Studio Monitor or any NDI-compatible software on the receiving device
2. Open the software and look for the source named "Tablet Screen Capture"
3. Select this source to view the stream

## Troubleshooting

- **NDI source not found**: Ensure both devices are on the same network and that the NDI SDK is properly installed
- **Poor performance**: Try lowering the frame rate using the slider
- **Application crashes**: Check that all dependencies are correctly installed. 

## Technical Details

- The application uses Python with FastAPI for the web server
- Screen capture is handled by MSS and OpenCV
- NDI communication uses the official NDI Python SDK
- The web interface uses standard HTML, CSS, and JavaScript with WebSockets for the preview.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
