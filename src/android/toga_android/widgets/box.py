from ..libs.activity import MainActivity
from ..libs.android_widgets import RelativeLayout, RelativeLayout__LayoutParams
from .base import Widget


class Box(Widget):
    def create(self):
        self.native = RelativeLayout(MainActivity.singletonThis)

    def set_child_bounds(self, widget, x, y, width, height):
        # Avoid setting child boundaries if `create()` has not been called.
        if not widget.native:
            return
        # We assume `widget.native` has already been added to this `RelativeLayout`.
        #
        # We use `topMargin` and `leftMargin` to perform absolute layout. Not very
        # relative, but that's how we do it.
        layout_params = RelativeLayout__LayoutParams(width, height)
        layout_params.topMargin = y
        layout_params.leftMargin = x
        self.native.updateViewLayout(widget.native, layout_params)
