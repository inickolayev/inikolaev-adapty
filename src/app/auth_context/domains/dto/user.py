from uuid import UUID

from pydantic import EmailStr, Field

from dddesign.structure.domains.dto import DataTransferObject


class RegisterDTO(DataTransferObject):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class LoginDTO(DataTransferObject):
    email: EmailStr
    password: str


class UserDTO(DataTransferObject):
    user_id: UUID
    email: EmailStr
    is_email_confirmed: bool
