# Session Notes - December 23, 2025

Notes for resuming work on the camera-live-feed app deployment.

## Current Status

**App installs and runs successfully on the robot**, but:
- No gear icon appears in the dashboard
- Direct URL access (http://reachy-mini:8080/) returns "Not Found"

## What We Learned

### Python Version Mismatch (SOLVED)

The robot has two Python versions:
- **Daemon**: Python 3.12.12 (uv standalone at `/home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/`)
- **System**: Python 3.13.5 (`/usr/bin/python3`)

Apps MUST be installed with Python 3.12 or the daemon won't find them.

**Fix applied:**
```bash
# Fix apps_venv to use Python 3.12
cd /venvs/apps_venv/bin/
rm -f python python3 python3.12 python3.13
ln -s /home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/bin/python3.12 python
ln -s python python3
ln -s python python3.12

# Fix pyvenv.cfg
echo 'home = /home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/bin' > /venvs/apps_venv/pyvenv.cfg
echo 'implementation = CPython' >> /venvs/apps_venv/pyvenv.cfg
echo 'version_info = 3.12.12' >> /venvs/apps_venv/pyvenv.cfg
echo 'include-system-site-packages = false' >> /venvs/apps_venv/pyvenv.cfg
```

### ReachyMiniApp Base Class (from /venvs/apps_venv/lib/python3.12/site-packages/reachy_mini/apps/app.py)

Key findings:

1. **`custom_app_url`** must be a full URL with port (e.g., `http://0.0.0.0:8080`)

2. **`settings_app`** (FastAPI instance) is only created when:
   - `custom_app_url is not None`
   - `dont_start_webserver` is False

3. **Base class automatically handles**:
   - Creating FastAPI app
   - Mounting static files from `{app_module_path}/static/`
   - Serving `index.html` at root `/`
   - Starting uvicorn server on the URL's hostname:port

4. **`wrapped_run()` method** starts uvicorn in a thread when settings_app exists

### What's NOT Working

The gear icon and direct URL access aren't working. Possible reasons:

1. **Dashboard doesn't know about the custom_app_url** - The daemon may need to query this from the app somehow

2. **App's server isn't starting** - The uvicorn server in `wrapped_run()` may not be launching

3. **Port 8080 might be blocked/in-use** - Firewall or another service

4. **Dashboard UI looks elsewhere** - The gear icon URL might come from a different source (HuggingFace metadata, daemon config, etc.)

## Files Structure

```
camera-live-feed/
├── pyproject.toml              # Entry point: camera-live-feed = camera_live_feed.main:CameraLiveFeed
├── README.md                   # HuggingFace frontmatter
├── index.html                  # HF Space landing page
├── style.css                   # HF Space styling
└── camera_live_feed/
    ├── __init__.py
    ├── main.py                 # CameraLiveFeed(ReachyMiniApp)
    └── static/
        ├── index.html          # App UI
        ├── style.css
        └── main.js
```

## Current main.py Configuration

```python
class CameraLiveFeed(ReachyMiniApp):
    custom_app_url = "http://0.0.0.0:8080"
    request_media_backend = "default"

    def __init__(self, running_on_wireless: bool = False) -> None:
        super().__init__(running_on_wireless=running_on_wireless)
        # ... frame capture setup ...
        if self.settings_app is not None:
            self._setup_routes()  # Adds /api/stream, /api/snapshot, /api/status
```

## Next Steps to Investigate

### 1. Check if uvicorn server starts
```bash
# While app is toggled ON, check if port 8080 is listening
ss -tlnp | grep 8080
# or
netstat -tlnp | grep 8080
```

### 2. Check daemon logs for uvicorn startup
```bash
journalctl -u reachy-mini-daemon -f
# Toggle app ON and look for uvicorn/server startup messages
```

### 3. Check if another app with gear icon exists
Look at HuggingFace for Reachy Mini apps that have working settings UIs:
- https://huggingface.co/spaces?search=reachy_mini

### 4. Check daemon source code
The daemon decides whether to show the gear icon. Look at:
```bash
cat /venvs/mini_daemon/lib/python3.12/site-packages/reachy_mini/daemon/app/routers/apps.py
```

### 5. Try a different port
Port 8080 might conflict. Try:
```python
custom_app_url = "http://0.0.0.0:8888"
```

### 6. Check if app needs to be running for gear icon
Some dashboards only show the gear icon when the app is actively running.

## Robot SSH Access

```bash
ssh pollen@reachy-mini
# Password: root
```

## Useful Commands

```bash
# Check installed apps
/venvs/apps_venv/bin/python -c "from importlib.metadata import entry_points; eps = entry_points(group='reachy_mini_apps'); [print(f'{ep.name}: {ep.value}') for ep in eps]"

# Reinstall app
/venvs/apps_venv/bin/python -m pip install --upgrade "git+https://github.com/doneyli/reachy-mini-apps.git#subdirectory=camera-live-feed"

# Restart daemon
sudo systemctl restart reachy-mini-daemon

# View daemon logs
journalctl -u reachy-mini-daemon -f

# Check listening ports
ss -tlnp
```

## Repository

https://github.com/doneyli/reachy-mini-apps

## Documentation Created

- `DEPLOYMENT.md` - Deployment guide with Python version fix
- `TROUBLESHOOTING.md` - Deep-dive debugging guide
- `CHANGELOG.md` - Version history
- `SESSION_NOTES.md` - This file
