---
title: Camera Live Feed
emoji: 📷
colorFrom: blue
colorTo: indigo
sdk: static
pinned: false
short_description: Live camera streaming dashboard for Reachy Mini
tags:
  - reachy_mini
  - reachy_mini_python_app
---

# Camera Live Feed

A Reachy Mini app that streams live video from the robot's camera to a web dashboard.

Built following the official [Make and Publish Reachy Mini Apps](https://huggingface.co/blog/pollen-robotics/make-and-publish-your-reachy-mini-apps) guide.

## Features

- Live MJPEG video streaming at 15 FPS
- Snapshot capture with download
- Auto-reconnect on connection loss
- Responsive dashboard UI

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           Reachy Mini Robot                                  │
│                                                                              │
│  ┌─────────────────────────────────┐    ┌──────────────────────────────┐    │
│  │  Reachy Mini Daemon (port 8000) │    │  Camera Live Feed (port 8042)│    │
│  │  ─────────────────────────────  │    │  ────────────────────────────│    │
│  │  • Main dashboard UI            │    │  • MJPEG video stream        │    │
│  │  • App management               │    │  • Snapshot API              │    │
│  │  • Shows gear icon when app     │───▶│  • Status endpoint           │    │
│  │    is running                   │    │  • Static UI files           │    │
│  └─────────────────────────────────┘    └──────────────────────────────┘    │
│           ▲                                         ▲                        │
└───────────│─────────────────────────────────────────│────────────────────────┘
            │                                         │
            │ http://reachy-mini:8000/                │ http://reachy-mini:8042/
            │                                         │
┌───────────│─────────────────────────────────────────│────────────────────────┐
│           │               Your Computer             │                        │
│           ▼                                         ▼                        │
│  ┌─────────────────────────────────┐    ┌──────────────────────────────┐    │
│  │  Browser Tab 1                  │    │  Browser Tab 2               │    │
│  │  ─────────────────────────────  │    │  ────────────────────────────│    │
│  │  Dashboard - toggle app on/off  │    │  Live camera feed viewer     │    │
│  │  Click ⚙️ gear icon to open ────────▶│  (opened via gear icon)      │    │
│  │  settings UI                    │    │                              │    │
│  └─────────────────────────────────┘    └──────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### How It Works

1. **Daemon (port 8000)**: The main Reachy Mini service that manages all apps
2. **Camera App (port 8042)**: Runs its own web server when activated
3. **Gear Icon**: Appears in dashboard only when the app is running
4. **MJPEG Streaming**: Low-overhead streaming that works in any browser

### Processing Load

The MJPEG streaming is handled entirely on the robot's Raspberry Pi:
- Frame capture from camera: ~5% CPU
- JPEG encoding at 15 FPS: ~10-15% CPU
- HTTP serving: negligible

This is well within the Pi's capabilities for local network streaming.

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

When the app is running, these endpoints are available at `http://reachy-mini:8042`:

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
