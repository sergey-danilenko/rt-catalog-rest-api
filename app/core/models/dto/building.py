from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .organization import Organization


class Building(BaseModel):
    id: int

    city: str
    street: str
    house: str

    lat: float
    lon: float
    create_date: datetime

    country: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    block: Optional[str] = None
    name: Optional[str] = None

    organizations: Optional[list["Organization"]] = None

    @property
    def full_address(self) -> str:
        address = f"г. {self.city}, ул. {self.street}, д. {self.house}"

        if self.block:
            address = f"{address}/{self.block}"
        if self.region:
            address = f"{self.region}, {address}"
        if self.postal_code:
            address = f"{self.postal_code}, {address}"
        if self.country:
            address = f"{self.country}, {address}"
        return address
