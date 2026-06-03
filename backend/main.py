import cv2

import services.detector as detector
import services.tracker as tracker_service

from services.event_generator import generate_entry_event
from services.event_logger import save_event
print("Imports OK")

# Video path
video_path = "../videos/entry_1.mp4"

# Open video
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video: {video_path}")
    exit()

print("Video Started...")

while True:

    success, frame = cap.read()

    if not success:
        print("Video Finished")
        break

    # Detection
    detections = detector.detect(frame)

    # Tracking
    tracked = tracker_service.update_tracks(detections)

    active_tracks = 0

    # Draw tracks
    for bbox, track_id in zip(
        tracked.xyxy,
        tracked.tracker_id
    ):

        if track_id is None:
            continue

        active_tracks += 1

        # Generate entry event
        event = generate_entry_event(track_id)

        if event:
            print(event)
            save_event(event)

        x1, y1, x2, y2 = map(int, bbox)

        # Bounding Box
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # Track ID
        cv2.putText(
            frame,
            f"ID {track_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # People Count
    cv2.putText(
        frame,
        f"People: {active_tracks}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    # Display Video
    cv2.imshow(
        "Store Intelligence - Entry Tracking",
        frame
    )

    key = cv2.waitKey(1)

    # ESC key
    if key == 27:
        print("Stopped by User")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

print("Processing Complete")