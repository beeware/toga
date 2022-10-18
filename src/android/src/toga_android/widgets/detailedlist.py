from rubicon.java.android_events import Handler, PythonRunnable
from travertino.size import at_least

from ..libs.android import R__color
from ..libs.android.graphics import BitmapFactory, Rect
from ..libs.android.view import Gravity, OnClickListener, View__MeasureSpec
from ..libs.android.widget import (
    ImageView,
    ImageView__ScaleType,
    LinearLayout,
    LinearLayout__LayoutParams,
    RelativeLayout,
    RelativeLayout__LayoutParams,
    ScrollView,
    TextView
)
from ..libs.androidx.swiperefreshlayout import (
    SwipeRefreshLayout,
    SwipeRefreshLayout__OnRefreshListener
)
from .base import Widget


class DetailedListOnClickListener(OnClickListener):
    def __init__(self, impl, row_number):
        super().__init__()
        self._impl = impl
        self._row_number = row_number

    def onClick(self, _view):
        row = self._impl.interface.data[self._row_number]
        self._impl._selection = row
        if self._impl.interface.on_select:
            self._impl.interface.on_select(self._impl.interface, row=self._impl.interface.data[self._row_number])


class OnRefreshListener(SwipeRefreshLayout__OnRefreshListener):
    def __init__(self, interface):
        super().__init__()
        self._interface = interface

    def onRefresh(self):
        if self._interface.on_refresh:
            self._interface.on_refresh(self._interface)


class DetailedList(Widget):
    ROW_HEIGHT = 250
    _swipe_refresh_layout = None
    _scroll_view = None
    _dismissable_container = None
    _selection = None

    def create(self):
        # DetailedList is not a specific widget on Android, so we build it out
        # of a few pieces.
        if self.native is None:
            self.native = LinearLayout(self._native_activity)
            self.native.setOrientation(LinearLayout.VERTICAL)
        else:
            # If create() is called a second time, clear the widget and regenerate it.
            self.native.removeAllViews()

        scroll_view = ScrollView(self._native_activity)
        self._scroll_view = scroll_view.__global__()
        scroll_view_layout_params = LinearLayout__LayoutParams(
                LinearLayout__LayoutParams.MATCH_PARENT,
                LinearLayout__LayoutParams.MATCH_PARENT
        )
        scroll_view_layout_params.gravity = Gravity.TOP
        swipe_refresh_wrapper = SwipeRefreshLayout(self._native_activity)
        swipe_refresh_wrapper.setOnRefreshListener(OnRefreshListener(self.interface))
        self._swipe_refresh_layout = swipe_refresh_wrapper.__global__()
        swipe_refresh_wrapper.addView(scroll_view)
        self.native.addView(swipe_refresh_wrapper, scroll_view_layout_params)
        dismissable_container = LinearLayout(self._native_activity)
        self._dismissable_container = dismissable_container.__global__()
        dismissable_container.setOrientation(LinearLayout.VERTICAL)
        dismissable_container_params = LinearLayout__LayoutParams(
                LinearLayout__LayoutParams.MATCH_PARENT,
                LinearLayout__LayoutParams.MATCH_PARENT
        )
        scroll_view.addView(
                dismissable_container, dismissable_container_params
        )
        for i in range(len((self.interface.data or []))):
            self._make_row(dismissable_container, i)

    def _make_row(self, container, i):
        # Create the foreground.
        row_foreground = RelativeLayout(self._native_activity)
        container.addView(row_foreground)

        # Add user-provided icon to layout.
        icon_image_view = ImageView(self._native_activity)
        icon = self.interface.data[i].icon
        if icon is not None:
            icon.bind(self.interface.factory)
            bitmap = BitmapFactory.decodeFile(str(icon._impl.path))
            icon_image_view.setImageBitmap(bitmap)
        icon_layout_params = RelativeLayout__LayoutParams(
            RelativeLayout__LayoutParams.WRAP_CONTENT,
            RelativeLayout__LayoutParams.WRAP_CONTENT)
        icon_layout_params.width = 150
        icon_layout_params.setMargins(25, 0, 25, 0)
        icon_layout_params.height = self.ROW_HEIGHT
        icon_image_view.setScaleType(ImageView__ScaleType.FIT_CENTER)
        row_foreground.addView(icon_image_view, icon_layout_params)

        # Create layout to show top_text and bottom_text.
        text_container = LinearLayout(self._native_activity)
        text_container_params = RelativeLayout__LayoutParams(
                RelativeLayout__LayoutParams.WRAP_CONTENT,
                RelativeLayout__LayoutParams.WRAP_CONTENT)
        text_container_params.height = self.ROW_HEIGHT
        text_container_params.setMargins(25 + 25 + 150, 0, 0, 0)
        row_foreground.addView(text_container, text_container_params)
        text_container.setOrientation(LinearLayout.VERTICAL)
        text_container.setWeightSum(2.0)

        # Create top & bottom text; add them to layout.
        top_text = TextView(self._native_activity)
        top_text.setText(str(getattr(self.interface.data[i], 'title', '')))
        top_text.setTextSize(20.0)
        top_text.setTextColor(self._native_activity.getResources().getColor(R__color.black))
        bottom_text = TextView(self._native_activity)
        bottom_text.setTextColor(self._native_activity.getResources().getColor(R__color.black))
        bottom_text.setText(str(getattr(self.interface.data[i], 'subtitle', '')))
        bottom_text.setTextSize(16.0)
        top_text_params = LinearLayout__LayoutParams(
                RelativeLayout__LayoutParams.WRAP_CONTENT,
                RelativeLayout__LayoutParams.MATCH_PARENT)
        top_text_params.weight = 1.0
        top_text.setGravity(Gravity.BOTTOM)
        text_container.addView(top_text, top_text_params)
        bottom_text_params = LinearLayout__LayoutParams(
                RelativeLayout__LayoutParams.WRAP_CONTENT,
                RelativeLayout__LayoutParams.MATCH_PARENT)
        bottom_text_params.weight = 1.0
        bottom_text.setGravity(Gravity.TOP)
        bottom_text_params.gravity = Gravity.TOP
        text_container.addView(bottom_text, bottom_text_params)

        # Apply an onclick listener so that clicking anywhere on the row triggers Toga's on_select(row).
        row_foreground.setOnClickListener(DetailedListOnClickListener(self, i))

    def change_source(self, source):
        # If the source changes, re-build the widget.
        self.create()

    def set_on_refresh(self, handler):
        # No special handling needed.
        pass

    def after_on_refresh(self, widget, result):
        if self._swipe_refresh_layout:
            self._swipe_refresh_layout.setRefreshing(False)

    def insert(self, index, item):
        # If the data changes, re-build the widget. Brutally effective.
        self.create()

    def change(self, item):
        # If the data changes, re-build the widget. Brutally effective.
        self.create()

    def remove(self, index, item):
        # If the data changes, re-build the widget. Brutally effective.
        self.create()

    def clear(self):
        # If the data changes, re-build the widget. Brutally effective.
        self.create()

    def get_selection(self):
        return self._selection

    def set_on_select(self, handler):
        # No special handling required.
        pass

    def set_on_delete(self, handler):
        # This widget currently does not implement event handlers for data change.
        self.interface.factory.not_implemented("DetailedList.set_on_delete()")

    def scroll_to_row(self, row):
        def scroll():
            row_obj = self._dismissable_container.getChildAt(row)
            hit_rect = Rect()
            row_obj.getHitRect(hit_rect)
            self._scroll_view.requestChildRectangleOnScreen(
                    self._dismissable_container,
                    hit_rect,
                    False,
                )
        Handler().post(PythonRunnable(scroll))

    def rehint(self):
        # Android can crash when rendering some widgets until they have their layout params set. Guard for that case.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
