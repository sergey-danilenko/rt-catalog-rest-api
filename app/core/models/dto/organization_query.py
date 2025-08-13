from dataclasses import dataclass


@dataclass
class AddressFilter:
    city: str | None = None
    street: str | None = None
    house: str | None = None
    office: str | None = None


@dataclass
class GeoRadiusQuery:
    center_lat: float
    center_lon: float
    radius: float


@dataclass
class GeoRectQuery:
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float


@dataclass
class OrgActivityQuery:
    activity_name: str
    depth: int = 3
