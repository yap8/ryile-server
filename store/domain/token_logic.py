import jwt
from typing import Any
from datetime import datetime, timedelta, timezone

from config import settings


def encode_payload_to_token(
    payload: dict[str, Any], exp_delta: timedelta = settings.token.default_exp_delta
) -> str:
    issued_at = datetime.now(tz=timezone.utc)
    expire = issued_at + exp_delta

    payload["iat"] = issued_at
    payload["exp"] = expire
    token = jwt.encode(
        payload=payload,
        key=settings.token.key,
        algorithm=settings.token.algorithm,
    )
    return token


def decode_payload_from_token(token: str) -> dict:
    payload: dict = jwt.decode(
        token,
        settings.token.key,
        options={"require": ["exp", "iat"]},
        algorithms=[settings.token.algorithm],
    )
    return payload
