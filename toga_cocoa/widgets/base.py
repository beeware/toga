from toga.widget import Widget as WidgetBase

from rubicon.objc import NSRect, NSPoint, NSSize


class Widget(WidgetBase):
    def __init__(self, style=None):
        super(Widget, self).__init__(style=style)
        # self.is_container = False

    def _apply_layout(self, layout):
        frame = NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height))
        # print("SET WIDGET FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
        self._impl.setFrame_(frame)
        self._impl.setNeedsDisplay_(True)
