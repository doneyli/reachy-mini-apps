"""Camera Live Feed App - streams video from Reachy Mini's camera to a web UI."""

import base64
import threading
import time
from typing import Any

import cv2
from reachy_mini import ReachyMini
from reachy_mini.apps.app import ReachyMiniApp


class CameraLiveFeedApp(ReachyMiniApp):
    """
    Reachy Mini App that streams live camera feed to a web interface.

    The video is captured from the robot's camera and served via MJPEG
    streaming to the browser.
    """

    custom_app_url = "/camera"
    request_media_backend = "default"

    def __init__(self, running_on_wireless: bool = False) -> None:
        """Initialize the camera app."""
        super().__init__(running_on_wireless=running_on_wireless)
        self._current_frame: bytes | None = None
        self._frame_lock = threading.Lock()
        self._fps = 15
        self._jpeg_quality = 80

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event) -> None:
        """
        Main app loop - captures frames and stores them for streaming.

        Args:
            reachy_mini: The connected Reachy Mini instance.
            stop_event: Event to signal graceful shutdown.
        """
        frame_interval = 1.0 / self._fps

        while not stop_event.is_set():
            start_time = time.time()

            try:
                frame = reachy_mini.media.get_frame()

                if frame is not None:
                    # Encode frame as JPEG
                    encode_params = [cv2.IMWRITE_JPEG_QUALITY, self._jpeg_quality]
                    _, jpeg = cv2.imencode(".jpg", frame, encode_params)

                    with self._frame_lock:
                        self._current_frame = jpeg.tobytes()

            except Exception as e:
                print(f"Error capturing frame: {e}")

            # Maintain target FPS
            elapsed = time.time() - start_time
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def get_frame(self) -> bytes | None:
        """Get the current frame as JPEG bytes (thread-safe)."""
        with self._frame_lock:
            return self._current_frame

    def generate_mjpeg_stream(self):
        """Generator for MJPEG streaming."""
        while True:
            frame = self.get_frame()
            if frame is not None:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            time.sleep(1.0 / self._fps)


# FastAPI routes for the web UI
def setup_routes(app: Any, camera_app: CameraLiveFeedApp) -> None:
    """Set up FastAPI routes for the camera stream."""
    from fastapi import Response
    from fastapi.responses import HTMLResponse, StreamingResponse

    @app.get("/camera", response_class=HTMLResponse)
    async def camera_page():
        """Serve the camera viewing page."""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Reachy Mini Camera</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: #1a1a2e;
            color: #eee;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        h1 {
            color: #00d4ff;
            margin-bottom: 20px;
        }
        .video-container {
            background: #16213e;
            border-radius: 12px;
            padding: 10px;
            box-shadow: 0 4px 20px rgba(0, 212, 255, 0.2);
        }
        img {
            max-width: 100%;
            border-radius: 8px;
        }
        .status {
            margin-top: 15px;
            color: #00d4ff;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>Reachy Mini Camera</h1>
    <div class="video-container">
        <img src="/camera/stream" alt="Live Camera Feed" />
    </div>
    <p class="status">Live stream from Reachy Mini</p>
</body>
</html>
"""

    @app.get("/camera/stream")
    async def video_stream():
        """Stream MJPEG video."""
        return StreamingResponse(
            camera_app.generate_mjpeg_stream(),
            media_type="multipart/x-mixed-replace; boundary=frame",
        )

    @app.get("/camera/snapshot")
    async def snapshot():
        """Get a single frame as JPEG."""
        frame = camera_app.get_frame()
        if frame is None:
            return Response(content="No frame available", status_code=503)
        return Response(content=frame, media_type="image/jpeg")
