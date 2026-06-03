from datetime import datetime

seen_tracks = set()

def generate_entry_event(track_id):

    if track_id not in seen_tracks:

        seen_tracks.add(track_id)

        return {
            "event_type": "entry",
            "track_id": int(track_id),
            "timestamp": datetime.now().isoformat()
        }

    return None