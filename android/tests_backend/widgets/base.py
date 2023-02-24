import asyncio

from pytest import skip


class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.native = widget._impl.native

        # Store the device DPI, as it will be needed to scale some values
        self.dpi = (
            self.native.getContext().getResources().getDisplayMetrics().densityDpi
        )

        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        container_native = container._impl.native
        for i in range(container_native.getChildCount()):
            child = container_native.getChildAt(i)
            if child is self.native:
                break
        else:
            raise AssertionError(f"cannot find {self.native} in {container_native}")

    def assert_alignment_equivalent(self, actual, expected):
        assert actual == expected

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # TODO: Wait for redraws to complete
        pass

        # If we're running slow, wait for a second
        if self.widget.app.run_slow:
            await asyncio.sleep(1)

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
