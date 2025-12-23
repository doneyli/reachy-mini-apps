Act as a Senior Python Architect and Robotics Engineer.

I am initializing a new GitHub repository called reachy-mini-apps for the Reachy Mini robot (using the official reachy-mini SDK v1.2+).

Repository Strategy:

Monorepo: I want to use a uv workspace structure. This allows me to have a root pyproject.toml for shared dev dependencies and individual pyproject.toml files for each app.

Hardware: The apps will run on a computer connected to the robot (Reachy Mini Lite mode) or directly on the robot.

Immediate Task: Generate the file structure and code for:

Root Configuration: A root pyproject.toml defining the workspace members.

Shared Library (packages/shared): A folder for common code (ClickHouse client, Robot connection wrappers).

First App (apps/camera-live-feed): A script that connects to the robot and streams video using cv2 and mini.media.get_frame().

Specific Requirements:

Dependencies:

Root/Shared: reachy-mini, clickhouse-connect, numpy.

Camera App: opencv-python.

Code Pattern: Use the context manager syntax (with ReachyMini() as mini:) which is the official best practice.

Error Handling: In the camera app, handle the case where the robot is not connected gracefully.

README: A root README.md explaining how to run uv run apps/camera-live-feed/main.py.

Please output the full directory tree first, then the content for the key configuration and source files.