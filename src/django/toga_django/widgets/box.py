from toga.interface import Box as BoxInterface

from .. import impl
from .base import WidgetMixin


class Box(BoxInterface, WidgetMixin):
    def __init__(self, id=None, style=None, children=None):
        super().__init__(id=id, style=style, children=children)
        self._create()

    def create(self):
        self._impl = impl.Box(
            id=self.id,
            style=self.style,
        )

    def _add_child(self, child):
        self._impl.add_child(child._impl)

    def _set_app(self, app):
        # for child in self.children:
            # child.app = app
        # app.support_module.__dict__['TogaBox'] = TogaBox
        pass

    def _set_window(self, window):
        # for child in self.children:
            # child.window = window
        pass

    # def _hint_size(self, width, height, min_width=None, min_height=None):
    #     if width is not None:
    #         self.width = width
    #     else:
    #         del(self.width)

    #     if min_width is not None:
    #         self.min_width = min_width
    #     else:
    #         del(self.min_width)

    #     if height is not None:
    #         self.height = height
    #     else:
    #         del(self.height)

    #     if min_height is not None:
    #         self.min_height = min_height
    #     else:
    #         del(self.min_height)

    # def _update_child_layout(self, **style):
    #     """Force a layout update on children of this container.

    #     The update request can be accompanied by additional style information
    #     (probably min_width, min_height, width or height) to control the
    #     layout.
    #     """
    #     for child in self.children:
    #         if child.is_container:
    #             child._update_layout()

    # def _set_frame(self, frame):
    #     print("SET FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
    #     self._impl.setFrame_(frame)
    #     self._impl.setNeedsDisplay_(True)
    #     for child in self.children:
    #         layout = child.layout
    #         child._set_frame(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))
