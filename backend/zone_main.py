import cv2

import services.detector as detector
import services.tracker as tracker_service

from services.zones import get_zone
from services.zone_event_generator import generate_zone_event
from services.event_logger import save_event

video_path = "../videos/zone.mp4"

cap = cv2.VideoCapture(video_path)

while True:

    success, frame = cap.read()

    if not success:
        break

    detections = detector.detect(frame)

    tracked = tracker_service.update_tracks(
        detections
    )

    for bbox, track_id in zip(
        tracked.xyxy,
        tracked.tracker_id
    ):

        if track_id is None:
            continue

        x1, y1, x2, y2 = map(int, bbox)

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        zone = get_zone(cx, cy)
        if zone is None:
          continue

        event = generate_zone_event(
            track_id,
            zone
        )

        if event:
            print(event)
            save_event(event)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"{track_id} | {zone}",
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            2
        )

    cv2.imshow("Zone Analytics", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()