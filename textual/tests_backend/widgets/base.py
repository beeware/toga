from unittest.mock import ANY

import pytest
from textual.widget import Widget as TextualWidget

from ..probe import BaseProbe


class SimpleProbe(BaseProbe):
    invalid_size_while_hidden = True
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
        return self.impl.scale_out_horizontal(self.native.region.width)

    @property
    def height(self):
        return self.impl.scale_out_vertical(self.native.region.height)

    def scale_expected_horizontal(self, value):
        return ANY if value is ANY else self.impl.scale_in_horizontal(value)

    def scale_expected_vertical(self, value):
        return ANY if value is ANY else self.impl.scale_in_vertical(value)

    def native_horizontal_range(self, width):
        if width == 0:
            return 0, 0
        return (
            self.impl.scale_out_horizontal(width),
            self.impl.scale_out_horizontal(width + 1) - 1,
        )

    def native_vertical_range(self, height):
        if height == 0:
            return 0, 0
        return (
            self.impl.scale_out_vertical(height),
            self.impl.scale_out_vertical(height + 1) - 1,
        )

    @property
    def root_native(self):
        widget = self.widget
        while widget.parent is not None:
            widget = widget.parent
        return widget._impl.native

    @property
    def native_position(self):
        root_region = self.root_native.region
        return (
            self.native.region.x - root_region.x,
            self.native.region.y - root_region.y,
        )

    def assert_layout(self, size, position):
        assert self.widget._impl.container is not None
        if self.is_hidden and size == (ANY, ANY):
            return

        assert (
            self.native.region.width,
            self.native.region.height,
        ) == (
            self.scale_expected_horizontal(size[0]),
            self.scale_expected_vertical(size[1]),
        )
        assert self.native_position == (
            self.scale_expected_horizontal(position[0]),
            self.scale_expected_vertical(position[1]),
        )

    def assert_width(self, min_width, max_width):
        native_min_width, native_max_width = self.native_horizontal_range(
            self.native.region.width
        )
        assert min_width <= native_max_width and native_min_width <= max_width, (
            f"Width ({native_min_width}-{native_max_width}) not in range "
            f"({min_width}, {max_width})"
        )

    def assert_height(self, min_height, max_height):
        native_min_height, native_max_height = self.native_vertical_range(
            self.native.region.height
        )
        assert min_height <= native_max_height and native_min_height <= max_height, (
            f"Height ({native_min_height}-{native_max_height}) not in range "
            f"({min_height}, {max_height})"
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
            if not widget._impl.native.visible:
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
