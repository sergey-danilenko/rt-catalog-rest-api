from typing import Optional

from pydantic import BaseModel

from .organization import Organization


class PhoneNumber(BaseModel):
    id: int
    number: str
    organization_id: int
    organization: Optional["Organization"] = None
