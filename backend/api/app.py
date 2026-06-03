from fastapi import FastAPI
import json
import os
from collections import Counter

app = FastAPI(title="Store Intelligence API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EVENT_FILE = os.path.join(
    BASE_DIR,
    "..",
    "events.jsonl"
)


def load_events():

    events = []

    try:

        with open(EVENT_FILE, "r") as f:

            for line in f:
                events.append(json.loads(line))

    except FileNotFoundError:
        pass

    return events


@app.get("/")
def home():

    return {
        "message": "Store Intelligence API Running"
    }


@app.get("/events")
def get_events():

    return load_events()


@app.get("/analytics/footfall")
def footfall():

    events = load_events()

    count = sum(
        1
        for e in events
        if e.get("event_type") == "entry"
    )

    return {
        "footfall": count
    }


@app.get("/analytics/zones")
def zone_analytics():

    events = load_events()

    zones = Counter()

    for e in events:

        if e.get("event_type") == "zone_entered":

            zones[e["zone"]] += 1

    return dict(zones)


@app.get("/alerts")
def alerts():

    events = load_events()

    return [
        e
        for e in events
        if e.get("event_type") == "queue_alert"
    ]