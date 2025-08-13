import re

from sqlalchemy import ForeignKey, TypeDecorator, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.base import object_state

from app.core.models import dto
from app.core.utils.phone import format_phone_num
from .base import Base, str_30
from .organization import Organization


class PhoneNumCleaner(TypeDecorator):
    impl = String(30)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value:
            return re.sub(r'[^\d]', '', value)


class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str_30] = mapped_column(PhoneNumCleaner, unique=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),

    )

    organization: Mapped[Organization] = relationship(
        foreign_keys=organization_id,
        back_populates="phones",
    )

    def to_dto(
        self,
        organization: list[dto.Organization] | None = None
    ) -> dto.PhoneNumber:
        return dto.PhoneNumber(
            id=self.id,
            number=format_phone_num(self.number),
            organization_id=self.organization_id,
            organization=organization
        )

    def to_full_dto(self) -> dto.PhoneNumber:
        state = object_state(self)
        organization = self.organization.to_dto() if "organization" in state.dict else None
        return self.to_dto(organization)
