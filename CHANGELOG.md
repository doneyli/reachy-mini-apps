# Changelog

All notable changes to this project will be documented in this file.

## [0.2.1] - 2025-12-23

### Fixed

#### Camera Live Feed App
- Changed port from 8080 to 8042 to match official template pattern
- Moved route setup to `run()` method (following official template)
- Added type annotation for `custom_app_url` class attribute

### Added
- Architecture diagram in README showing daemon/app relationship
- Processing load documentation for MJPEG streaming

## [0.2.0] - 2025-12-23

### Added

#### Camera Live Feed App
- Complete ReachyMiniApp implementation following official guide
- Entry point registration for robot dashboard discovery
- Static web UI with MJPEG streaming
- HuggingFace Spaces landing page (index.html, style.css)
- README with YAML frontmatter for HF publishing

#### Documentation
- DEPLOYMENT.md - Comprehensive deployment guide including:
  - SSH credentials and connection instructions
  - HuggingFace Spaces publishing workflow
  - Direct SSH installation from GitHub
  - Robot filesystem structure (/venvs/apps_venv/)
  - Python version verification steps
  - Daemon restart instructions

- TROUBLESHOOTING.md - Deep-dive debugging guide covering:
  - Python version mismatch problem (daemon uses 3.12, system has 3.13)
  - The critical pyvenv.cfg configuration for uv standalone Python
  - Entry point discovery issues and fixes
  - HuggingFace Spaces publishing gotchas (colorTo values, frontmatter)
  - Complete diagnosis and repair commands

### Fixed
- Entry point name: `camera-live-feed` (hyphens, not underscores)
- Python version constraint: `>=3.10` (robot runs 3.13.5)
- HuggingFace colorTo value: `indigo` (cyan not valid)

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
