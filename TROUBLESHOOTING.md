# Troubleshooting Guide

Hard-won lessons from deploying Reachy Mini apps to the robot.

## The Python Version Mismatch Problem

### Symptoms
- App appears in the dashboard but toggle immediately goes back to OFF
- Daemon logs show: `ValueError: No entry point found for app 'your-app-name'`
- Entry point IS registered when you check manually

### Root Cause

The Reachy Mini Wireless has **two separate Python environments**:

| Environment | Path | Python Version | Purpose |
|-------------|------|----------------|---------|
| mini_daemon | `/venvs/mini_daemon/` | Python 3.12 (uv) | Runs the daemon |
| apps_venv | `/venvs/apps_venv/` | Must match daemon | Installed apps |

The daemon runs Python 3.12 from uv's standalone installation:
```
/home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/bin/python3.12
```

When apps are installed with a different Python version (e.g., system Python 3.13), they go to a different site-packages directory:
- Python 3.12 packages: `/venvs/apps_venv/lib/python3.12/site-packages/`
- Python 3.13 packages: `/venvs/apps_venv/lib/python3.13/site-packages/`

**The daemon only looks in `python3.12/site-packages/`!**

### Diagnosis

SSH into the robot and check:

```bash
# What Python is apps_venv using?
/venvs/apps_venv/bin/python --version

# What Python is mini_daemon using?
/venvs/mini_daemon/bin/python --version

# These MUST match! If apps_venv shows 3.13 and mini_daemon shows 3.12, that's the problem.

# Check which site-packages directories exist
ls /venvs/apps_venv/lib/

# Check where your app is installed
ls /venvs/apps_venv/lib/python3.12/site-packages/ | grep your-app
ls /venvs/apps_venv/lib/python3.13/site-packages/ | grep your-app
```

### The Fix

#### Step 1: Fix the Python symlinks in apps_venv

```bash
cd /venvs/apps_venv/bin/
rm -f python python3 python3.12 python3.13
ln -s /home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/bin/python3.12 python
ln -s python python3
ln -s python python3.12
```

#### Step 2: Fix pyvenv.cfg

The `pyvenv.cfg` file tells Python where to find its standard library. It MUST point to the uv Python installation:

```bash
# Check current config
cat /venvs/apps_venv/pyvenv.cfg

# If it shows Python 3.13 or /usr/bin, it's wrong. Fix it:
echo 'home = /home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/bin' > /venvs/apps_venv/pyvenv.cfg
echo 'implementation = CPython' >> /venvs/apps_venv/pyvenv.cfg
echo 'version_info = 3.12.12' >> /venvs/apps_venv/pyvenv.cfg
echo 'include-system-site-packages = false' >> /venvs/apps_venv/pyvenv.cfg
```

#### Step 3: Verify Python works

```bash
/venvs/apps_venv/bin/python --version
# Should output: Python 3.12.12
```

If you see errors like `ModuleNotFoundError: No module named 'encodings'`, the pyvenv.cfg is still wrong.

#### Step 4: Reinstall your app

```bash
/venvs/apps_venv/bin/python -m pip install --upgrade "git+https://github.com/YOUR_USER/YOUR_REPO.git#subdirectory=your-app"
```

#### Step 5: Verify entry point

```bash
/venvs/apps_venv/bin/python -c "from importlib.metadata import entry_points; eps = entry_points(group='reachy_mini_apps'); print([ep.name for ep in eps])"
```

#### Step 6: Restart daemon and test

```bash
sudo systemctl restart reachy-mini-daemon
```

Then toggle your app ON in the dashboard.

---

## Understanding the uv Standalone Python

Reachy Mini uses [uv](https://github.com/astral-sh/uv) to manage Python installations. The uv-installed Python is a standalone build located at:

```
/home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/
```

This standalone Python:
- Has its own standard library
- Requires a proper `pyvenv.cfg` when used in a venv
- Cannot be symlinked directly without the venv configuration

### Why pyvenv.cfg Matters

When you create a virtual environment, Python needs to know where to find:
1. The Python executable
2. The standard library (stdlib)
3. The site-packages directory

The `pyvenv.cfg` file in the venv root provides this information. The `home` key tells Python where the base installation is, and Python finds the stdlib relative to that.

**Wrong pyvenv.cfg:**
```
home = /usr/bin
version = 3.13.5
```

**Correct pyvenv.cfg:**
```
home = /home/pollen/.local/share/uv/python/cpython-3.12.12-linux-aarch64-gnu/bin
implementation = CPython
version_info = 3.12.12
include-system-site-packages = false
```

---

## HuggingFace Spaces Publishing Gotchas

### Required Files

Your app MUST have these files in the root (not in a subdirectory):

```
your-app/
├── index.html          # HF Space landing page (required!)
├── style.css           # HF Space styling (required!)
├── README.md           # With YAML frontmatter (required!)
├── pyproject.toml      # With entry point
└── your_app/
    ├── __init__.py
    └── main.py
```

### README.md Frontmatter

Must include these exact fields:

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

**Valid colorFrom/colorTo values:** red, yellow, green, blue, indigo, purple, pink, gray

`cyan` is NOT valid and will cause publishing to fail!

### Entry Point Name

Use **hyphens**, not underscores:

```toml
# Correct
[project.entry-points."reachy_mini_apps"]
camera-live-feed = "camera_live_feed.main:CameraLiveFeed"

# Wrong - won't be discovered
[project.entry-points."reachy_mini_apps"]
camera_live_feed = "camera_live_feed.main:CameraLiveFeed"
```

### Python Version Constraint

The robot runs Python 3.13.5, so don't restrict to older versions:

```toml
# Correct
requires-python = ">=3.10"

# Wrong - will fail on robot
requires-python = ">=3.10,<3.13"
```

---

## Useful Debug Commands

### View Daemon Logs

```bash
# Recent logs
journalctl -u reachy-mini-daemon -n 50 --no-pager

# Follow logs in real-time (while toggling app)
journalctl -u reachy-mini-daemon -f
```

### Check Installed Apps

```bash
/venvs/apps_venv/bin/python -c "
from importlib.metadata import entry_points
eps = entry_points(group='reachy_mini_apps')
for ep in eps:
    print(f'{ep.name} = {ep.value}')
"
```

### Check Package Installation

```bash
/venvs/apps_venv/bin/python -m pip list | grep your-app
/venvs/apps_venv/bin/python -m pip show your-app
```

### Restart Services

```bash
sudo systemctl restart reachy-mini-daemon
```

---

## Quick Reference: SSH Credentials

- **Host:** `reachy-mini` (or IP on local network)
- **Username:** `pollen`
- **Password:** `root`

```bash
ssh pollen@reachy-mini
```

---

## Summary: The Critical Points

1. **Python versions must match**: apps_venv MUST use the same Python 3.12 as mini_daemon
2. **pyvenv.cfg must be correct**: Points to uv's Python installation, not system Python
3. **Entry points are version-specific**: Packages install to `pythonX.Y/site-packages/`
4. **Use hyphens in entry point names**: `my-app` not `my_app`
5. **HF Spaces needs index.html**: Landing page is required for publishing
6. **Valid colorTo values**: Only specific color names work in frontmatter
