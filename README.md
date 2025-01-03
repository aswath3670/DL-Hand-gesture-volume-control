Hand Gesture Volume Control
This project demonstrates a system that allows users to control their device's volume using hand gestures. By importing predefined Python modules and leveraging a hand tracking file, the system detects hand gestures in real time and maps them to volume control.


A demonstration of the hand gesture used to control volume.

How It Works
Hand Detection:
The system uses a pre-trained hand tracking module (based on Mediapipe) to detect and track hand landmarks in a live video feed.

Gesture Recognition:

The distance between the thumb and index finger is calculated.
This distance is mapped to a range of volume levels (e.g., 0% to 100%).
Volume Control:
The recognized gesture dynamically adjusts the system's volume through OS-specific APIs.

Project Structure
hand_tracking.py:
Contains the implementation for hand tracking using Mediapipe.

volume_control.py:
Main script to run the volume control system. This script imports the hand tracking module, processes the video feed, and maps gestures to volume levels.

assets/sample_gesture.png:
Sample image showing the gesture used to control volume.
