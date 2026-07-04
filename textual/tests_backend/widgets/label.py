from textual.widgets import Label as TextualLabel

from .base import SimpleProbe


class LabelProbe(SimpleProbe):
    native_class = TextualLabel
    minimum_required_height = 40
    supports_text_width_change = False

    @property
    def text(self):
        return str(self.native.renderable)
