import cv2
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTrackingModule as htm

# Constants for the camera dimensions
CAM_WIDTH, CAM_HEIGHT = 640, 480

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)
prev_time = 0

# Initialize hand detector with a higher detection confidence
detector = htm.handDetector(detectionCon=0.75)

# Set up audio controls
audio_devices = AudioUtilities.GetSpeakers()
audio_interface = audio_devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_control = cast(audio_interface, POINTER(IAudioEndpointVolume))
vol_range = volume_control.GetVolumeRange()
min_vol, max_vol = vol_range[0], vol_range[1]

# Variables for volume control
current_vol = 0
vol_bar_height = 400
vol_percent = 0

while True:
    # Capture frame from webcam
    success, frame = cap.read()
    if not success:
        break

    # Detect hands in the frame
    frame = detector.findHands(frame)
    landmarks = detector.findPosition(frame, draw=False)

    if landmarks:
        # Get positions of thumb and index finger
        thumb_x, thumb_y = landmarks[4][1], landmarks[4][2]
        index_x, index_y = landmarks[8][1], landmarks[8][2]
        center_x, center_y = (thumb_x + index_x) // 2, (thumb_y + index_y) // 2

        # Draw interactive elements
        cv2.circle(frame, (thumb_x, thumb_y), 12, (0, 0, 255), cv2.FILLED)
        cv2.circle(frame, (index_x, index_y), 12, (0, 255, 0), cv2.FILLED)
        cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 255, 0), 2)
        cv2.circle(frame, (center_x, center_y), 10, (255, 255, 255), cv2.FILLED)

        # Calculate distance between thumb and index finger
        distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

        # Map the distance to volume range
        current_vol = np.interp(distance, [30, 300], [min_vol, max_vol])
        vol_bar_height = np.interp(distance, [30, 300], [400, 150])
        vol_percent = np.interp(distance, [30, 300], [0, 100])

        # Apply volume changes
        volume_control.SetMasterVolumeLevel(current_vol, None)

        # Visual feedback for minimal distance
        if distance < 30:
            cv2.circle(frame, (center_x, center_y), 15, (0, 255, 255), cv2.FILLED)

    # Draw gradient volume bar
    for i in range(150, 401, 10):
        color = (int(255 - (i - 150) / 2), int((i - 150) / 2), 255)
        cv2.rectangle(frame, (50, i), (85, i + 10), color, cv2.FILLED)

    cv2.rectangle(frame, (50, int(vol_bar_height)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, f'{int(vol_percent)}%', (40, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Display frame rate
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f'FPS: {int(fps)}', (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show the output frame
    cv2.imshow("Hand Volume Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
