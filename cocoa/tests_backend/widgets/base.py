class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        container_native = container._impl.native
        for control in container_native.subviews:
            if control == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Refresh the layout
        self.widget.window.content.refresh()
        # Force a repaint
        self.widget.window.content._impl.native.displayIfNeeded()

    @property
    def enabled(self):
        return self.native.enabled

    @property
    def hidden(self):
        return self.native.hidden

    @property
    def width(self):
        return self.native.frame.size.width

    @property
    def height(self):
        return self.native.frame.size.height

    def press(self):
        self.native.performClick(None)
