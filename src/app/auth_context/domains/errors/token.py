from dddesign.structure.domains.errors import BaseError


class InvalidTokenError(BaseError):
    status_code: int = 401
    message: str = 'Invalid authentication token'


class TokenExpiredError(BaseError):
    status_code: int = 401
    message: str = 'Authentication token has expired'


class RefreshTokenRevokedError(BaseError):
    status_code: int = 401
    message: str = 'Refresh token is no longer valid'
