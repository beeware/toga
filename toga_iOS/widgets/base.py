from toga.widget import Widget as WidgetBase

from rubicon.objc import CGRect, CGPoint, CGSize


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
        # print("DO WIDGET LAYOUT", self)
        if self._in_progress:
            return
        self._in_progress = True

        self.style(**style)

        # Recompute layout
        layout = self.layout
        # print("WIDGET LAYOUT", layout)

        # Set the frame for the widget to adhere to the new style.
        self._set_frame(CGRect(CGPoint(layout.left, layout.top), CGSize(layout.width, layout.height)))

        self._update_child_layout(**style)

        # Set the frame for the widget to adhere to the new style.
        self._set_child_frames()

        self._in_progress = False

    def _set_frame(self, frame):
        # print("SET FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
        self._impl.setFrame_(frame)
        self._impl.setNeedsDisplay()

    def _update_child_layout(self, **style):
        """Force a layout update on children of this widget.

        By default, do nothing; widgets have no children
        """
        pass

    def _set_child_frames(self):
        pass
