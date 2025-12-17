from __future__ import annotations

from dataclasses import fields, is_dataclass
from datetime import UTC, datetime
from typing import Any, TypeVar

T = TypeVar("T")


def to_dataclass(dc_cls: type[T], data: dict[str, Any]) -> T:
    """Filter dict to dataclass fields and build instance."""
    if not is_dataclass(dc_cls):
        raise TypeError(f"{dc_cls} is not a dataclass")
    allowed = {f.name for f in fields(dc_cls)}
    filtered = {k: v for k, v in data.items() if k in allowed}
    return dc_cls(**filtered)  # type: ignore[arg-type]


def to_utc_naive(dt: datetime | None) -> datetime | None:
    """
    Convert timezone-aware datetime -> naive UTC datetime.
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt
    return dt.astimezone(UTC).replace(tzinfo=None)


def orm_to_dict(obj: Any) -> dict[str, Any]:
    """Best-effort: take public attributes from ORM model."""
    return {k: getattr(obj, k) for k in dir(obj) if not k.startswith("_") and hasattr(obj, k)}
