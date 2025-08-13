from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.util import object_state

from app.core.models import dto

from .base import Base, str_50, UTC_datetime
from .organization import Organization
from .org_activity import OrgActivity


class Activity(Base):
    __tablename__ = 'activities'
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        Index("ix_activities_name", "name"),
        Index('ix_activities_parent_id', 'parent_id'),
        Index('ix_activities_name_parent', 'name', 'parent_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str_50] = mapped_column(unique=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="SET NULL"),
        default=None,
    )
    create_date: Mapped[UTC_datetime]

    organizations: Mapped[list["Organization"]] = relationship(
        secondary=OrgActivity.__table__,
        back_populates="activities",
        viewonly=True,
    )
    org_activities = relationship(
        "OrgActivity",
        foreign_keys="OrgActivity.activity_id",
        cascade="all, delete-orphan",
    )

    parent: Mapped[Optional["Activity"]] = relationship(
        back_populates="children",
        remote_side=[id],
    )
    children: Mapped[list["Activity"]] = relationship(
        back_populates="parent",
    )

    def __repr__(self):
        return self.name

    def to_dto(self) -> dto.Activity:
        state = object_state(self)
        return dto.Activity(
            id=self.id,
            name=self.name,
            create_date=self.create_date,
            parent_id=self.parent_id,
            parent=self.parent.to_dto() if "parent" in state.dict else None,
            children=[
                c.to_dto() for c in self.children
            ] if "children" in state.dict else None
        )
