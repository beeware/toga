import pytest
from textual.widget import Widget as TextualWidget

from ..probe import BaseProbe


class SimpleProbe(BaseProbe):
    invalid_size_while_hidden = False
    supports_text_width_change = True

    def __init__(self, widget):
        super().__init__()
        self.app = widget.app
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        assert self.widget._impl.container is container._impl
        assert self.native.parent is container._impl.native

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.parent is None

    def assert_text_align(self, expected):
        pytest.skip("Text alignment assertions are not implemented on Textual.")

    @property
    def enabled(self):
        return not self.native.disabled

    @property
    def width(self):
        return self.widget.layout.content_width

    @property
    def height(self):
        return self.widget.layout.content_height

    def assert_layout(self, size, position):
        assert self.widget._impl.container is not None
        assert (self.width, self.height) == size
        assert (
            self.widget.layout.absolute_content_left,
            self.widget.layout.absolute_content_top,
        ) == position

    def assert_width(self, min_width, max_width):
        assert min_width <= self.width <= max_width, (
            f"Width ({self.width}) not in range ({min_width}, {max_width})"
        )

    def assert_height(self, min_height, max_height):
        assert min_height <= self.height <= max_height, (
            f"Height ({self.height}) not in range ({min_height}, {max_height})"
        )

    @property
    def shrink_on_resize(self):
        return True

    @property
    def color(self):
        pytest.skip("Foreground color assertions are not implemented on Textual.")

    @property
    def background_color(self):
        pytest.skip("Background color assertions are not implemented on Textual.")

    @property
    def is_hidden(self):
        widget = self.widget
        while widget is not None:
            if not widget._impl.native.display:
                return True
            widget = widget.parent

        return False

    @property
    def has_focus(self):
        return self.native.has_focus

    def assert_font_family(self, expected):
        pytest.skip("Font assertions are not implemented on Textual.")

    def assert_font_size(self, expected):
        pytest.skip("Font assertions are not implemented on Textual.")

    def assert_font_options(self, **expected):
        pytest.skip("Font assertions are not implemented on Textual.")

    async def type_character(self, char):
        pytest.skip("Keyboard input is not implemented on Textual probes.")

    async def undo(self):
        pytest.skip("Undo is not implemented on Textual probes.")

    async def redo(self):
        pytest.skip("Redo is not implemented on Textual probes.")


class TextualWidgetProbe(SimpleProbe):
    native_class = TextualWidget
