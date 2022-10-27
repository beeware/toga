from .base import Source


class ValueSource(Source):
    def __init__(self, value=None):
        self._source = None
        self.value = value

    def __str__(self):
        if self.value is None:
            return ""
        return str(self.value)

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if not attr.startswith("_"):
            if self._source is not None:
                self._source._notify("change", item=self)
