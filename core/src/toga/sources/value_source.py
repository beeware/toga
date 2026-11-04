from __future__ import annotations

from .base import Source


class ValueSource(Source):
    """
    :param value:
    :param accessor:
    """

    def __init__(self, value: object = None, accessor: str = "value"):
        super().__init__()
        self.accessor = accessor
        setattr(self, accessor, value)

    def __str__(self) -> str:
        return str(getattr(self, self.accessor, None))

    def __setattr__(self, attr: str, value: object) -> None:
        notify = attr == getattr(self, "accessor", None)
        if notify:
            self.notify("pre_change", item=getattr(self, attr, None))
        super().__setattr__(attr, value)
        if notify:
            self.notify("change", item=value)
