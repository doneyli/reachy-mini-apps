"""Body Rotation Demo

Demonstrates rotating the robot's body (yaw axis).
Body yaw range: -160 to +160 degrees.
"""

import numpy as np
from reachy_mini import ReachyMini

with ReachyMini(localhost_only=False) as mini:
    print("Connected to Reachy Mini!")

    # Rotate body left (positive yaw)
    print("Rotating body left...")
    mini.goto_target(body_yaw=np.deg2rad(45), duration=1.5)

    # Rotate body right (negative yaw)
    print("Rotating body right...")
    mini.goto_target(body_yaw=np.deg2rad(-45), duration=1.5)

    # Return to center
    print("Returning to center...")
    mini.goto_target(body_yaw=np.deg2rad(0), duration=1.0)

    print("Done!")
