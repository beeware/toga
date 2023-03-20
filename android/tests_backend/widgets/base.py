import asyncio

from java import dynamic_proxy
from pytest import skip

from android.view import ViewTreeObserver


class LayoutListener(dynamic_proxy(ViewTreeObserver.OnGlobalLayoutListener)):
    def __init__(self):
        super().__init__()
        self.event = asyncio.Event()

    def onGlobalLayout(self):
        self.event.set()
        self.event.clear()


class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.native = widget._impl.native
        self.layout_listener = LayoutListener()
        self.native.getViewTreeObserver().addOnGlobalLayoutListener(
            self.layout_listener
        )

        # Store the device DPI, as it will be needed to scale some values
        self.dpi = (
            self.native.getContext().getResources().getDisplayMetrics().densityDpi
        )
        self.scale_factor = self.dpi / 160

        assert isinstance(self.native, self.native_class)

    def __del__(self):
        self.native.getViewTreeObserver().removeOnGlobalLayoutListener(
            self.layout_listener
        )

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
        self.native.requestLayout()
        await self.layout_listener.event.wait()

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
        # Return the value in DP
        return self.native.getWidth() / self.scale_factor

    @property
    def height(self):
        # Return the value in DP
        return self.native.getHeight() / self.scale_factor

    def press(self):
        self.native.performClick()
