from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self._action('create ScrollContainer')
        self._horizontal_position = 0
        self._vertical_position = 0

    def set_content(self, widget):
        self._action('set content', widget=widget)

    def set_vertical(self, value):
        self._set_value('vertical', value)

    def set_horizontal(self, value):
        self._set_value('horizontal', value)

    def set_on_scroll(self, on_scroll):
        self._set_value('on_scroll', on_scroll)

    def set_horizontal_position(self, horizontal_position):
        self._set_value('horizontal_position', horizontal_position)
        self._horizontal_position = horizontal_position

    def get_horizontal_position(self):
        return self._horizontal_position

    def set_vertical_position(self, vertical_position):
        self._set_value('vertical_position', vertical_position)
        self._vertical_position = vertical_position

    def get_vertical_position(self):
        return self._vertical_position
