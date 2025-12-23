# Prompt Version History

This file tracks all prompts used to build and evolve this repository.
LLMs should read this file to understand the project's evolution and context.

---

## Prompt 0 — Initial Repository Setup

**File:** `reachy-mini-prompt-0.md`
**Date:** 2024-12-22
**Status:** Completed

### Summary

Initial setup of the reachy-mini-apps monorepo with:

- uv workspace structure with root `pyproject.toml`
- Shared library (`packages/shared`) with:
  - Robot connection wrapper using context manager pattern
  - ClickHouse client wrapper
- First app (`camera-live-feed`) for live video streaming
- Dependencies: reachy-mini v1.2+, clickhouse-connect, numpy, opencv-python

### Files Created

```
pyproject.toml
.python-version
README.md
PROMPTS.md
packages/shared/pyproject.toml
packages/shared/src/shared/__init__.py
packages/shared/src/shared/robot.py
packages/shared/src/shared/clickhouse.py
camera-live-feed/pyproject.toml
camera-live-feed/main.py
```

### Key Decisions

1. Python 3.12 as target version (updated from 3.11 per official SDK docs)
2. Context manager pattern (`with ReachyMini() as mini:`) for robot connections
3. Graceful error handling for disconnected robot scenarios
4. Shared library uses `src/` layout for proper packaging
5. Apps live at root level (not under `apps/` directory) for flatter structure

---

## Prompt 1 — SDK Installation & Wireless Setup

**File:** N/A (interactive session)
**Date:** 2024-12-22
**Status:** Completed

### Summary

Installed and configured the reachy-mini SDK on macOS for connecting to a wireless Reachy Mini robot. Followed official installation guide and resolved GStreamer dependencies required for network video streaming.

### Prerequisites Installed

- **uv** package manager
- **Python 3.12** (via `uv python install 3.12 --default`)
- **Git LFS** (via `brew install git-lfs && git lfs install`)
- **GStreamer** (via `brew install gstreamer pkg-config`)

### Files Modified

```
.python-version                    # Changed from 3.11 to 3.12
packages/shared/pyproject.toml     # Added [gstreamer] extra to reachy-mini
camera-live-feed/main.py           # Updated to use SDK's actual API (robot_name, localhost_only)
packages/shared/src/shared/robot.py # Updated wrapper to match SDK API
```

### Key Decisions

1. **Python 3.12**: Required by official SDK installation guide
2. **GStreamer extra**: Required for network video streaming (`reachy-mini[gstreamer]`)
3. **NOT wireless-version extra**: The `wireless-version` extra is for running ON the robot (requires lgpio/RPi), not for connecting TO the robot from macOS
4. **SDK API parameters**:
   - `robot_name` for discovery (default: "reachy_mini")
   - `localhost_only=False` for network connections
   - No `host` parameter exists in SDK

### Robot Connection Requirements

For the camera app to work, the robot must have:
- Port 8443 open (WebRTC signaling server)
- The reachy-mini-daemon running

### Running the App

```bash
uv run camera-live-feed/main.py           # Connect over network (default)
uv run camera-live-feed/main.py --local   # Connect to localhost only
```

---

## Prompt 2 — Convert to Reachy Mini App Format

**File:** N/A (interactive session)
**Date:** 2024-12-22
**Status:** Completed

### Summary

Converted the camera-live-feed from a standalone script to a proper Reachy Mini App that can be installed on the robot via the dashboard or published to Hugging Face.

### Key Changes

1. **App Structure**: Created proper Python package structure:
   ```
   camera-live-feed/
   ├── pyproject.toml           # With reachy_mini.apps entry point
   ├── README.md
   └── camera_live_feed/
       ├── __init__.py
       └── main.py              # CameraLiveFeedApp class
   ```

2. **ReachyMiniApp Base Class**: App now inherits from `reachy_mini.apps.app.ReachyMiniApp`

3. **Web-Based Streaming**: Since the robot is headless (no display), replaced `cv2.imshow()` with:
   - MJPEG streaming endpoint (`/camera/stream`)
   - Web UI at `/camera`
   - Snapshot endpoint (`/camera/snapshot`)

### Files Created/Modified

```
camera-live-feed/pyproject.toml        # Entry point for reachy_mini.apps
camera-live-feed/README.md             # App documentation
camera-live-feed/camera_live_feed/__init__.py
camera-live-feed/camera_live_feed/main.py  # CameraLiveFeedApp class
```

Removed: `camera-live-feed/main.py` (old standalone script)

### Deployment Options

**Option 1: Install directly on robot via pip**
```bash
# SSH into robot
ssh reachy@reachy-mini.local

# Install the app
pip install git+https://github.com/YOUR_USER/reachy-mini-apps.git#subdirectory=camera-live-feed

# The app will appear in the dashboard
```

**Option 2: Publish to Hugging Face**
```bash
# Use the app assistant
reachy-mini-app-assistant publish

# App becomes installable from dashboard's App Store
```

### Web UI Endpoints

Once running on the robot, access via browser:
- `http://reachy-mini.local:8000/camera` - Live video player
- `http://reachy-mini.local:8000/camera/stream` - Raw MJPEG stream
- `http://reachy-mini.local:8000/camera/snapshot` - Single frame

### Key Decisions

1. **MJPEG over WebRTC**: Simpler implementation, works in all browsers
2. **Standalone dependencies**: App no longer depends on shared library
3. **Entry point registration**: Uses `[project.entry-points."reachy_mini.apps"]`

---

## Adding New Prompts

When adding a new prompt:

1. Create a new file: `reachy-mini-prompt-N.md` (increment N)
2. Add a new section below following this template:

```markdown
## Prompt N — Title

**File:** `reachy-mini-prompt-N.md`
**Date:** YYYY-MM-DD
**Status:** Pending | In Progress | Completed

### Summary

Brief description of what this prompt accomplishes.

### Files Created/Modified

- List of files

### Key Decisions

- Important architectural or implementation decisions made
```
