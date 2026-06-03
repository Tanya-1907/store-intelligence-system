from datetime import datetime

track_zone_map = {}

def generate_zone_event(track_id, current_zone):

    if current_zone is None:
        return None

    previous_zone = track_zone_map.get(track_id)

    if previous_zone != current_zone:

        track_zone_map[track_id] = current_zone

        return {
            "event_type": "zone_entered",
            "track_id": int(track_id),
            "zone": current_zone,
            "timestamp": datetime.now().isoformat()
        }

    return None