"""Camera Live Feed - Streams video from Reachy Mini's camera to dashboard UI."""

import threading
import time
import cv2
from fastapi import Response
from fastapi.responses import StreamingResponse
from reachy_mini import ReachyMini
from reachy_mini.apps.app import ReachyMiniApp


class CameraLiveFeed(ReachyMiniApp):
    """
    Reachy Mini App that streams live camera feed to the robot's dashboard.

    When running, access the live feed at the custom_app_url (default: http://reachy-mini:8080)
    """

    # Full URL - the base class starts a uvicorn server on this port
    # and automatically serves static/ files and index.html
    custom_app_url = "http://0.0.0.0:8080"
    request_media_backend = "default"

    def __init__(self, running_on_wireless: bool = False) -> None:
        """Initialize the camera app."""
        super().__init__(running_on_wireless=running_on_wireless)

        self._current_frame: bytes | None = None
        self._frame_lock = threading.Lock()
        self._fps = 15
        self._jpeg_quality = 80

        # Register custom API routes (static files handled by base class)
        if self.settings_app is not None:
            self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up FastAPI routes for camera streaming."""

        @self.settings_app.get("/api/stream")
        async def video_stream():
            """Stream MJPEG video."""
            return StreamingResponse(
                self._generate_mjpeg_stream(),
                media_type="multipart/x-mixed-replace; boundary=frame"
            )

        @self.settings_app.get("/api/snapshot")
        async def snapshot():
            """Get a single frame as JPEG."""
            with self._frame_lock:
                frame = self._current_frame
            if frame is None:
                return Response(content="No frame available", status_code=503)
            return Response(content=frame, media_type="image/jpeg")

        @self.settings_app.get("/api/status")
        async def status():
            """Get camera status."""
            with self._frame_lock:
                has_frame = self._current_frame is not None
            return {
                "streaming": has_frame,
                "fps": self._fps,
                "quality": self._jpeg_quality
            }

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event) -> None:
        """
        Main app loop - captures frames from the camera.

        Args:
            reachy_mini: The connected Reachy Mini instance.
            stop_event: Event to signal graceful shutdown.
        """
        self.logger.info("Starting camera capture...")
        frame_interval = 1.0 / self._fps

        # Let camera initialize
        time.sleep(1.0)

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
                self.logger.error(f"Error capturing frame: {e}")

            # Maintain target FPS
            elapsed = time.time() - start_time
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def _generate_mjpeg_stream(self):
        """Generator for MJPEG streaming."""
        while not self.stop_event.is_set():
            with self._frame_lock:
                frame = self._current_frame

            if frame is not None:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            time.sleep(1.0 / self._fps)
