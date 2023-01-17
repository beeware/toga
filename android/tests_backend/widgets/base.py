from pytest import skip


class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        container_native = container._impl.native
        for i in range(container_native.getChildCount()):
            child = container_native.getChildAt(i)
            if child is self.native:
                break
        else:
            raise AssertionError(f"cannot find {self.native} in {container_native}")

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Refresh the layout
        self.widget.window.content.refresh()

    @property
    def enabled(self):
        return self.native.isEnabled()

    @property
    def background_color(self):
        skip("not implemented: background_color")

    @property
    def color(self):
        skip("not implemented: color")

    @property
    def hidden(self):
        skip("not implemented: hidden")

    @property
    def width(self):
        return self.native.getWidth()

    @property
    def height(self):
        return self.native.getHeight()

    def press(self):
        self.native.performClick()
