"""Head Movement Demo

Demonstrates controlling the robot's head position using create_head_pose.
The head can move in x, y, z coordinates relative to its base.
"""

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

with ReachyMini(localhost_only=False) as mini:
    print("Connected to Reachy Mini!")

    # Look up (positive z)
    print("Looking up...")
    mini.goto_target(head=create_head_pose(z=15, mm=True), duration=1.0)

    # Look down (negative z)
    print("Looking down...")
    mini.goto_target(head=create_head_pose(z=-15, mm=True), duration=1.0)

    # Look left (positive y)
    print("Looking left...")
    mini.goto_target(head=create_head_pose(y=15, mm=True), duration=1.0)

    # Look right (negative y)
    print("Looking right...")
    mini.goto_target(head=create_head_pose(y=-15, mm=True), duration=1.0)

    # Return to center
    print("Returning to center...")
    mini.goto_target(head=create_head_pose(x=0, y=0, z=0, mm=True), duration=1.0)

    print("Done!")
