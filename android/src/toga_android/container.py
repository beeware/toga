from .libs.android.widget import RelativeLayout, RelativeLayout__LayoutParams


class Container:
    def init_container(self, native_parent):
        self.width = self.height = 0

        context = native_parent.getContext()
        self.native_content = RelativeLayout(context)
        native_parent.addView(self.native_content)

        self.dpi = context.getResources().getDisplayMetrics().densityDpi
        # Toga needs to know how the current DPI compares to the platform default,
        # which is 160: https://developer.android.com/training/multiscreen/screendensities
        self.baseline_dpi = 160
        self.scale = self.dpi / self.baseline_dpi

    def set_content(self, widget):
        self.clear_content()
        if widget:
            widget.container = self

    def clear_content(self):
        if self.interface.content:
            self.interface.content._impl.container = None

    def resize_content(self, width, height):
        if (self.width, self.height) != (width, height):
            self.width, self.height = (width, height)
            if self.interface.content:
                self.interface.content.refresh()

    def refreshed(self):
        # We must use the correct LayoutParams class, but we don't know what that class
        # is, so reuse the existing object. Calling the constructor of type(lp) is also
        # an option, but would probably be less safe because a subclass might change the
        # meaning of the (int, int) constructor.
        lp = self.native_content.getLayoutParams()
        layout = self.interface.content.layout
        lp.width = max(self.width, layout.width)
        lp.height = max(self.height, layout.height)
        self.native_content.setLayoutParams(lp)

    def add_content(self, widget):
        self.native_content.addView(widget.native)

    def remove_content(self, widget):
        self.native_content.removeView(widget.native)

    def set_content_bounds(self, widget, x, y, width, height):
        lp = RelativeLayout__LayoutParams(width, height)
        lp.topMargin = y
        lp.leftMargin = x
        widget.native.setLayoutParams(lp)
