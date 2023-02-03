import asyncio


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

    def alignment_equivalent(self, actual, expected):
        assert actual == expected
        return True

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # TODO: Travertino/Pack doesn't force a layout refresh
        # when properties such as flex or width are altered.
        # For now, do a manual refresh.
        self.widget.window.content.refresh()

        # Force a repaint
        self.widget.window.content._impl.native.displayIfNeeded()

        # If we're running slow, wait for a second
        if self.widget.app.run_slow:
            await asyncio.sleep(1)

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
