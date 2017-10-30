from .. import impl
from .base import Widget


class Label(Widget):
    def create(self):
        self._impl = impl.Label(
            id=self.id,
            text=self._config['text'],
            alignment=self._config['alignment'],
            style=self.style,
        )

    def set_text(self, value):
        self._impl.innerText = value

    def set_alignment(self, value):
        raise NotImplementedError()

    def rehint(self):
        pass

