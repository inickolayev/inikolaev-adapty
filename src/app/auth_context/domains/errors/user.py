from dddesign.structure.domains.errors import BaseError


class UserAlreadyExistsError(BaseError):
    status_code: int = 400
    message: str = 'User with this email already exists'


class InvalidCredentialsError(BaseError):
    status_code: int = 401
    message: str = 'Invalid email or password'


class UserNotFoundError(BaseError):
    status_code: int = 404
    message: str = 'User not found'


class EmailNotConfirmedError(BaseError):
    status_code: int = 403
    message: str = 'Email is not confirmed'
