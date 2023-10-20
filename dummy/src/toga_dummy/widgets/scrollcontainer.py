from ..window import Container
from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self._action("create ScrollContainer")
        self.scroll_container = Container()

    # Required to satisfy the scroll container
    def get_width(self):
        return 3700

    # Required to satisfy the scroll container
    def get_height(self):
        return 4200

    def set_content(self, widget):
        self.scroll_container.content = widget
        self._action("set content", widget=widget)
        self.scroll_container.content = widget

    def get_vertical(self):
        return self._get_value("vertical", True)

    def set_vertical(self, value):
        self._set_value("vertical", value)

        # Disabling scrolling implies a position reset; that's a scroll event.
        if value is False:
            self._set_value("vertical_position", 0)
            self.interface.on_scroll()

    def get_horizontal(self):
        return self._get_value("horizontal", True)

    def set_horizontal(self, value):
        self._set_value("horizontal", value)

        # Disabling scrolling implies a position reset; that's a scroll event.
        if value is False:
            self._set_value("horizontal_position", 0)
            self.interface.on_scroll()

    def set_on_scroll(self, on_scroll):
        self._set_value("on_scroll", on_scroll)

    def set_position(self, horizontal_position, vertical_position):
        self._set_value("horizontal_position", horizontal_position)
        self._set_value("vertical_position", vertical_position)
        self.interface.on_scroll()

    def get_horizontal_position(self):
        return self._get_value("horizontal_position", 0)

    def get_max_horizontal_position(self):
        return 1000 if self.get_horizontal() else 0

    def get_vertical_position(self):
        return self._get_value("vertical_position", 0)

    def get_max_vertical_position(self):
        return 2000 if self.get_vertical() else 0
