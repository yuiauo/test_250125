import os
from typing import Any

import jwt


def encode(payload: dict[str, Any]):
    expires_in = os.getenv("ACCESS_TOKEN_LIFETIME")
    payload.update(expires_in=expires_in)
    return jwt.encode(payload)

