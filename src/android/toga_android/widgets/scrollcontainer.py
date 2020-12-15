from travertino.size import at_least

from ..libs import android_widgets
from .base import Widget
from toga_android.window import AndroidViewport

class ScrollContainer(Widget):
    hScrollView = None
    vScrollView = None

    def create(self):
        print('ScrollContainer.create()')
        print('self.interface.vertical='+str(self.interface.vertical))
        print('self.interface.horizontal='+str(self.interface.horizontal))
        print('self.interface.content='+str(self.interface.content))
        if self.interface.vertical:
            self.vScrollView = android_widgets.ScrollView(self._native_activity)
            vScrollView_layout_params = android_widgets.LinearLayout__LayoutParams(
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
            )
            vScrollView_layout_params.gravity = android_widgets.Gravity.TOP
            self.vScrollView.setLayoutParams(vScrollView_layout_params)
            print('Created vertical ScrollView')
            self.native = self.vScrollView
        if self.interface.horizontal:
            self.hScrollView = android_widgets.HorizontalScrollView(self._native_activity)
            hScrollView_layout_params = android_widgets.LinearLayout__LayoutParams(
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
            )
            hScrollView_layout_params.gravity = android_widgets.Gravity.LEFT
            print('Created horizontal ScrollView')
            self.native = self.hScrollView
            if (self.interface.vertical):
                self.vScrollView.addView(self.hScrollView, hScrollView_layout_params)
                self.native = self.vScrollView
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
        if self.hScrollView is not None:
            self.hScrollView.addView(widget.native, content_view_params)
        else:
            self.vScrollView.addView(widget.native, content_view_params)
        for child in widget.interface.children:
            child._impl.container = widget
        print('Added content to ScrollContainer')

    def set_vertical(self, value):
        print('ScrollContainer.set_vertical(): '+str(value))
        if (value is True and self.vScrollView is None) or (value is False and self.vScrollView is not None):
            self.vScrollView = None
            self.hScrollView = None
            self.create()

    def set_horizontal(self, value):
        print('ScrollContainer.set_horizontal(): '+str(value))
        if (value is True and self.hScrollView is None) or (value is False and self.hScrollView is not None):
            self.vScrollView = None
            self.hScrollView = None
            self.create()

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
