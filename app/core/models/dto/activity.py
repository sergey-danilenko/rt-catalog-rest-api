from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .organization import Organization


class Activity(BaseModel):
    id: int
    name: str
    create_date: datetime
    parent_id: Optional[int] = None

    organizations: Optional[list["Organization"]] = None
    parent: Optional["Activity"] = None
    children: Optional[list["Activity"]] = None

    @property
    def has_parent(self) -> bool:
        return self.parent_id is not None
