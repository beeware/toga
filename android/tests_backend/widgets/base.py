import asyncio

from java import dynamic_proxy

from android.view import ViewTreeObserver
from toga.fonts import SYSTEM

from .properties import toga_color


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

    def assert_alignment(self, expected):
        assert self.alignment == expected

    def assert_font_family(self, expected):
        actual = self.font.family
        if expected == SYSTEM:
            assert actual == "sans-serif"
        else:
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
    def width(self):
        # Return the value in DP
        return self.native.getWidth() / self.scale_factor

    @property
    def height(self):
        # Return the value in DP
        return self.native.getHeight() / self.scale_factor

    def assert_width(self, min_width, max_width):
        assert (
            min_width <= self.width <= max_width
        ), f"Width ({self.width}) not in range ({min_width}, {max_width})"

    def assert_height(self, min_height, max_height):
        assert (
            min_height <= self.height <= max_height
        ), f"Height ({self.height}) not in range ({min_height}, {max_height})"

    @property
    def background_color(self):
        return toga_color(self.native.getBackground().getColor())

    async def press(self):
        self.native.performClick()
