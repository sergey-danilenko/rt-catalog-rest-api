from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.base import object_state

from app.core.models import dto

from .base import Base, str_10, str_100, UTC_datetime
from .org_activity import OrgActivity

if TYPE_CHECKING:
    from .activity import Activity
    from .building import Building
    from .phone import PhoneNumber


class Organization(Base):
    __tablename__ = 'organizations'
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        Index('ix_organizations_name', 'name'),
        Index('ix_organizations_building_id', 'building_id'),
        Index(
            'ix_organizations_building_office',
            'building_id',
            'office',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str_100]
    inn: Mapped[str_10] = mapped_column(unique=True)

    building_id: Mapped[int | None] = mapped_column(
        ForeignKey('buildings.id'),
        default=None,
    )

    office: Mapped[str_10 | None] = mapped_column(default=None)
    create_date: Mapped[UTC_datetime]

    phones: Mapped[list[PhoneNumber]] = relationship(
        foreign_keys='PhoneNumber.organization_id',
        back_populates='organization',
        cascade="all, delete-orphan",
    )
    building: Mapped[Building] = relationship(
        foreign_keys=building_id,
        back_populates='organizations',
    )

    activities: Mapped[list["Activity"]] = relationship(
        secondary=OrgActivity.__table__,
        back_populates="organizations",
        viewonly=True,
    )
    org_activities = relationship(
        "OrgActivity",
        foreign_keys="OrgActivity.organization_id",
        cascade="all, delete-orphan",
    )

    def to_dto(self) -> dto.Organization:
        state = object_state(self)
        return dto.Organization(
            id=self.id,
            name=self.name,
            inn=self.inn,
            create_date=self.create_date,
            building_id=self.building_id,
            office=self.office,
            phones=[p.to_dto() for p in self.phones] if "phones" in state.dict else None,
            activities=[c.to_dto() for c in self.activities] if "activities" in state.dict else None,
            building=self.building.to_dto() if "building" in state.dict else None,
        )
