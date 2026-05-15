from datetime import timedelta
from typing import Any

import jwt

from ddutils.datetime_helpers import utc_now

from config.settings import settings


def encode_token(payload: dict[str, Any], expires_delta: timedelta) -> str:
    now = utc_now()
    to_encode = {**payload, 'iat': now, 'exp': now + expires_delta}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT.

    Raises ``jwt.ExpiredSignatureError`` / ``jwt.InvalidTokenError`` on failure —
    callers convert these into domain errors.
    """
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
