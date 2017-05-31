from toga.interface import Label as LabelInterface

from .. import impl
from .base import WidgetMixin
# from ..utils import process_callback


class Label(LabelInterface, WidgetMixin):
    def __init__(self, text, id=None, style=None, alignment=None):
        super().__init__(text, id=id, style=style, alignment=alignment)
        self._create()

    def create(self):
        self._impl = impl.Label(
            id=self.id,
            text=self._config['text'],
            alignment=self._config['alignment'],
            style=self.style,
        )

    def _set_text(self, text):
        self._impl.innerText = text

    def _set_alignment(self, text):
        pass
