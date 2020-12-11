from ..libs import android_widgets
from .base import Widget
from toga_android.window import AndroidViewport

class ScrollContainer(Widget):
    hScrollView = None
    vScrollView = None
    content = None

    def create(self):
        if self.interface.vertical:
            vScrollView = android_widgets.ScrollView(self._native_activity)
            vScrollView_layout_params = android_widgets.LinearLayout__LayoutParams(
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
            )
            vScrollView_layout_params.gravity = android_widgets.Gravity.TOP
        if self.interface.horizontal:
            hScrollView = android_widgets.HorizontalScrollView(self._native_activity)
            hScrollView_layout_params = android_widgets.LinearLayout__LayoutParams(
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
                android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
            )
            hScrollView_layout_params.gravity = android_widgets.Gravity.LEFT
            if (self.interface.vertical):
                vScrollView.addView(hScrollView, hScrollView_layout_params)
        if vScrollView is not None:
            self.native = vScrollView
        else:
            if hScrollView is not None:
                self.native = hScrollView
            else:
                raise ValueError('ScrollContainer: either horizontal or vertical must be true')

    def set_content(self, widget):
        self.content = widget
        widget.viewport = AndroidViewport(widget.native)
        content_view_params = android_widgets.LinearLayout__LayoutParams(
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT,
            android_widgets.LinearLayout__LayoutParams.MATCH_PARENT
        )
        self.native.addView(widget.native, content_view_params)

    def set_vertical(self, value):
        self.create()
        if self.content is not None:
            self.set_content(self.content)

    def set_horizontal(self, value):
        self.create()
        if self.content is not None:
            self.set_content(self.content)

    def rehint(self):
        # Android can crash when rendering some widgets until they have their layout params set. Guard for that case.
        if self.native.getLayoutParams() is None:
            return
        self.native.measure(
            android_widgets.View__MeasureSpec.UNSPECIFIED,
            android_widgets.View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
