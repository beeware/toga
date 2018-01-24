from .base import Widget
from .. import impl


class Label(Widget):
    def create(self):
        self._impl = impl.Label(
            id=self.id,
            text=self._config['text'],
            alignment=self._config['alignment'],
            style=self.style,
        )

    def set_text(self, value):
        self._impl.innerText = self.interface._text

    def set_alignment(self, value):
        self.interface.factory.not_implemented('Label.set_alignment()')

    def rehint(self):
        pass

