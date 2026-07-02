from textual.containers import ScrollableContainer as TextualScrollableContainer
from travertino.size import at_least

from .base import Scalable, Widget


class TogaScrollableContainer(TextualScrollableContainer):
    def __init__(self, impl):
        super().__init__(can_focus=False)
        self.interface = impl.interface
        self.impl = impl

    def watch_scroll_x(self, old_value, new_value):
        super().watch_scroll_x(old_value, new_value)
        self.impl.on_native_scroll()

    def watch_scroll_y(self, old_value, new_value):
        super().watch_scroll_y(old_value, new_value)
        self.impl.on_native_scroll()


class ScrollDocumentContainer(Scalable):
    def __init__(self, impl):
        self.impl = impl
        self.native = impl.native
        self.content = None

    @property
    def width(self):
        return self.impl.viewport_width

    @property
    def height(self):
        return self.impl.viewport_height

    def refreshed(self):
        self.impl.content_refreshed()


class ScrollContainer(Widget):
    def create(self):
        self.native = TogaScrollableContainer(self)
        self.document_container = ScrollDocumentContainer(self)
        self._horizontal = True
        self._vertical = True
        self._horizontal_position = 0
        self._vertical_position = 0
        self._viewport_width = self.interface._MIN_WIDTH
        self._viewport_height = self.interface._MIN_HEIGHT
        self._document_width = self._viewport_width
        self._document_height = self._viewport_height
        self._suppress_native_scroll = False

    @property
    def viewport_width(self):
        return self._viewport_width

    @property
    def viewport_height(self):
        return self._viewport_height

    @property
    def document_width(self):
        return self._document_width

    @property
    def document_height(self):
        return self._document_height

    def _native_is_ready(self):
        return self.native.is_attached and self.interface.app is not None

    def install(self, parent, index=None):
        super().install(parent, index)
        if (
            self.document_container.content is not None
            and self.document_container.content.native.parent is None
        ):
            self.document_container.content.install(parent=self.document_container)

    def _set_native_scroll(self, horizontal_position, vertical_position):
        self._suppress_native_scroll = True
        try:
            self.native.scroll_x = self.scale_in_horizontal(horizontal_position)
            self.native.scroll_y = self.scale_in_vertical(vertical_position)
        finally:
            self._suppress_native_scroll = False

    def _clamp_positions(self):
        self._horizontal_position = min(
            self._horizontal_position,
            self.get_max_horizontal_position(),
        )
        self._vertical_position = min(
            self._vertical_position,
            self.get_max_vertical_position(),
        )

    def _sync_native_document_size(self):
        content = self.document_container.content
        if content is not None:
            content.native.styles.width = self.scale_in_horizontal(self._document_width)
            content.native.styles.height = self.scale_in_vertical(self._document_height)

    def _refresh_document_size(self):
        content = self.interface.content
        if content is None:
            self._document_width = self._viewport_width
            self._document_height = self._viewport_height
        else:
            width = self._viewport_width
            height = self._viewport_height
            if self._horizontal:
                width = max(content.layout.width, width)
            if self._vertical:
                height = max(content.layout.height, height)

            self._document_width = width
            self._document_height = height

        self._clamp_positions()
        self._sync_native_document_size()
        self._set_native_scroll(self._horizontal_position, self._vertical_position)

    def content_refreshed(self):
        self._refresh_document_size()

    def on_native_scroll(self):
        if self._suppress_native_scroll:
            return

        if self._horizontal:
            self._horizontal_position = min(
                self.scale_out_horizontal(self.native.scroll_x),
                self.get_max_horizontal_position(),
            )
        if self._vertical:
            self._vertical_position = min(
                self.scale_out_vertical(self.native.scroll_y),
                self.get_max_vertical_position(),
            )
        self.interface.on_scroll()

    def set_content(self, widget):
        old_content = self.document_container.content
        if old_content is not None:
            if old_content.native.parent is self.native:
                self.remove_child(old_content)
            else:
                old_content.container = None

        self.document_container.content = widget
        if widget is not None:
            if self._native_is_ready():
                widget.install(parent=self.document_container)
            else:
                widget.container = self.document_container

        self._refresh_document_size()

    def get_horizontal(self):
        return self._horizontal

    def set_horizontal(self, value):
        self._horizontal = value
        self.native.styles.overflow_x = "auto" if value else "hidden"
        if not value:
            self._horizontal_position = 0

        self._refresh_document_size()
        if not value:
            self.interface.on_scroll()

    def get_vertical(self):
        return self._vertical

    def set_vertical(self, value):
        self._vertical = value
        self.native.styles.overflow_y = "auto" if value else "hidden"
        if not value:
            self._vertical_position = 0

        self._refresh_document_size()
        if not value:
            self.interface.on_scroll()

    def get_max_vertical_position(self):
        if not self._vertical:
            return 0
        return max(0, int(self._document_height - self._viewport_height))

    def get_vertical_position(self):
        return self._vertical_position

    def get_max_horizontal_position(self):
        if not self._horizontal:
            return 0
        return max(0, int(self._document_width - self._viewport_width))

    def get_horizontal_position(self):
        return self._horizontal_position

    def set_position(self, horizontal_position, vertical_position):
        self._horizontal_position = horizontal_position
        self._vertical_position = vertical_position
        self._clamp_positions()
        self._set_native_scroll(self._horizontal_position, self._vertical_position)
        self.interface.on_scroll()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self._viewport_width = self.scale_out_horizontal(
            self.scale_in_horizontal(width)
        )
        self._viewport_height = self.scale_out_vertical(self.scale_in_vertical(height))

        if self.interface.content is not None:
            self.interface.content.refresh()
        else:
            self._refresh_document_size()

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.scale_in_horizontal(self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            self.scale_in_vertical(self.interface._MIN_HEIGHT)
        )
