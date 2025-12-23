"""Camera Capture Demo

Demonstrates capturing a frame from the robot's camera and saving it.
"""

import time
import cv2
from reachy_mini import ReachyMini

with ReachyMini(localhost_only=False) as mini:
    print("Connected to Reachy Mini!")

    # Give the camera time to initialize
    print("Waiting for camera to initialize...")
    time.sleep(1.0)

    # Try to capture a frame with retries
    print("Capturing frame...")
    frame = None
    for attempt in range(5):
        frame = mini.media.get_frame()
        if frame is not None:
            break
        print(f"  Attempt {attempt + 1}/5 - waiting...")
        time.sleep(0.5)

    if frame is not None:
        # Save the frame
        filename = "captured_frame.jpg"
        cv2.imwrite(filename, frame)
        print(f"Frame saved to {filename}")
        print(f"Frame size: {frame.shape[1]}x{frame.shape[0]}")

        # Display the frame (press any key to close, or wait 10 seconds)
        print("Displaying frame (press any key to close, auto-closes in 10s)...")
        cv2.imshow("Reachy Mini Camera", frame)
        cv2.waitKey(10000)  # 10 second timeout
        cv2.destroyAllWindows()
        cv2.waitKey(1)  # Flush any remaining events
    else:
        print("Failed to capture frame after 5 attempts")
        print("Make sure the robot's camera is connected and working")

print("Done!")
