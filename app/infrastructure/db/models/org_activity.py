from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class OrgActivity(Base):
    __tablename__ = 'org_activity'
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        PrimaryKeyConstraint("organization_id", "activity_id"),
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
    )
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"),
    )
