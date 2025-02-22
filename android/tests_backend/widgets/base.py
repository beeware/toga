import asyncio

import pytest
from android.graphics.drawable import (
    ColorDrawable,
    DrawableContainer,
    DrawableWrapper,
    LayerDrawable,
)
from android.os import Build, SystemClock
from android.view import MotionEvent, View, ViewGroup

from toga.colors import TRANSPARENT
from toga.style.pack import JUSTIFY, LEFT

from ..fonts import FontMixin
from ..probe import BaseProbe
from .properties import toga_color, toga_vertical_alignment


class SimpleProbe(BaseProbe, FontMixin):
    default_font_family = "sans-serif"
    default_font_size = 14

    def __init__(self, widget):
        super().__init__(widget.app)
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        self.native_toplevel = widget._impl.native_toplevel
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        assert self.widget._impl.container is container._impl.container
        assert (
            self.native_toplevel.getParent() is container._impl.container.native_content
        )
        assert (self.native is self.native_toplevel) or (
            self.native.getParent() is self.native_toplevel
        )

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native_toplevel.getParent() is None

    def assert_text_align(self, expected):
        actual = self.text_align
        if expected == JUSTIFY and (
            Build.VERSION.SDK_INT < 26 or not self.supports_justify
        ):
            assert actual == LEFT
        else:
            assert actual == expected

    def assert_vertical_text_align(self, expected):
        assert toga_vertical_alignment(self.native.getGravity()) == expected

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
        assert self.native_toplevel.getParent() is not None

        # Size and position is as expected. Values must be scaled from DP, and
        # compared inexactly due to pixel scaling
        assert (
            pytest.approx(self.native.getWidth() / self.scale_factor, rel=0.01),
            pytest.approx(self.native.getHeight() / self.scale_factor, rel=0.01),
        ) == size
        assert (
            pytest.approx(self.native.getLeft() / self.scale_factor, rel=0.01),
            pytest.approx(self.native.getTop() / self.scale_factor, rel=0.01),
        ) == position

    @property
    def background_color(self):
        background = self.native_toplevel.getBackground()
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
            # The default background color is TRANSPARENT, but setting it
            # to TRANSPARENT actually sets it to None, in order to avoid
            # clipping of ripple and other effects on widgets.
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

    def motion_event(self, down_time, event_time, action, x, y):
        event = MotionEvent.obtain(down_time, event_time, action, x, y, 0)
        self.native.dispatchTouchEvent(event)
        event.recycle()

    async def swipe(self, start_x, start_y, end_x, end_y, *, duration=0.3, hold=0.2):
        down_time = SystemClock.uptimeMillis()
        self.motion_event(
            down_time, down_time, MotionEvent.ACTION_DOWN, start_x, start_y
        )

        # Convert to milliseconds
        duration *= 1000
        hold *= 1000
        end_time = down_time + duration

        dx, dy = end_x - start_x, end_y - start_y
        while (time := SystemClock.uptimeMillis()) < end_time:
            fraction = (time - down_time) / duration
            self.motion_event(
                down_time,
                time,
                MotionEvent.ACTION_MOVE,
                start_x + (dx * fraction),
                start_y + (dy * fraction),
            )
            await asyncio.sleep(0.02)

        # Hold at the end of the swipe to prevent it becoming a "fling"
        end_time += hold
        while (time := SystemClock.uptimeMillis()) < end_time:
            self.motion_event(down_time, time, MotionEvent.ACTION_MOVE, end_x, end_y)
            await asyncio.sleep(0.02)

        self.motion_event(down_time, time, MotionEvent.ACTION_UP, end_x, end_y)

    @property
    def is_hidden(self):
        return self.native.getVisibility() == View.INVISIBLE

    @property
    def has_focus(self):
        return self.widget.app._impl.native.getCurrentFocus() == self.native

    async def undo(self):
        pytest.skip("Undo not supported on this platform")

    async def redo(self):
        pytest.skip("Redo not supported on this platform")


def find_view_by_type(root, cls):
    assert isinstance(root, View)
    if isinstance(root, cls):
        return root
    if isinstance(root, ViewGroup):
        for i in range(root.getChildCount()):
            result = find_view_by_type(root.getChildAt(i), cls)
            if result is not None:
                return result
    return None
