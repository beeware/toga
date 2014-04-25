from tailor.cassowary.widget import Container as CassowaryContainer


class Container(CassowaryContainer):
    def __init__(self):
        super(Container, self).__init__()
        self._window = None

    def add(self, widget):
        self._layout_manager.add_widget(widget)
        if self._window:
            widget._create(self._window)

    def _create(self, window, x, y, width, height):
        self._window = window
        for widget in self._layout_manager.children:

            min_width, preferred_width = widget._width_hint
            min_height, preferred_height = widget._height_hint

            x_pos = widget._bounding_box.x.value
            if widget._expand_horizontal:
                width = widget._bounding_box.width.value
            else:
                x_pos = x_pos + ((widget._bounding_box.width.value - preferred_width) / 2.0)
                width = preferred_width

            y_pos = widget._bounding_box.y.value
            if widget._expand_vertical:
                height = widget._bounding_box.height.value
            else:
                y_pos = y_pos + ((widget._bounding_box.height.value - preferred_height) / 2.0)
                height = preferred_height

            widget._create(window, x_pos, y_pos, width, height)

    def _resize(self, x, y, width, height):

        with self._layout_manager.layout(width, height):
            for widget in self._layout_manager.children:
                min_width, preferred_width = widget._width_hint
                min_height, preferred_height = widget._height_hint

                x_pos = widget._bounding_box.x.value
                if widget._expand_horizontal:
                    width = widget._bounding_box.width.value
                else:
                    x_pos = x_pos + ((widget._bounding_box.width.value - preferred_width) / 2.0)
                    width = preferred_width

                y_pos = widget._bounding_box.y.value
                if widget._expand_vertical:
                    height = widget._bounding_box.height.value
                else:
                    y_pos = y_pos + ((widget._bounding_box.height.value - preferred_height) / 2.0)
                    height = preferred_height

                widget._resize(x_pos, y_pos, width, height)

    @property
    def _width_hint(self):
        width = self._layout_manager.bounding_box.width.value
        print "PREFERRED WIDTH", width
        return width, width

    @property
    def _height_hint(self):
        height = self._layout_manager.bounding_box.height.value
        print "PREFERRED HEIGHT", height
        return height, height
