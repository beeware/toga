from travertino.size import at_least

from ..libs import android_widgets, android
from .base import Widget
from toga_android.window import AndroidViewport

class TogaOnTouchListener(android.View__OnTouchListener):
    is_scrolling_enabled = True
    scrollview_impl = None

    def __init__(self, scrollview_impl):
        super().__init__()
        self.scrollview_impl = scrollview_impl
        print('TogaOnTouchListener.scrollview_impl=' + str(self.scrollview_impl))

    def onTouch(self, view, motion_event):
        if self.is_scrolling_enabled:
            return self.scrollview_impl.onTouchEvent(motion_event)
        else:
            return True


class ScrollContainer(Widget):
    vScrollView = None
    vScrollListener = None
    hScrollView = None
    hScrollListener = None

    def create(self):
        print('ScrollContainer.create()')
        print('self.interface.vertical='+str(self.interface.vertical))
        print('self.interface.horizontal='+str(self.interface.horizontal))
        print('self.interface.content='+str(self.interface.content))
        self.vScrollView = android_widgets.ScrollView(self._native_activity)
        vScrollView_layout_params = android_widgets.LinearLayout__LayoutParams(
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
        )
        vScrollView_layout_params.gravity = android_widgets.Gravity.TOP
        self.vScrollView.setLayoutParams(vScrollView_layout_params)
        self.vScrollListener = TogaOnTouchListener(scrollview_impl=self.vScrollView)
        self.vScrollListener.is_scrolling_enabled = self.interface.vertical
        self.vScrollView.setOnTouchListener(self.vScrollListener)
        self.native = self.vScrollView
        print('Created vertical ScrollView')
        self.hScrollView = android_widgets.HorizontalScrollView(self._native_activity)
        hScrollView_layout_params = android_widgets.LinearLayout__LayoutParams(
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
        )
        hScrollView_layout_params.gravity = android_widgets.Gravity.LEFT
        self.hScrollListener = TogaOnTouchListener(scrollview_impl=self.hScrollView)
        self.hScrollListener.is_scrolling_enabled = self.interface.horizontal
        self.hScrollView.setOnTouchListener(self.hScrollListener)
        print('Created horizontal ScrollView')
        self.vScrollView.addView(self.hScrollView, hScrollView_layout_params)
        print('self.native='+str(self.native))

    def set_content(self, widget):
        print('ScrollContainer.set_content()')
        print('widget.native='+str(widget.native))
        widget.viewport = AndroidViewport(widget.native)
        content_view_params = android_widgets.LinearLayout__LayoutParams(
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
        )
        widget_parent = widget.native.getParent()
        print('widget parent='+str(widget_parent))
        if widget_parent is not None:
            print('Removing existing parent from widget')
            widget_parent.removeView(widget.native)
        self.hScrollView.addView(widget.native, content_view_params)
        for child in widget.interface.children:
            child._impl.container = widget
        print('Added content to ScrollContainer')

    def set_vertical(self, value):
        print('ScrollContainer.set_vertical(): '+str(value))
        self.vScrollListener.is_scrolling_enabled = value

    def set_horizontal(self, value):
        self.hScrollListener.is_scrolling_enabled = value

    def rehint(self):
        # Android can crash when rendering some widgets until they have their layout params set. Guard for that case.
        print('ScrollContainer.rehint()')
        if self.native.getLayoutParams() is None:
            return
        self.native.measure(
            android_widgets.View__MeasureSpec.UNSPECIFIED,
            android_widgets.View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
