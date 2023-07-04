from .libs.android.view import ViewGroup__LayoutParams
from .libs.android.widget import RelativeLayout, RelativeLayout__LayoutParams


# Common base class of Window, ScrollContainer, and potentially other containers.
class Container:
    def clear_content(self):
        if self.interface.content:
            self.interface.content._impl.viewport = None

    def set_content(self, widget):
        self.clear_content()
        if widget:
            widget.viewport = self.content_viewport


class Viewport:
    def __init__(self, parent, container):
        """
        :param parent: A native widget to display the viewport within.
        :param container: An object with a `content` attribute, which, if not None,
            will have `refresh()` called on it whenever the viewport size changes.
        """
        self.parent = parent
        self.container = container
        self.width = self.height = 0

        context = parent.getContext()
        self.native = RelativeLayout(context)
        self.parent.addView(
            self.native,
            ViewGroup__LayoutParams(
                ViewGroup__LayoutParams.MATCH_PARENT,
                ViewGroup__LayoutParams.MATCH_PARENT,
            ),
        )

        self.dpi = context.getResources().getDisplayMetrics().densityDpi
        # Toga needs to know how the current DPI compares to the platform default,
        # which is 160: https://developer.android.com/training/multiscreen/screendensities
        self.baseline_dpi = 160
        self.scale = self.dpi / self.baseline_dpi

    def refreshed(self):
        pass

    @property
    def size(self):
        return (self.width, self.height)

    @size.setter
    def size(self, size):
        if size != (self.width, self.height):
            self.width, self.height = size
            self.native.setMinimumWidth(self.width)
            self.native.setMinimumHeight(self.height)
            if self.container.content is not None:
                self.container.content.refresh()

    def add_widget(self, widget):
        self.native.addView(widget.native)

    def remove_widget(self, widget):
        self.native.removeView(widget.native)

    def set_widget_bounds(self, widget, x, y, width, height):
        layout_params = RelativeLayout__LayoutParams(width, height)
        layout_params.topMargin = y
        layout_params.leftMargin = x
        self.native.updateViewLayout(widget.native, layout_params)
