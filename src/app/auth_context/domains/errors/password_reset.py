from dddesign.structure.domains.errors import BaseError


class InvalidResetCodeError(BaseError):
    status_code: int = 400
    message: str = 'Invalid or expired password reset code'
