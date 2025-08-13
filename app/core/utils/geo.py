from math import cos, radians

EARTH_RADIUS_KM = 6371.0


def bounding_box(lat, lon, radius_km):
    lat_deg = radius_km / 111.32
    lon_deg = radius_km / (111.32 * cos(radians(lat)))
    return (
        lat - lat_deg,
        lon - lon_deg,
        lat + lat_deg,
        lon + lon_deg,
    )
