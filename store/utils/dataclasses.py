from typing import Any
from dataclasses import asdict


def asdict_exclude_none(obj: Any) -> dict[str, Any]:
    return {k: v for k, v in asdict(obj).items() if v is not None}
