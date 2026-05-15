from typing import Self

from pydantic import EmailStr, Field

from dddesign.components.domains.value_objects import AutoUUID
from dddesign.structure.domains.entities import Entity


class UserId(AutoUUID):
    ...


class User(Entity):
    user_id: UserId = Field(default_factory=UserId)
    email: EmailStr
    password_hash: str

    @classmethod
    def factory(cls, email: EmailStr, password_hash: str) -> Self:
        return cls(email=email, password_hash=password_hash)
