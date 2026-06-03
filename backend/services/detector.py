from ultralytics import YOLO
import supervision as sv

model = YOLO("yolov8n.pt")

def detect(frame):

    results = model(frame, verbose=False)[0]

    detections = sv.Detections.from_ultralytics(results)

    return detections