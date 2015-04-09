from __future__ import print_function, absolute_import, division, unicode_literals

from toga.widget import Widget as WidgetBase

from rubicon.objc import NSRect, NSPoint, NSSize

_level = 0

class Widget(WidgetBase):
    def _update_layout(self, **style):
        """Force a layout update on the widget.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        global _level
        print ('    ' * _level, 'update %s:' % self, style, (self.left, self.top), (self.width, self.height))
        print ('    ' * _level, '%s pre frame: ' % self, (self._impl.frame.size.width, self._impl.frame.size.height), (self._impl.frame.origin.x, self._impl.frame.origin.y))

        # import traceback, sys
        # traceback.print_stack()

        # Apply the style hints to the widget
        self.style(**style)

        # Recompute layout
        layout = self.layout

        # Set the frame for the widget to adhere to the new style.
        self._set_frame(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))

        _level = _level + 1
        self._update_child_layout(**style)
        _level = _level - 1

        print ('    ' * _level, '%s post frame:' % self, (self._impl.frame.size.width, self._impl.frame.size.height), (self._impl.frame.origin.x, self._impl.frame.origin.y))

    def _set_frame(self, frame):
        self._impl.setFrame_(frame)

    def _update_child_layout(self, **style):
        """Force a layout update on children of this widget.

        By default, do nothing; widgets have no children
        """
        pass

