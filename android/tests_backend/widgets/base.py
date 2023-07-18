import asyncio

from java import dynamic_proxy
from pytest import approx

from android.graphics.drawable import (
    ColorDrawable,
    DrawableContainer,
    DrawableWrapper,
    LayerDrawable,
)
from android.os import Build, SystemClock
from android.view import MotionEvent, View, ViewTreeObserver
from toga.colors import TRANSPARENT
from toga.style.pack import JUSTIFY, LEFT

from ..probe import BaseProbe
from .properties import toga_color, toga_vertical_alignment


class LayoutListener(dynamic_proxy(ViewTreeObserver.OnGlobalLayoutListener)):
    def __init__(self):
        super().__init__()
        self.event = asyncio.Event()

    def onGlobalLayout(self):
        self.event.set()


class SimpleProbe(BaseProbe):
    def __init__(self, widget):
        super().__init__()
        self.app = widget.app
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
        assert self.widget._impl.container is container._impl.container
        assert self.native.getParent() is container._impl.container.native_content

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.getParent() is None

    def assert_alignment(self, expected):
        actual = self.alignment
        if expected == JUSTIFY and (
            Build.VERSION.SDK_INT < 26 or not self.supports_justify
        ):
            assert actual == LEFT
        else:
            assert actual == expected

    def assert_vertical_alignment(self, expected):
        assert toga_vertical_alignment(self.native.getGravity()) == expected

    async def redraw(self, message=None, delay=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        self.native.requestLayout()
        try:
            event = self.layout_listener.event
            event.clear()
            await asyncio.wait_for(event.wait(), 5)
        except asyncio.TimeoutError:
            print("Redraw timed out")

        await super().redraw(message=message, delay=delay)

    @property
    def enabled(self):
        return self.native.isEnabled()

    @property
    def width(self):
        # Return the value in DP
        return round(self.native.getWidth() / self.scale_factor)

    @property
    def height(self):
        # Return the value in DP
        return round(self.native.getHeight() / self.scale_factor)

    def assert_width(self, min_width, max_width):
        assert (
            min_width <= self.width <= max_width
        ), f"Width ({self.width}) not in range ({min_width}, {max_width})"

    def assert_height(self, min_height, max_height):
        assert (
            min_height <= self.height <= max_height
        ), f"Height ({self.height}) not in range ({min_height}, {max_height})"

    @property
    def shrink_on_resize(self):
        return True

    def assert_layout(self, size, position):
        # Widget is contained
        assert self.widget._impl.container is not None
        assert self.native.getParent() is not None

        # Size and position is as expected. Values must be scaled from DP, and
        # compared inexactly due to pixel scaling
        assert (
            approx(self.native.getWidth() / self.scale_factor, rel=0.01),
            approx(self.native.getHeight() / self.scale_factor, rel=0.01),
        ) == size
        assert (
            approx(self.native.getLeft() / self.scale_factor, rel=0.01),
            approx(self.native.getTop() / self.scale_factor, rel=0.01),
        ) == position

    @property
    def background_color(self):
        background = self.native.getBackground()
        while True:
            if isinstance(background, ColorDrawable):
                return toga_color(background.getColor())

            # The following complex Drawables all apply color filters to their children,
            # but they don't implement getColorFilter, at least not in our current
            # minimum API level.
            elif isinstance(background, LayerDrawable):
                background = background.getDrawable(0)
            elif isinstance(background, DrawableContainer):
                background = background.getCurrent()
            elif isinstance(background, DrawableWrapper):
                background = background.getDrawable()

            else:
                break

        if background is None:
            return TRANSPARENT
        filter = background.getColorFilter()
        if filter:
            # PorterDuffColorFilter.getColor is undocumented, but continues to work for
            # now. If this method is blocked in the future, another option is to use the
            # filter to draw something and see what color comes out.
            return toga_color(filter.getColor())
        else:
            return TRANSPARENT

    async def press(self):
        self.native.performClick()

    def motion_event(self, down_time, action, x, y):
        event = MotionEvent.obtain(
            down_time,
            SystemClock.uptimeMillis(),  # eventTime
            action,
            x,
            y,
            0,  # metaState
        )
        self.native.dispatchTouchEvent(event)
        event.recycle()

    async def swipe(self, dx, dy):
        down_time = SystemClock.uptimeMillis()
        start_x, start_y = (self.width / 2, self.height / 2)
        end_x, end_y = (start_x + dx, start_y + dy)
        self.motion_event(down_time, MotionEvent.ACTION_DOWN, start_x, start_y)
        self.motion_event(down_time, MotionEvent.ACTION_MOVE, end_x, end_y)
        self.motion_event(down_time, MotionEvent.ACTION_UP, end_x, end_y)

    @property
    def is_hidden(self):
        return self.native.getVisibility() == View.INVISIBLE

    @property
    def has_focus(self):
        return self.widget.app._impl.native.getCurrentFocus() == self.native
