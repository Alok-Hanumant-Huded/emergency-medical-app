def build_google_maps_link(latitude, longitude):
    if latitude is None or longitude is None:
        return "Location not available"
    return f"https://www.google.com/maps?q={latitude},{longitude}"


def create_location_payload(latitude, longitude):
    return {
        "latitude": latitude,
        "longitude": longitude,
        "map_link": build_google_maps_link(latitude, longitude),
    }
