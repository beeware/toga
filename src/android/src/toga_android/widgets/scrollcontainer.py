from travertino.size import at_least

from toga_android.window import AndroidViewport

from ..libs.android.view import (
    Gravity,
    View__MeasureSpec,
    View__OnTouchListener
)
from ..libs.android.widget import (
    HorizontalScrollView,
    LinearLayout__LayoutParams,
    ScrollView
)
from .base import Widget


class TogaOnTouchListener(View__OnTouchListener):
    is_scrolling_enabled = True

    def __init__(self):
        super().__init__()

    def onTouch(self, view, motion_event):
        if self.is_scrolling_enabled:
            return view.onTouchEvent(motion_event)
        else:
            return True


class ScrollContainer(Widget):
    vScrollListener = None
    hScrollView = None
    hScrollListener = None

    def create(self):
        vScrollView = ScrollView(self._native_activity)
        vScrollView_layout_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT
        )
        vScrollView_layout_params.gravity = Gravity.TOP
        vScrollView.setLayoutParams(vScrollView_layout_params)
        self.vScrollListener = TogaOnTouchListener()
        self.vScrollListener.is_scrolling_enabled = self.interface.vertical
        vScrollView.setOnTouchListener(self.vScrollListener)
        self.native = vScrollView
        self.hScrollView = HorizontalScrollView(self._native_activity)
        hScrollView_layout_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT
        )
        hScrollView_layout_params.gravity = Gravity.LEFT
        self.hScrollListener = TogaOnTouchListener()
        self.hScrollListener.is_scrolling_enabled = self.interface.horizontal
        self.hScrollView.setOnTouchListener(self.hScrollListener)
        vScrollView.addView(self.hScrollView, hScrollView_layout_params)
        if self.interface.content is not None:
            self.set_content(self.interface.content)

    def set_content(self, widget):
        widget.viewport = AndroidViewport(self.native, self.interface)
        content_view_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT
        )
        if widget.container:
            widget.container = None
        if self.interface.content:
            self.hScrollView.removeAllViews()
        self.hScrollView.addView(widget.native, content_view_params)
        for child in widget.interface.children:
            if child._impl.container:
                child._impl.container = None
            child._impl.container = widget

    def set_vertical(self, value):
        self.vScrollListener.is_scrolling_enabled = value

    def set_horizontal(self, value):
        self.hScrollListener.is_scrolling_enabled = value

    def set_on_scroll(self, on_scroll):
        self.interface.factory.not_implemented("ScrollContainer.set_on_scroll()")

    def get_vertical_position(self):
        self.interface.factory.not_implemented(
            "ScrollContainer.get_vertical_position()"
        )
        return 0

    def set_vertical_position(self, vertical_position):
        self.interface.factory.not_implemented(
            "ScrollContainer.set_vertical_position()"
        )

    def get_horizontal_position(self):
        self.interface.factory.not_implemented(
            "ScrollContainer.get_horizontal_position()"
        )
        return 0

    def set_horizontal_position(self, horizontal_position):
        self.interface.factory.not_implemented(
            "ScrollContainer.set_horizontal_position()"
        )

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
