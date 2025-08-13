from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

if TYPE_CHECKING:
    from .activity import Activity
    from .building import Building
    from .phone import PhoneNumber


@dataclass
class OrgCreate:
    name: str
    inn: str
    building_id: int | None = None
    office: str | None = None
    phones: list[str] | None = None
    activities: list[int] | None = None


class Organization(BaseModel):
    id: int
    name: str
    inn: str
    create_date: Optional[datetime] = None

    building_id: Optional[int] = None
    office: Optional[str] = None

    phones: Optional[list["PhoneNumber"]] = None
    activities: Optional[list["Activity"]] = None
    building: Optional["Building"] = None
