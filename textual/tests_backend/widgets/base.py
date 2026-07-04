from math import ceil

import pytest
from textual.widget import Widget as TextualWidget

from ..probe import BaseProbe


class _NativeGeometryAdapter:
    """Convert Textual terminal-cell geometry into Toga-compatible geometry."""

    def __init__(self, widget):
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native

    @property
    def width_cells(self):
        return self.native.styles.width.value

    @property
    def height_cells(self):
        return self.native.styles.height.value

    @property
    def width(self):
        try:
            return self.impl.scale_out_horizontal(self.width_cells)
        except AttributeError:
            return self.widget.layout.content_width

    @property
    def height(self):
        try:
            return self.impl.scale_out_vertical(self.height_cells)
        except AttributeError:
            return self.widget.layout.content_height

    def width_cells_for(self, width):
        return self.impl.scale_in_horizontal(width)

    def height_cells_for(self, height):
        return self.impl.scale_in_vertical(height)

    def width_cells_range(self, min_width, max_width):
        return (
            max(1 if min_width > 0 else 0, self.impl.scale_in_horizontal(min_width)),
            ceil(max_width / self.impl.HORIZONTAL_SCALE),
        )

    def height_cells_range(self, min_height, max_height):
        return (
            max(1 if min_height > 0 else 0, self.impl.scale_in_vertical(min_height)),
            ceil(max_height / self.impl.VERTICAL_SCALE),
        )


class SimpleProbe(BaseProbe):
    invalid_size_while_hidden = False
    supports_tab_index = False
    supports_text_width_change = True

    def __init__(self, widget):
        super().__init__()
        self.app = widget.app
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        self._native_geometry = _NativeGeometryAdapter(widget)
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        assert self.widget._impl.container is container._impl
        assert self.native.parent is container._impl.native

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.parent is None

    def assert_text_align(self, expected):
        pytest.skip("Text alignment assertions are not implemented on Textual.")

    def assert_vertical_text_align(self, expected):
        pytest.skip(
            "Vertical text alignment assertions are not implemented on Textual."
        )

    @property
    def enabled(self):
        return not self.native.disabled

    @property
    def width(self):
        return self._native_geometry.width

    @property
    def height(self):
        return self._native_geometry.height

    def assert_layout(self, size, position):
        assert self.widget._impl.container is not None

        assert (
            self._native_geometry.width_cells
            == self._native_geometry.width_cells_for(size[0])
        )
        assert (
            self._native_geometry.height_cells
            == self._native_geometry.height_cells_for(size[1])
        )
        assert (
            self.widget.layout.absolute_content_left,
            self.widget.layout.absolute_content_top,
        ) == position

    def assert_width(self, min_width, max_width):
        native_width = self._native_geometry.width_cells
        min_native_width, max_native_width = self._native_geometry.width_cells_range(
            min_width, max_width
        )
        assert min_native_width <= native_width <= max_native_width, (
            f"Width ({self.width}) not in range ({min_width}, {max_width})"
        )

    def assert_height(self, min_height, max_height):
        native_height = self._native_geometry.height_cells
        min_native_height, max_native_height = self._native_geometry.height_cells_range(
            min_height, max_height
        )
        assert min_native_height <= native_height <= max_native_height, (
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
