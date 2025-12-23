# Camera Live Feed

A Reachy Mini App that streams live video from the robot's camera to your web browser.

## Features

- Live MJPEG video stream viewable in any browser
- Single-frame snapshot endpoint
- Optimized for low-latency streaming

## Installation

Install from the Reachy Mini dashboard's App Store, or manually:

```bash
pip install camera-live-feed
```

## Usage

Once installed and started from the dashboard, open your browser to:

```
http://reachy-mini.local:8000/camera
```

### Endpoints

- `/camera` - Web UI with live video player
- `/camera/stream` - Raw MJPEG stream
- `/camera/snapshot` - Single JPEG frame

## Development

```bash
# Clone and install in development mode
cd camera-live-feed
pip install -e .

# Run with the daemon
reachy-mini-daemon
```

## License

MIT
