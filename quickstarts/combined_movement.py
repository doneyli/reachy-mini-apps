"""Combined Movement Demo

Demonstrates controlling head, body, and antennas simultaneously.
Shows different interpolation methods: linear, minjerk, ease, cartoon.
"""

import numpy as np
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

with ReachyMini(localhost_only=False) as mini:
    print("Connected to Reachy Mini!")

    # Combined movement with minjerk (smooth acceleration/deceleration)
    print("Combined movement (minjerk interpolation)...")
    mini.goto_target(
        head=create_head_pose(z=10, mm=True),
        antennas=np.deg2rad([30, 30]),
        body_yaw=np.deg2rad(20),
        duration=2.0,
        method="minjerk"
    )

    # Different interpolation: cartoon (exaggerated, playful motion)
    print("Cartoon-style movement...")
    mini.goto_target(
        head=create_head_pose(z=-10, mm=True),
        antennas=np.deg2rad([-30, -30]),
        body_yaw=np.deg2rad(-20),
        duration=1.5,
        method="cartoon"
    )

    # Linear interpolation (constant speed)
    print("Linear movement...")
    mini.goto_target(
        head=create_head_pose(y=15, mm=True),
        antennas=np.deg2rad([45, -45]),
        body_yaw=np.deg2rad(0),
        duration=1.0,
        method="linear"
    )

    # Return to neutral position
    print("Returning to neutral...")
    mini.goto_target(
        head=create_head_pose(x=0, y=0, z=0, mm=True),
        antennas=[0, 0],
        body_yaw=0,
        duration=1.5,
        method="ease"
    )

    print("Done!")
