import asyncio

from android.os import SystemClock
from android.view import KeyEvent
from android.widget import (
    ImageView,
    LinearLayout,
    ListView,
    RelativeLayout,
    ScrollView,
    TextView,
)
from androidx.swiperefreshlayout.widget import SwipeRefreshLayout

from .base import SimpleProbe, find_view_by_type


class DetailedListProbe(SimpleProbe):
    native_class = SwipeRefreshLayout
    supports_actions = True
    supports_refresh = True

    def __init__(self, widget):
        super().__init__(widget)
        self.refresh_layout = self.native
        assert self.refresh_layout.getChildCount() == 2

        # Child index 0 is the refresh icon.
        self.scroll_view = self.native.getChildAt(1)
        assert isinstance(self.scroll_view, ScrollView)
        assert self.scroll_view.getChildCount() == 1

        self.linear_layout = self.scroll_view.getChildAt(0)
        assert isinstance(self.linear_layout, LinearLayout)

    @property
    def row_count(self):
        return self.linear_layout.getChildCount()

    def assert_cell_content(self, row, title, subtitle, icon):
        row_layout = self._row_layout(row)
        assert isinstance(row_layout, RelativeLayout)
        assert row_layout.getChildCount() == 2

        icon_view = row_layout.getChildAt(0)
        assert isinstance(icon_view, ImageView)
        if icon is None:
            assert icon_view.getDrawable() is None
        else:
            assert icon_view.getDrawable().getBitmap() is icon._impl.native

        text_layout = row_layout.getChildAt(1)
        assert isinstance(text_layout, LinearLayout)
        assert text_layout.getChildCount() == 2

        title_view = text_layout.getChildAt(0)
        assert isinstance(title_view, TextView)
        assert str(title_view.getText()) == title

        subtitle_view = text_layout.getChildAt(1)
        assert isinstance(subtitle_view, TextView)
        assert str(subtitle_view.getText()) == subtitle

    def _row_layout(self, row):
        return self.linear_layout.getChildAt(row)

    @property
    def max_scroll_position(self):
        return (
            self.linear_layout.getHeight() - self.scroll_view.getHeight()
        ) / self.scale_factor

    @property
    def scroll_position(self):
        return self.scroll_view.getScrollY() / self.scale_factor

    async def wait_for_scroll_completion(self):
        pass

    async def select_row(self, row, add=False):
        self._row_layout(row).performClick()

    def refresh_available(self):
        return self.scroll_position <= 0

    async def non_refresh_action(self):
        await self._swipe_down(80)

    async def refresh_action(self, active=True):
        await self._swipe_down(180)

    # The minimum distance to trigger a refresh is 128 dp.
    async def _swipe_down(self, distance):
        x = self.native.getWidth() * 0.5
        start_y = self.native.getHeight() * 0.1
        end_y = start_y + (distance * self.scale_factor)

        await self.swipe(x, start_y, x, end_y)
        await asyncio.sleep(0.5)  # Handler isn't called until animation completes.

    async def perform_primary_action(self, row, active=True):
        await self._perform_action(row, self.widget._primary_action, active)

    async def perform_secondary_action(self, row, active=True):
        await self._perform_action(row, self.widget._secondary_action, active)

    async def _perform_action(self, row, action, active):
        expected_actions = []
        if self.widget._impl._primary_action_enabled:
            expected_actions.append(self.widget._primary_action)
        if self.widget._impl._secondary_action_enabled:
            expected_actions.append(self.widget._secondary_action)
        assert (action in expected_actions) == active

        self._row_layout(row).performLongClick()
        await self.redraw("Long-pressed row")

        dialog_view = self.get_dialog_view()
        if not expected_actions:
            assert dialog_view is None
            return

        menu = find_view_by_type(dialog_view, ListView)
        assert [
            str(find_view_by_type(menu.getChildAt(i), TextView).getText())
            for i in range(menu.getChildCount())
        ] == expected_actions

        if active:
            menu.performItemClick(None, expected_actions.index(action), 0)
            await self.redraw("Clicked menu item")
        else:
            timestamp = SystemClock.uptimeMillis()
            dialog_view.dispatchKeyEvent(
                KeyEvent(
                    timestamp,  # downTime
                    timestamp,  # eventTime
                    KeyEvent.ACTION_UP,
                    KeyEvent.KEYCODE_BACK,
                    0,  # repeat
                    0,  # metaState
                    0,  # deviceId
                    0,  # scancode
                    KeyEvent.FLAG_TRACKING,
                ),
            )
            await self.redraw("Closed menu")
            assert self.get_dialog_view() is None
