# Quickstarts

Simple example scripts to get started with Reachy Mini. Based on the [official Python SDK documentation](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/python-sdk.md).

## Prerequisites

Make sure you've completed the [main setup](../README.md#installation) and the Reachy Mini daemon is running.

## Available Examples

### Wiggle Antennas

A simple connection test that moves the robot's antennas.

```bash
uv run python quickstarts/wiggle_antennas.py
```

**What it demonstrates:**
- Basic connection to the robot
- Antenna position control with `goto_target(antennas=[...])`

---

### Head Movement

Control the robot's head position in 3D space.

```bash
uv run python quickstarts/head_movement.py
```

**What it demonstrates:**
- Using `create_head_pose(x, y, z, mm=True)` for head positioning
- Looking up, down, left, and right
- Head movement limits: pitch/roll ±40°, yaw ±180°

---

### Body Rotation

Rotate the robot's body on the yaw axis.

```bash
uv run python quickstarts/body_rotation.py
```

**What it demonstrates:**
- Body yaw control with `goto_target(body_yaw=...)`
- Using `np.deg2rad()` for angle conversion
- Body rotation limits: ±160°

---

### Camera Capture

Capture and save a frame from the robot's camera.

```bash
uv run python quickstarts/camera_capture.py
```

**What it demonstrates:**
- Accessing the camera with `mini.media.get_frame()`
- Saving frames with OpenCV
- Displaying captured images

---

### Combined Movement

Control head, body, and antennas simultaneously with different interpolation styles.

```bash
uv run python quickstarts/combined_movement.py
```

**What it demonstrates:**
- Simultaneous control of multiple joints
- Interpolation methods: `linear`, `minjerk`, `ease`, `cartoon`
- Smooth, coordinated robot movements

---

### Camera Dashboard

Stream live video from the robot's camera to a web dashboard.

```bash
uv run python quickstarts/camera_dashboard.py
```

Then open http://localhost:8080 in your browser. Press `Ctrl+C` to stop.

**What it demonstrates:**
- Live MJPEG video streaming
- FastAPI web server setup
- Multi-threaded frame capture
- Web dashboard with styled UI

---

## API Reference

### Movement Methods

| Method | Description |
|--------|-------------|
| `goto_target(...)` | Smooth interpolation to target position |
| `set_target(...)` | Instant position update (for high-frequency control) |

### goto_target Parameters

```python
mini.goto_target(
    head=create_head_pose(x, y, z, mm=True),  # Head position
    antennas=[left, right],                    # Antenna angles (radians)
    body_yaw=angle,                            # Body rotation (radians)
    duration=2.0,                              # Movement duration (seconds)
    method="minjerk"                           # Interpolation method
)
```

### Interpolation Methods

| Method | Description |
|--------|-------------|
| `linear` | Constant speed movement |
| `minjerk` | Smooth acceleration/deceleration (default) |
| `ease` | Gentle easing motion |
| `cartoon` | Exaggerated, playful motion |

### Movement Limits

| Component | Range |
|-----------|-------|
| Head Pitch/Roll | -40° to +40° |
| Head Yaw | -180° to +180° |
| Body Yaw | -160° to +160° |
| Head-Body Yaw Difference | Maximum 65° |

### Motor Control

```python
mini.enable_motors()              # Stiff mode - maintains position
mini.disable_motors()             # Limp mode - unpowered
mini.enable_gravity_compensation() # Allows manual repositioning
```

### Media Operations

```python
# Camera
frame = mini.media.get_frame()

# Audio
sample = mini.media.get_audio_sample()
mini.media.play_sound("sound.wav")
```

## Connection Modes

**Wireless (Reachy Mini Lite):**
```python
with ReachyMini(localhost_only=False) as mini:
```

**Local (running on robot):**
```python
with ReachyMini() as mini:
```

## Official Documentation

- [SDK Quickstart Guide](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/quickstart.md)
- [Python SDK Reference](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/python-sdk.md)
- [Core Concepts](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/core-concept.md)
- [SDK Installation](https://github.com/pollen-robotics/reachy_mini/blob/develop/docs/SDK/installation.md)
