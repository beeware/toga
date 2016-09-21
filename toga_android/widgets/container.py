# from ..libs import CassowaryLayout, LayoutParams, LP

from ..app import App
from .base import Widget


class CSSLayout(extends=android.view.ViewGroup):
    def __init__(self, activity, container):
        super(CSSLayout, self).__init__(activity)
        self.container = container

    def onMeasure(self, widthMeasureSpec: int, heightMeasureSpec: int) -> None:
        widthMode = MeasureSpec.getMode(widthMeasureSpec)
        widthSize = MeasureSpec.getSize(widthMeasureSpec)
        heightMode = MeasureSpec.getMode(heightMeasureSpec)
        heightSize = MeasureSpec.getSize(heightMeasureSpec)

        self.container._update_layout(width=widthSize, height=heightSize)

    def onLayout(self, changed: bool, left: int, top: int, right: int, bottom: int) -> None:
        self._set_frame(left, top, right, bottom)


class Container(Widget):
    def __init__(self):
        super(Container, self).__init__()
        self.children = []

        self.startup()

    def startup(self):
        self._impl = CSSLayout(App._impl)
        self._impl.setLayoutParams(LayoutParams(LP.MATCH_PARENT, LP.MATCH_PARENT))

    def add(self, child):
        self.children.append(child)
        self._add_child(child)

    def _add_child(self, child):
        child.app = self.app
        child.window = self.window
        self._impl.addView(child._impl)

    def _set_app(self, app):
        for child in self.children:
            child.app = app

    def _set_window(self, window):
        for child in self.children:
            child.window = window

    def _hint_size(self, width, height, min_width=None, min_height=None):
        if width is not None:
            self.width = width
        else:
            del(self.width)

        if min_width is not None:
            self.min_width = min_width
        else:
            del(self.min_width)

        if height is not None:
            self.height = height
        else:
            del(self.height)

        if min_height is not None:
            self.min_height = min_height
        else:
            del(self.min_height)

    def _update_child_layout(self, **style):
        """Force a layout update on children of this container.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        for child in self.children:
            if child.is_container:
                child._update_layout()

    def _set_frame(self, left, top, right, bottom):
        print("SET FRAME", self, left, top, right, bottom)
        for child in self.children:
            layout = child.layout
            child._set_frame(left, top, right, bottom)
