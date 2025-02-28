from android.widget import RelativeLayout

from .widgets.base import Scalable


class Container(Scalable):
    def init_container(self, native_parent):
        context = native_parent.getContext()
        self.native_parent = native_parent
        self.init_scale(context)
        self.native_width = self.native_height = 0
        self.content = None

        self.native_content = RelativeLayout(context)
        native_parent.addView(self.native_content)

    @property
    def width(self):
        return self.scale_out(self.native_width)

    @property
    def height(self):
        return self.scale_out(self.native_height)

    def set_content(self, widget):
        self.clear_content()
        if widget:
            widget.container = self
            self.content = widget

    def clear_content(self):
        if self.content:
            self.content.container = None
            self.content = None

    def resize_content(self, width, height):
        if (self.native_width, self.native_height) != (width, height):
            self.native_width, self.native_height = (width, height)
            if self.content:
                self.content.interface.refresh()

    def refreshed(self):
        # We must use the correct LayoutParams class, but we don't know what that class
        # is, so reuse the existing object. Calling the constructor of type(lp) is also
        # an option, but would probably be less safe because a subclass might change the
        # meaning of the (int, int) constructor.
        lp = self.native_content.getLayoutParams()
        layout = self.content.interface.layout
        lp.width = max(self.native_width, self.scale_in(layout.width))
        lp.height = max(self.native_height, self.scale_in(layout.height))
        self.native_content.setLayoutParams(lp)

    def add_content(self, widget):
        self.native_content.addView(widget.native_toplevel)

    def remove_content(self, widget):
        self.native_content.removeView(widget.native_toplevel)

    def set_content_bounds(self, widget, x, y, width, height):
        lp = RelativeLayout.LayoutParams(width, height)
        lp.topMargin = y
        lp.leftMargin = x
        widget.native_toplevel.setLayoutParams(lp)
