from typing import Any

import jwt

from code.settings import settings


def encode_jwt(payload: dict[str, Any]) -> str:
    secret_key = settings.jwt.JWT_SECRET
    algorithm = settings.jwt.JWT_ALGORITHM
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_jwt(token: str) -> dict[str, Any]:
    algorithm = settings.jwt.JWT_ALGORITHM
    secret_key = settings.jwt.JWT_SECRET
    decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
    return decoded
