# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-12-22

### Added

#### Quickstart Examples
- `wiggle_antennas.py` - Basic connection test with antenna control
- `head_movement.py` - Head position control (x, y, z coordinates)
- `body_rotation.py` - Body yaw rotation demo
- `camera_capture.py` - Capture and save a single frame from robot camera
- `camera_dashboard.py` - Live MJPEG web dashboard (http://localhost:8080)
- `combined_movement.py` - Multi-joint control with interpolation styles (linear, minjerk, ease, cartoon)

#### Documentation
- Main README with About Reachy Mini section and setup instructions
- Quickstarts README with API reference and movement limits
- Links to official SDK documentation

#### Project Setup
- uv workspace configuration for monorepo structure
- Shared library package for robot connection utilities
- Camera live feed app with MJPEG streaming
- Apache 2.0 license

### Fixed

#### macOS GStreamer Setup
- Added `gst-signalling` as explicit dependency (not declared by reachy-mini SDK)
- Documented `libnice-gstreamer` requirement for WebRTC support
- Camera capture retry logic with initialization delay

### Dependencies
- Python 3.10-3.12 (required by reachy-mini SDK)
- reachy-mini >= 1.2.4
- gst-signalling >= 1.1.2
- GStreamer with libnice-gstreamer plugin (macOS: `brew install gstreamer libnice-gstreamer`)

### Notes

#### macOS Installation
```bash
# Required for WebRTC/audio features
brew install gstreamer libnice-gstreamer
```

#### Running Examples
```bash
uv run python quickstarts/wiggle_antennas.py
uv run python quickstarts/camera_dashboard.py  # Opens web UI at localhost:8080
```
