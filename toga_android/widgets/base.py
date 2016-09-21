from toga.widget import Widget as WidgetBase


class Widget(WidgetBase):
    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        self.is_container = False
        self._in_progress = False

    def _update_layout(self, **style):
        """Force a layout update on the widget.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        print("DO WIDGET LAYOUT", self)
        if self._in_progress:
            return
        self._in_progress = True

        self.style(**style)

        # Recompute layout
        layout = self.layout
        print("WIDGET LAYOUT", layout)

        # Set the frame for the widget to adhere to the new style.
        self._set_frame(layout.left, layout.top, layout.left + layout.right, layout.top + layout.height)

        self._update_child_layout(**style)

        # Set the frame for the widget to adhere to the new style.
        self._set_child_frames()

        self._in_progress = False

    def _set_frame(self, left, top, right, bottom):
        print("SET FRAME", self, left, right, top, bottom)
        self._impl.layout(left, right, top, bottom)

    def _update_child_layout(self, **style):
        """Force a layout update on children of this widget.

        By default, do nothing; widgets have no children
        """
        pass

    def _set_child_frames(self):
        pass
