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
├── apps_venv/          # Where apps are installed
│   ├── bin/
│   │   ├── python -> /usr/bin/python3
│   │   └── pip
│   └── lib/
├── mini_daemon/        # Daemon's venv
└── src/                # Source code
```

#### Installation Steps

1. **SSH into the robot:**
   ```bash
   ssh pollen@reachy-mini
   # Password: root
   ```

2. **Fix Python symlinks if broken:**
   ```bash
   cd /venvs/apps_venv/bin/
   rm -f python python3 python3.12 python3.13
   ln -s /usr/bin/python3 python
   ln -s /usr/bin/python3 python3
   ln -s /usr/bin/python3 python3.13
   ```

3. **Reinstall pip if needed:**
   ```bash
   ./python -m ensurepip --upgrade
   ```

4. **Install app from GitHub:**
   ```bash
   ./python -m pip install "git+https://github.com/doneyli/reachy-mini-apps.git#subdirectory=camera-live-feed"
   ```

5. **Verify installation:**
   ```bash
   ./python -c "from importlib.metadata import entry_points; eps = entry_points(group='reachy_mini_apps'); print([ep.name for ep in eps])"
   ```

6. **Refresh dashboard:**
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

### Python Version

The robot runs **Python 3.13.5**. Ensure your `pyproject.toml` allows it:
```toml
requires-python = ">=3.10"
```

## Dashboard URLs

- **Robot dashboard:** http://reachy-mini:8000/
- **Local development:** http://localhost:8000/

## Resources

- [Make and Publish Reachy Mini Apps](https://huggingface.co/blog/pollen-robotics/make-and-publish-your-reachy-mini-apps)
- [Reachy Mini SDK](https://github.com/pollen-robotics/reachy_mini)
- [SDK Installation Guide](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/installation.md)
