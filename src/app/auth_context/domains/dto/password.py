from pydantic import EmailStr, Field

from dddesign.structure.domains.dto import DataTransferObject


class PasswordResetRequestDTO(DataTransferObject):
    email: EmailStr


class PasswordResetConfirmDTO(DataTransferObject):
    email: EmailStr
    code: str
    new_password: str = Field(min_length=8, max_length=72)
