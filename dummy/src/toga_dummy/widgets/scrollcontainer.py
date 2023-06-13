from ..utils import not_required
from ..window import Container
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class ScrollContainer(Widget):
    def create(self):
        self._action("create ScrollContainer")
        self.scroll_container = Container(self)

    # Required to satisfy the scroll container
    def get_width(self):
        return 3700

    # Required to satisfy the scroll container
    def get_height(self):
        return 4200

    def set_content(self, widget):
        self._action("set content", widget=widget)

    def get_vertical(self):
        return self._get_value("vertical", True)

    def set_vertical(self, value):
        self._set_value("vertical", value)

    def get_horizontal(self):
        return self._get_value("horizontal", True)

    def set_horizontal(self, value):
        self._set_value("horizontal", value)

    def set_on_scroll(self, on_scroll):
        self._set_value("on_scroll", on_scroll)

    def set_position(self, horizontal_position, vertical_position):
        self._set_value("horizontal_position", horizontal_position)
        self._set_value("vertical_position", vertical_position)

    def get_horizontal_position(self):
        return self._get_value("horizontal_position", 0)

    def get_max_horizontal_position(self):
        return 1000

    def get_vertical_position(self):
        if not self.get_vertical():
            return None
        return self._get_value("vertical_position", 0)

    def get_max_vertical_position(self):
        return 2000
