import json

def save_event(event):

    with open("events.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")