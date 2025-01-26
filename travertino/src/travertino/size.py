from __future__ import annotations

from dataclasses import dataclass


@dataclass
class at_least:
    """An annotation to wrap around a value to describe that it is a minimum bound."""

    value: int

    def __repr__(self):
        return f"at least {self.value}"


@dataclass
class BaseIntrinsicSize:
    """Representation of the intrinsic size of an object."""

    width: int | None = None
    height: int | None = None

    def __repr__(self):
        return f"({self.width}, {self.height})"
