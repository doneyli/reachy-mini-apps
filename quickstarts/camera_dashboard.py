"""Camera Dashboard Demo

Streams live video from Reachy Mini's camera to a web dashboard.
Open http://localhost:8080 in your browser to view the feed.
Press Ctrl+C to stop the server.
"""

import threading
import time
import cv2
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
from reachy_mini import ReachyMini

# Global variables for frame sharing between threads
current_frame = None
frame_lock = threading.Lock()
running = True


def capture_frames(mini: ReachyMini):
    """Continuously capture frames from the robot's camera."""
    global current_frame, running

    print("Starting camera capture...")
    time.sleep(1.0)  # Let camera initialize

    while running:
        try:
            frame = mini.media.get_frame()
            if frame is not None:
                # Encode as JPEG
                _, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                with frame_lock:
                    current_frame = jpeg.tobytes()
        except Exception as e:
            print(f"Capture error: {e}")

        time.sleep(1.0 / 15)  # ~15 FPS


def generate_stream():
    """Generator for MJPEG streaming."""
    while running:
        with frame_lock:
            frame = current_frame

        if frame is not None:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )
        time.sleep(1.0 / 15)


# FastAPI app
app = FastAPI(title="Reachy Mini Camera Dashboard")


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the camera dashboard page."""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Reachy Mini Camera Dashboard</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 30px;
        }
        h1 {
            color: #00d4ff;
            margin-bottom: 10px;
            font-size: 2em;
        }
        .subtitle {
            color: #888;
            margin-bottom: 30px;
        }
        .video-container {
            background: #0f0f23;
            border-radius: 16px;
            padding: 15px;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.15);
            border: 1px solid rgba(0, 212, 255, 0.2);
        }
        img {
            display: block;
            max-width: 640px;
            width: 100%;
            border-radius: 8px;
        }
        .status {
            margin-top: 20px;
            padding: 10px 20px;
            background: rgba(0, 212, 255, 0.1);
            border-radius: 20px;
            font-size: 14px;
            color: #00d4ff;
        }
        .status::before {
            content: "";
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #00ff88;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .footer {
            margin-top: 30px;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h1>Reachy Mini Camera</h1>
    <p class="subtitle">Live video feed from the robot</p>
    <div class="video-container">
        <img src="/stream" alt="Live Camera Feed" />
    </div>
    <div class="status">Streaming live</div>
    <p class="footer">Press Ctrl+C in terminal to stop</p>
</body>
</html>
"""


@app.get("/stream")
async def video_stream():
    """Stream MJPEG video."""
    return StreamingResponse(
        generate_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/snapshot")
async def snapshot():
    """Get a single frame as JPEG."""
    with frame_lock:
        frame = current_frame
    if frame is None:
        return Response(content="No frame available", status_code=503)
    return Response(content=frame, media_type="image/jpeg")


if __name__ == "__main__":
    print("Connecting to Reachy Mini...")

    with ReachyMini(localhost_only=False) as mini:
        print("Connected!")

        # Start capture thread
        capture_thread = threading.Thread(target=capture_frames, args=(mini,), daemon=True)
        capture_thread.start()

        print("\n" + "=" * 50)
        print("  Camera Dashboard running!")
        print("  Open: http://localhost:8080")
        print("  Press Ctrl+C to stop")
        print("=" * 50 + "\n")

        try:
            uvicorn.run(app, host="0.0.0.0", port=8080, log_level="warning")
        except KeyboardInterrupt:
            pass
        finally:
            running = False
            print("\nShutting down...")
