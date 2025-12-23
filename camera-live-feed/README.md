# Camera Live Feed

A Reachy Mini app that streams live video from the robot's camera to a web dashboard.

Built following the official [Make and Publish Reachy Mini Apps](https://huggingface.co/blog/pollen-robotics/make-and-publish-your-reachy-mini-apps) guide.

## Features

- Live MJPEG video streaming at 15 FPS
- Snapshot capture with download
- Auto-reconnect on connection loss
- Responsive dashboard UI

## Installation

```bash
# From the monorepo root
uv sync

# Or install standalone
pip install -e camera-live-feed/
```

## Usage

### Via Robot Dashboard

1. Start the Reachy Mini daemon:
   ```bash
   reachy-mini-daemon
   ```

2. Open the dashboard at http://localhost:8000/ (or http://reachy-mini:8000/)

3. Find "Camera Live Feed" in the Applications section

4. Click **Run** to start the app

5. Click the **gear icon** to open the live feed UI

### API Endpoints

When the app is running, these endpoints are available:

| Endpoint | Description |
|----------|-------------|
| `/` | Dashboard UI |
| `/api/stream` | MJPEG video stream |
| `/api/snapshot` | Single JPEG frame |
| `/api/status` | Camera status JSON |

## Project Structure

```
camera-live-feed/
├── pyproject.toml
├── README.md
└── camera_live_feed/
    ├── __init__.py
    ├── main.py              # ReachyMiniApp implementation
    └── static/
        ├── index.html       # Dashboard UI
        ├── style.css        # Styling
        └── main.js          # Client-side logic
```

## Development

The app follows the standard Reachy Mini app structure:

- Inherits from `ReachyMiniApp`
- Implements `run(reachy_mini, stop_event)` method
- Uses `custom_app_url` for the settings UI
- Registers custom FastAPI routes for streaming

## Resources

- [Reachy Mini SDK](https://github.com/pollen-robotics/reachy_mini)
- [App Development Guide](https://huggingface.co/blog/pollen-robotics/make-and-publish-your-reachy-mini-apps)
- [SDK Python Reference](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/python-sdk.md)
