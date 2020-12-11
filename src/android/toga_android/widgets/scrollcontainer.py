from ..libs import android_widgets
from .base import Widget
from toga_android.window import AndroidViewport

class ScrollContainer(Widget):
    hScrollView = None
    vScrollView = None
    content = None

    def create(self):
        print('ScrollContainer.create()')
        if self.interface.vertical:
            self.vScrollView = android_widgets.ScrollView(self._native_activity)
            vScrollView_layout_params = android_widgets.LinearLayout__LayoutParams(
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
            )
            vScrollView_layout_params.gravity = android_widgets.Gravity.TOP
        if self.interface.horizontal:
            self.hScrollView = android_widgets.HorizontalScrollView(self._native_activity)
            hScrollView_layout_params = android_widgets.LinearLayout__LayoutParams(
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
            )
            hScrollView_layout_params.gravity = android_widgets.Gravity.LEFT
            if (self.interface.vertical):
                self.vScrollView.addView(self.hScrollView, hScrollView_layout_params)
        if self.vScrollView is not None:
            print('Created vertical ScrollView')
            self.native = self.vScrollView
        else:
            if self.hScrollView is not None:
                print('Created horizontal ScrollView')
                self.native = self.hScrollView
            else:
                raise ValueError('ScrollContainer: either horizontal or vertical must be true')
        if self.interface.content is not None:
            self.set_content(content)

    def set_content(self, widget):
        print('ScrollContainer.set_content()')
        self.content = widget
        widget.viewport = AndroidViewport(widget.native)
        content_view_params = android_widgets.LinearLayout__LayoutParams(
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
        )
        self.native.addView(widget.native, content_view_params)
        print('Added content to ScrollContainer')

    def set_vertical(self, value):
        print('ScrollContainer.set_vertical(): '+str(value))
        if (value is True and self.vScrollView is None) or (value is False and self.vScrollView is not None):
            self.vScrollView = None
            self.hScrollView = None
            self.create()
            if self.content is not None:
                self.set_content(self.content)

    def set_horizontal(self, value):
        print('ScrollContainer.set_horizontal(): '+str(value))
        if (value is True and self.hScrollView is None) or (value is False and self.hScrollView is not None):
            self.vScrollView = None
            self.hScrollView = None
            self.create()
            if self.content is not None:
                self.set_content(self.content)

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
