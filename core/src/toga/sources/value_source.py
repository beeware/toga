from __future__ import annotations

from .base import Source


class ValueSource(Source):
    def __init__(self, value=None, accessor="value"):
        super().__init__()
        self.accessor = accessor
        setattr(self, accessor, value)

    def __str__(self):
        return str(getattr(self, self.accessor, None))

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if attr == getattr(self, "accessor", None):
            self.notify("change", item=value)


class ValueProperty(property):
    def __set__(self, instance, value):
        if isinstance(value, ValueSource):
            value.add_listener(ValueListener(self, instance))
            value = value.value
            # TODO: remove listener when necessary

        super().__set__(instance, value)


class ValueListener:
    def __init__(self, source_property, instance):
        self.source_property = source_property
        self.instance = instance

    def change(self, item):
        self.source_property.__set__(self.instance, item)
