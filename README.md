# Reachy Mini Apps

A monorepo for Reachy Mini robot applications using [uv](https://docs.astral.sh/uv/) workspace.

## Prerequisites

- **Python 3.10-3.12** (required by reachy-mini SDK)
- **Git** with **Git LFS** (for model assets)
- **[uv](https://docs.astral.sh/uv/)** package manager
- **GStreamer** (for audio/video streaming)
- Reachy Mini robot (connected via USB or network)

See the [official SDK installation guide](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/installation.md) for detailed instructions.

## Installation

### 1. Install uv (if not already installed)

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install Git LFS and GStreamer

**macOS (with Homebrew):**
```bash
brew install git-lfs gstreamer libnice-gstreamer
git lfs install
```

**Linux:**
```bash
sudo apt install git-lfs gstreamer1.0-plugins-bad gstreamer1.0-nice
git lfs install
```

### 3. Clone and setup the project

```bash
git clone <repo-url>
cd reachy-mini-apps

# Install Python 3.12 and sync dependencies
uv python install 3.12
uv sync
```

### 4. Run commands

Use `uv run` to execute scripts (no activation needed):
```bash
uv run python hello.py
```

Or activate the virtual environment:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

## Project Structure

```
reachy-mini-apps/
├── pyproject.toml          # Root workspace configuration
├── quickstarts/            # Simple example scripts
│   └── wiggle_antennas.py  # Antenna wiggle demo
├── packages/
│   └── shared/             # Shared library (robot connection, ClickHouse client)
└── camera-live-feed/       # Live camera streaming app
```

## Connecting to Reachy Mini

Before running scripts, ensure the daemon is running. See the [quickstart guide](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/quickstart.md).

**Basic connection (local):**
```python
from reachy_mini import ReachyMini

with ReachyMini() as mini:
    # Your code here
```

**Wireless connection (Reachy Mini Lite):**
```python
with ReachyMini(localhost_only=False) as mini:
    # Your code here
```

## Running Apps

### Wiggle Antennas

Test your connection with the antenna wiggle demo:
```bash
uv run python quickstarts/wiggle_antennas.py
```

### Camera Live Feed

Stream live video from the robot's camera:

```bash
uv run camera-live-feed/main.py
```

Press `q` to quit the video stream.

## Development

### Adding a New App

1. Create a new directory in the root:
   ```bash
   mkdir my-new-app
   ```

2. Create a `pyproject.toml` with dependencies:
   ```toml
   [project]
   name = "my-new-app"
   version = "0.1.0"
   dependencies = ["shared"]
   ```

3. Add the app to the workspace in root `pyproject.toml`:
   ```toml
   [tool.uv.workspace]
   members = ["packages/*", "camera-live-feed", "my-new-app"]
   ```

4. Create your `main.py` and run:
   ```bash
   uv run my-new-app/main.py
   ```

### Shared Library

The `packages/shared` library provides:

- `get_robot_connection()` - Context manager for robot connections
- `RobotConnectionError` - Exception for connection failures
- `ClickHouseClient` - Wrapper for ClickHouse database operations

## Hardware Modes

- **Lite Mode**: Apps run on a computer connected to the robot over network
- **On-Robot**: Apps run directly on the robot's embedded computer

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.
