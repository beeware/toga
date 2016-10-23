from toga.widget import Widget as WidgetBase


class Widget(WidgetBase):
    def __init__(self, *args, **kwargs):
        self.widget_id = kwargs.pop('widget_id', id(self))
        super(Widget, self).__init__(*args, **kwargs)
        self.is_container = False
        self._in_progress = False

    def handler(self, fn, name):
        if hasattr(fn, '__self__'):
            ref = '(%s,%s-%s)' % (fn.__self__.widget_id, self.widget_id, name)
        else:
            ref = '%s-%s' % (self.widget_id, name)

        return ref

    # def _set_app(self, app):
    #     app.support_module.__dict__[self.IMPL_CLASS.__name__] = self.IMPL_CLASS

    # def _update_layout(self, **style):
    #     """Force a layout update on the widget.

    #     The update request can be accompanied by additional style information
    #     (probably min_width, min_height, width or height) to control the
    #     layout.
    #     """
    #     if self._in_progress:
    #         return
    #     self._in_progress = True

    #     self.style(**style)

    #     # Recompute layout
    #     layout = self.layout
    #     print("WIDGET LAYOUT", layout)

    #     # Set the frame for the widget to adhere to the new style.
    #     self._set_frame(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))

    #     self._update_child_layout(**style)

    #     # Set the frame for the widget to adhere to the new style.
    #     self._set_child_frames()

    #     self._in_progress = False

    # def _set_frame(self, frame):
    #     print("SET FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
    #     self._impl.setFrame_(frame)
    #     self._impl.setNeedsDisplay_(True)

    # def _update_child_layout(self, **style):
    #     """Force a layout update on children of this widget.

    #     By default, do nothing; widgets have no children
    #     """
    #     pass

    # def _set_child_frames(self):
    #     pass
