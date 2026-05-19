from dddesign.structure.domains.errors import BaseError


class InvalidConfirmationTokenError(BaseError):
    status_code: int = 400
    message: str = 'Invalid or expired confirmation token'
