from travertino.size import at_least

from toga_android.window import AndroidViewport

from ..libs.android.view import (
    Gravity,
    View__MeasureSpec,
    View__OnScrollChangeListener,
    View__OnTouchListener,
)
from ..libs.android.widget import (
    HorizontalScrollView,
    LinearLayout__LayoutParams,
    ScrollView,
)
from .base import Widget


class TogaOnTouchListener(View__OnTouchListener):
    def __init__(self):
        super().__init__()
        self.is_scrolling_enabled = True

    def onTouch(self, view, motion_event):
        if self.is_scrolling_enabled:
            return view.onTouchEvent(motion_event)
        else:
            return True


class TogaOnScrollListener(View__OnScrollChangeListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onScrollChange(self, view, new_x, new_y, old_x, old_y):
        self.impl.interface.on_scroll(None)


class ScrollContainer(Widget):
    def create(self):
        scroll_listener = TogaOnScrollListener(self)

        self.native = self.vScrollView = ScrollView(self._native_activity)
        vScrollView_layout_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT,
        )
        vScrollView_layout_params.gravity = Gravity.TOP
        self.vScrollView.setLayoutParams(vScrollView_layout_params)
        self.vScrollListener = TogaOnTouchListener()
        self.vScrollView.setOnTouchListener(self.vScrollListener)
        self.vScrollView.setOnScrollChangeListener(scroll_listener)

        self.hScrollView = HorizontalScrollView(self._native_activity)
        hScrollView_layout_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT,
        )
        hScrollView_layout_params.gravity = Gravity.LEFT
        self.hScrollListener = TogaOnTouchListener()
        self.hScrollView.setOnTouchListener(self.hScrollListener)
        self.hScrollView.setOnScrollChangeListener(scroll_listener)
        self.vScrollView.addView(self.hScrollView, hScrollView_layout_params)

        self.content = None

    def set_content(self, widget):
        if self.content:
            self.hScrollView.removeAllViews()
            for child in self.content.interface.children:
                child._impl.container = None

        self.content = widget
        if widget:
            widget.viewport = AndroidViewport(self.native, self.interface)
            content_view_params = LinearLayout__LayoutParams(
                LinearLayout__LayoutParams.MATCH_PARENT,
                LinearLayout__LayoutParams.MATCH_PARENT,
            )
            if widget.container:
                widget.container = None
            self.hScrollView.addView(widget.native, content_view_params)

            for child in widget.interface.children:
                if child._impl.container:
                    child._impl.container = None
                child._impl.container = widget

    def get_vertical(self):
        return self.vScrollListener.is_scrolling_enabled

    def set_vertical(self, value):
        self.vScrollListener.is_scrolling_enabled = value

    def get_horizontal(self):
        return self.hScrollListener.is_scrolling_enabled

    def set_horizontal(self, value):
        self.hScrollListener.is_scrolling_enabled = value

    def get_vertical_position(self):
        return self.vScrollView.getScrollY() / self.scale

    def get_horizontal_position(self):
        return self.hScrollView.getScrollX() / self.scale

    def get_max_horizontal_position(self):
        content_width = 0 if self.content is None else self.content.native.getWidth()
        return max(0, content_width - self.native.getWidth()) / self.scale

    def get_max_vertical_position(self):
        content_height = 0 if self.content is None else self.content.native.getHeight()
        return max(0, content_height - self.native.getHeight()) / self.scale

    def set_position(self, horizontal_position, vertical_position):
        self.hScrollView.setScrollX(horizontal_position * self.scale)
        self.vScrollView.setScrollY(vertical_position * self.scale)

    def set_background_color(self, value):
        self.set_background_simple(value)

    def rehint(self):
        # Android can crash when rendering some widgets until they have their layout params set. Guard for that case.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = at_least(self.native.getMeasuredHeight())
