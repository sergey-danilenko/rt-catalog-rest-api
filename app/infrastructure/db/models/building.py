from __future__ import annotations

from sqlalchemy import Index, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import dto
from .base import Base, str_10, str_50, str_100, str_150, UTC_datetime
from .organization import Organization


class Building(Base):
    __tablename__ = 'buildings'
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        UniqueConstraint('city', 'street', 'house'),
        Index("ix_buildings_geo_lat_lon", "lat", "lon"),
        Index("ix_buildings_city_postal", "city", "postal_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    country: Mapped[str_100 | None] = mapped_column(default=None)
    region: Mapped[str_150 | None] = mapped_column(default=None)
    city: Mapped[str_100]
    street: Mapped[str_150]
    house: Mapped[str_10]
    postal_code: Mapped[str_10 | None] = mapped_column(default=None)
    block: Mapped[str_10 | None] = mapped_column(default=None)

    lat: Mapped[float]
    lon: Mapped[float]
    name: Mapped[str_50 | None] = mapped_column(default=None)
    create_date: Mapped[UTC_datetime]

    organizations: Mapped[list[Organization]] = relationship(
        back_populates='building',
    )

    def to_dto(self) -> dto.Building:
        return dto.Building(
            id=self.id,
            city=self.city,
            street=self.street,
            house=self.house,
            lat=self.lat,
            lon=self.lon,
            create_date=self.create_date,
            country=self.country,
            region=self.region,
            postal_code=self.postal_code,
            name=self.name,
        )
