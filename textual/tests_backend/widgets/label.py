from textual.widgets import Label as TextualLabel

from .base import SimpleProbe


class LabelProbe(SimpleProbe):
    native_class = TextualLabel
    minimum_required_height = 40
    supports_text_width_change = False

    @property
    def text(self):
        return str(self.native.renderable)

    @property
    def height(self):
        return self.widget.layout.content_height

    def assert_text_align(self, expected):
        # Textual label alignment is currently not implemented by the backend.
        return

    def assert_vertical_text_align(self, expected):
        # Textual label vertical alignment is currently not implemented by the backend.
        return
