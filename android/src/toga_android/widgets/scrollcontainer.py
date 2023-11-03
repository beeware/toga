from decimal import ROUND_DOWN

from android.view import Gravity, View
from android.widget import HorizontalScrollView, LinearLayout, ScrollView
from java import dynamic_proxy

from ..container import Container
from .base import Widget


class TogaOnTouchListener(dynamic_proxy(View.OnTouchListener)):
    def __init__(self):
        super().__init__()
        self.is_scrolling_enabled = True

    def onTouch(self, view, motion_event):
        if self.is_scrolling_enabled:
            return view.onTouchEvent(motion_event)
        else:
            return True


class TogaOnScrollListener(dynamic_proxy(View.OnScrollChangeListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onScrollChange(self, view, new_x, new_y, old_x, old_y):
        self.impl.interface.on_scroll()


class ScrollContainer(Widget, Container):
    def create(self):
        scroll_listener = TogaOnScrollListener(self)

        self.native = self.vScrollView = ScrollView(self._native_activity)
        vScrollView_layout_params = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.MATCH_PARENT,
        )
        vScrollView_layout_params.gravity = Gravity.TOP
        self.vScrollView.setLayoutParams(vScrollView_layout_params)
        self.vScrollListener = TogaOnTouchListener()
        self.vScrollView.setOnTouchListener(self.vScrollListener)
        self.vScrollView.setOnScrollChangeListener(scroll_listener)

        self.hScrollView = HorizontalScrollView(self._native_activity)
        hScrollView_layout_params = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.MATCH_PARENT,
        )
        hScrollView_layout_params.gravity = Gravity.LEFT
        self.hScrollListener = TogaOnTouchListener()
        self.hScrollView.setOnTouchListener(self.hScrollListener)
        self.hScrollView.setOnScrollChangeListener(scroll_listener)
        self.vScrollView.addView(self.hScrollView, hScrollView_layout_params)

        self.init_container(self.hScrollView)

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.resize_content(
            self.scale_in(width, ROUND_DOWN),
            self.scale_in(height, ROUND_DOWN),
        )

    def get_vertical(self):
        return self.vScrollListener.is_scrolling_enabled

    def set_vertical(self, value):
        if not value:
            self.vScrollView.setScrollY(0)
        self.vScrollListener.is_scrolling_enabled = value

    def get_horizontal(self):
        return self.hScrollListener.is_scrolling_enabled

    def set_horizontal(self, value):
        if not value:
            self.hScrollView.setScrollX(0)
        self.hScrollListener.is_scrolling_enabled = value

    def get_vertical_position(self):
        return self.scale_out(self.vScrollView.getScrollY())

    def get_horizontal_position(self):
        return self.scale_out(self.hScrollView.getScrollX())

    def get_max_horizontal_position(self):
        return self.scale_out(
            max(0, self.native_content.getWidth() - self.native.getWidth())
        )

    def get_max_vertical_position(self):
        return self.scale_out(
            max(0, self.native_content.getHeight() - self.native.getHeight())
        )

    def set_position(self, horizontal_position, vertical_position):
        self.hScrollView.setScrollX(self.scale_in(horizontal_position))
        self.vScrollView.setScrollY(self.scale_in(vertical_position))

    def set_background_color(self, value):
        self.set_background_simple(value)
