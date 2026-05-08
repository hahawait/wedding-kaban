from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class GuestCreate(BaseModel):
    name: str
    email: str
    wish: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("ФИО не может быть пустым")
        return v

    @field_validator("email")
    @classmethod
    def email_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v or "@" not in v:
            raise ValueError("Некорректный email")
        return v.lower()


class GuestOut(BaseModel):
    id: int
    name: str
    email: str
    wish: Optional[str]
    registered_at: datetime

    model_config = {"from_attributes": True}
