# Deployment Guide

Guide for deploying Reachy Mini apps to the robot.

## Robot Connection

**SSH Credentials:**
- Host: `reachy-mini` (or `192.168.1.15` on local network)
- Username: `pollen`
- Password: `root`

```bash
ssh pollen@reachy-mini
```

## Deployment Methods

### Method 1: HuggingFace Spaces (Recommended)

The official way to distribute Reachy Mini apps.

#### Prerequisites
- HuggingFace account and token
- App passes all checks

#### Steps

1. **Check your app:**
   ```bash
   cd camera-live-feed
   reachy-mini-app-assistant check
   ```

2. **Publish to HuggingFace:**
   ```bash
   reachy-mini-app-assistant publish
   ```

3. **Install on robot:**
   - Go to http://reachy-mini:8000/
   - Click "Install from HuggingFace"
   - Search for your app

#### Required Files for HuggingFace

```
your-app/
├── index.html              # HF Space landing page
├── style.css               # HF Space styling
├── README.md               # With YAML frontmatter (see below)
├── pyproject.toml          # With entry point
└── your_app/
    ├── __init__.py
    ├── main.py             # ReachyMiniApp class
    └── static/             # App UI (optional)
```

**README.md frontmatter:**
```yaml
---
title: Your App Name
emoji: 📷
colorFrom: blue
colorTo: indigo
sdk: static
pinned: false
short_description: Your app description
tags:
  - reachy_mini
  - reachy_mini_python_app
---
```

**pyproject.toml entry point:**
```toml
[project.entry-points."reachy_mini_apps"]
your-app-name = "your_app.main:YourAppClass"
```

### Method 2: Direct SSH Install

For development and testing without publishing to HuggingFace.

#### Robot Filesystem Structure

```
/venvs/
├── apps_venv/          # Where apps are installed (MUST use Python 3.12)
│   ├── bin/
│   │   └── python -> uv's Python 3.12
│   ├── lib/
│   │   └── python3.12/site-packages/  # Apps go here
│   └── pyvenv.cfg      # CRITICAL: Must point to uv Python 3.12
├── mini_daemon/        # Daemon's venv (Python 3.12)
└── src/                # Source code
```

> **CRITICAL**: The daemon runs Python 3.12 and only looks for apps in `python3.12/site-packages/`. If apps_venv uses Python 3.13, your apps will install to the wrong location and the daemon won't find them!

#### Installation Steps

1. **SSH into the robot:**
   ```bash
   ssh pollen@reachy-mini
   # Password: root
   ```

2. **Verify Python version matches daemon:**
   ```bash
   /venvs/apps_venv/bin/python --version   # Must be 3.12.x
   /venvs/mini_daemon/bin/python --version  # Reference: 3.12.12
   ```

3. **If Python versions don't match, fix apps_venv:**
   ```bash
   # Fix symlinks to use uv's Python 3.12 (same as daemon)
   cd /venvs/apps_venv/bin/
   rm -f python python3 python3.12 python3.13
   ln -s /home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/bin/python3.12 python
   ln -s python python3
   ln -s python python3.12

   # Fix pyvenv.cfg (CRITICAL for standalone uv Python)
   echo 'home = /home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/bin' > /venvs/apps_venv/pyvenv.cfg
   echo 'implementation = CPython' >> /venvs/apps_venv/pyvenv.cfg
   echo 'version_info = 3.12.12' >> /venvs/apps_venv/pyvenv.cfg
   echo 'include-system-site-packages = false' >> /venvs/apps_venv/pyvenv.cfg

   # Verify
   /venvs/apps_venv/bin/python --version  # Should show 3.12.12
   ```

4. **Install app from GitHub:**
   ```bash
   /venvs/apps_venv/bin/python -m pip install "git+https://github.com/doneyli/reachy-mini-apps.git#subdirectory=camera-live-feed"
   ```

5. **Verify installation:**
   ```bash
   /venvs/apps_venv/bin/python -c "from importlib.metadata import entry_points; eps = entry_points(group='reachy_mini_apps'); print([ep.name for ep in eps])"
   ```

6. **Restart daemon:**
   ```bash
   sudo systemctl restart reachy-mini-daemon
   ```

7. **Refresh dashboard:**
   - Go to http://reachy-mini:8000/
   - App should appear in Applications section

#### Updating an App

```bash
./python -m pip install --upgrade "git+https://github.com/doneyli/reachy-mini-apps.git#subdirectory=camera-live-feed"
```

#### Uninstalling an App

```bash
./python -m pip uninstall camera-live-feed
```

## Troubleshooting

### Check Daemon Logs

```bash
# View recent logs
journalctl -u reachy-mini-daemon -n 50 --no-pager

# Follow logs in real-time
journalctl -u reachy-mini-daemon -f
```

### App Won't Start (Toggle Goes Back to OFF)

This usually means the app is crashing. Check logs for errors:
```bash
journalctl -u reachy-mini-daemon -f
# Then toggle the app ON in the dashboard
```

Common issues:
- Missing dependencies
- Import errors
- Python version incompatibility

### Restart Daemon

```bash
sudo systemctl restart reachy-mini-daemon
```

### Check App Entry Points

```bash
/venvs/apps_venv/bin/python -c "
from importlib.metadata import entry_points
eps = entry_points(group='reachy_mini_apps')
for ep in eps:
    print(f'{ep.name} = {ep.value}')
"
```

### Python Version Mismatch

**This is the #1 cause of "app won't start" issues!**

The robot has two Python versions:
- **System Python**: 3.13.5 (`/usr/bin/python3`)
- **Daemon Python**: 3.12.12 (uv standalone at `/home/pollen/.local/share/uv/python/`)

The daemon uses Python 3.12 and only finds apps in `python3.12/site-packages/`.

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for the full diagnosis and fix.

Your `pyproject.toml` should allow both versions:
```toml
requires-python = ">=3.10"
```

## Dashboard URLs

- **Robot dashboard:** http://reachy-mini:8000/
- **Local development:** http://localhost:8000/

## Resources

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed debugging guide for common issues
- [Make and Publish Reachy Mini Apps](https://huggingface.co/blog/pollen-robotics/make-and-publish-your-reachy-mini-apps)
- [Reachy Mini SDK](https://github.com/pollen-robotics/reachy_mini)
- [SDK Installation Guide](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/installation.md)
