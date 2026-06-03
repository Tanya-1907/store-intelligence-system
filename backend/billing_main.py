import cv2

import services.detector as detector
import services.tracker as tracker_service

from services.event_logger import save_event
from datetime import datetime

# Prevent duplicate billing events
billing_tracks = set()

video_path = "../videos/billing_area.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Could not open billing video")
    exit()

print("Billing Analytics Started")

while True:

    success, frame = cap.read()

    if not success:
        break

    detections = detector.detect(frame)

    tracked = tracker_service.update_tracks(
        detections
    )

    active_people = 0

    for bbox, track_id in zip(
        tracked.xyxy,
        tracked.tracker_id
    ):

        if track_id is None:
            continue

        active_people += 1

        x1, y1, x2, y2 = map(int, bbox)

        # Generate billing entered event once
        if track_id not in billing_tracks:

            billing_tracks.add(track_id)

            event = {
                "event_type": "billing_entered",
                "track_id": int(track_id),
                "timestamp": datetime.now().isoformat()
            }

            print(event)

            save_event(event)

        # Draw box
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            f"ID {track_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            2
        )

    # Queue Alert
    if active_people >= 5:

        alert = {
            "event_type": "queue_alert",
            "queue_size": active_people,
            "timestamp": datetime.now().isoformat()
        }

        print(alert)

        save_event(alert)

        cv2.putText(
            frame,
            "QUEUE ALERT",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    cv2.putText(
        frame,
        f"Queue Size: {active_people}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.imshow(
        "Billing Analytics",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("Billing Analytics Finished")