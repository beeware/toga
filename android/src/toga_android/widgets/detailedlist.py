from dataclasses import dataclass

from android import R
from android.app import AlertDialog
from android.content import DialogInterface
from android.graphics import Rect
from android.view import Gravity, View
from android.widget import ImageView, LinearLayout, RelativeLayout, ScrollView, TextView
from java import dynamic_proxy

try:
    from androidx.swiperefreshlayout.widget import SwipeRefreshLayout
except ImportError:  # pragma: no cover
    # Import will fail if SwipeRefreshLayout is not listed in dependencies
    # No cover due to not being able to test in CI
    SwipeRefreshLayout = None


from .base import Widget


class DetailedListOnClickListener(dynamic_proxy(View.OnClickListener)):
    def __init__(self, impl, row_number):
        super().__init__()
        self.impl = impl
        self.row_number = row_number

    def onClick(self, _view):
        self.impl._set_selection(self.row_number)
        self.impl.interface.on_select()


@dataclass
class Action:
    name: str
    handler: callable
    enabled: bool


class DetailedListOnLongClickListener(dynamic_proxy(View.OnLongClickListener)):
    def __init__(self, impl, row_number):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface
        self.row_number = row_number

    def onLongClick(self, _view):
        self.impl._set_selection(self.row_number)
        self.impl.interface.on_select()

        actions = [
            action
            for action in [
                Action(
                    self.interface._primary_action,
                    self.interface.on_primary_action,
                    self.impl._primary_action_enabled,
                ),
                Action(
                    self.interface._secondary_action,
                    self.interface.on_secondary_action,
                    self.impl._secondary_action_enabled,
                ),
            ]
            if action.enabled
        ]

        if actions:
            row = self.interface.data[self.row_number]
            AlertDialog.Builder(self.impl._native_activity).setItems(
                [action.name for action in actions],
                DetailedListActionListener(actions, row),
            ).show()

        return True


class DetailedListActionListener(dynamic_proxy(DialogInterface.OnClickListener)):
    def __init__(self, actions, row):
        super().__init__()
        self.actions = actions
        self.row = row

    def onClick(self, dialog, which):
        self.actions[which].handler(row=self.row)


if SwipeRefreshLayout is not None:  # pragma: no cover

    class OnRefreshListener(dynamic_proxy(SwipeRefreshLayout.OnRefreshListener)):
        def __init__(self, interface):
            super().__init__()
            self._interface = interface

        def onRefresh(self):
            self._interface.on_refresh()


class DetailedList(Widget):
    def create(self):
        if SwipeRefreshLayout is None:  # pragma: no cover
            raise RuntimeError(
                "Unable to import SwipeRefreshLayout. Ensure that the AndroidX Swipe Refresh Layout "
                "widget package (androidx.swiperefreshlayout:swiperefreshlayout:1.1.0) "
                "is listed in your app's dependencies."
            )
        # get the selection color from the current theme
        attrs = [R.attr.colorBackground, R.attr.colorControlHighlight]
        typed_array = self._native_activity.obtainStyledAttributes(attrs)
        self.color_unselected = typed_array.getColor(0, 0)
        self.color_selected = typed_array.getColor(1, 0)
        typed_array.recycle()

        self.native = self._refresh_layout = SwipeRefreshLayout(self._native_activity)
        self._refresh_layout.setOnRefreshListener(OnRefreshListener(self.interface))

        self._scroll_view = ScrollView(self._native_activity)
        match_parent = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.MATCH_PARENT,
        )
        self._refresh_layout.addView(self._scroll_view, match_parent)

        self._linear_layout = LinearLayout(self._native_activity)
        self._linear_layout.setOrientation(LinearLayout.VERTICAL)
        self._scroll_view.addView(self._linear_layout, match_parent)

    def _load_data(self):
        self._selection = None
        self._linear_layout.removeAllViews()
        for i, row in enumerate(self.interface.data):
            self._make_row(self._linear_layout, i, row)

    def _make_row(self, container, i, row):
        # Create the foreground.
        row_view = RelativeLayout(self._native_activity)
        container.addView(row_view)
        row_view.setOnClickListener(DetailedListOnClickListener(self, i))
        row_view.setOnLongClickListener(DetailedListOnLongClickListener(self, i))
        row_height = self.scale_in(64)

        title, subtitle, icon = (
            getattr(row, attr, None) for attr in self.interface.accessors
        )

        # Add user-provided icon to layout.
        icon_image_view = ImageView(self._native_activity)
        if icon is not None:
            icon_image_view.setImageBitmap(icon._impl.native)
        icon_layout_params = RelativeLayout.LayoutParams(
            RelativeLayout.LayoutParams.WRAP_CONTENT,
            RelativeLayout.LayoutParams.WRAP_CONTENT,
        )
        icon_width = self.scale_in(48)
        icon_margin = self.scale_in(8)
        icon_layout_params.width = icon_width
        icon_layout_params.setMargins(icon_margin, 0, icon_margin, 0)
        icon_layout_params.height = row_height
        icon_image_view.setScaleType(ImageView.ScaleType.FIT_CENTER)
        row_view.addView(icon_image_view, icon_layout_params)

        # Create layout to show top_text and bottom_text.
        text_container = LinearLayout(self._native_activity)
        text_container_params = RelativeLayout.LayoutParams(
            RelativeLayout.LayoutParams.WRAP_CONTENT,
            RelativeLayout.LayoutParams.WRAP_CONTENT,
        )
        text_container_params.height = row_height
        text_container_params.setMargins(icon_width + (2 * icon_margin), 0, 0, 0)
        row_view.addView(text_container, text_container_params)
        text_container.setOrientation(LinearLayout.VERTICAL)
        text_container.setWeightSum(2.0)

        # Create top & bottom text; add them to layout.
        def get_string(value):
            if value is None:
                value = self.interface.missing_value
            return str(value)

        top_text = TextView(self._native_activity)
        top_text.setText(get_string(title))
        top_text.setTextSize(20.0)
        top_text.setTextColor(
            self._native_activity.getResources().getColor(R.color.black)
        )
        bottom_text = TextView(self._native_activity)
        bottom_text.setTextColor(
            self._native_activity.getResources().getColor(R.color.black)
        )
        bottom_text.setText(get_string(subtitle))
        bottom_text.setTextSize(16.0)
        top_text_params = LinearLayout.LayoutParams(
            RelativeLayout.LayoutParams.WRAP_CONTENT,
            RelativeLayout.LayoutParams.MATCH_PARENT,
        )
        top_text_params.weight = 1.0
        top_text.setGravity(Gravity.BOTTOM)
        text_container.addView(top_text, top_text_params)
        bottom_text_params = LinearLayout.LayoutParams(
            RelativeLayout.LayoutParams.WRAP_CONTENT,
            RelativeLayout.LayoutParams.MATCH_PARENT,
        )
        bottom_text_params.weight = 1.0
        bottom_text.setGravity(Gravity.TOP)
        bottom_text_params.gravity = Gravity.TOP
        text_container.addView(bottom_text, bottom_text_params)

    def _get_row(self, index):
        return self._linear_layout.getChildAt(index)

    def change_source(self, source):
        self._load_data()

    def after_on_refresh(self, widget, result):
        self._refresh_layout.setRefreshing(False)

    def insert(self, index, item):
        self._load_data()

    def change(self, item):
        self._load_data()

    def remove(self, index, item):
        self._load_data()

    def clear(self):
        self._load_data()

    def _clear_selection(self):
        if self._selection is not None:
            self._get_row(self._selection).setBackgroundColor(self.color_unselected)
            self._selection = None

    def _set_selection(self, index):
        self._clear_selection()
        self._get_row(index).setBackgroundColor(self.color_selected)
        self._selection = index

    def get_selection(self):
        return self._selection

    def set_primary_action_enabled(self, enabled):
        self._primary_action_enabled = enabled

    def set_secondary_action_enabled(self, enabled):
        self._secondary_action_enabled = enabled

    def set_refresh_enabled(self, enabled):
        self._refresh_layout.setEnabled(enabled)

    def scroll_to_row(self, row):
        row_obj = self._linear_layout.getChildAt(row)
        hit_rect = Rect()
        row_obj.getHitRect(hit_rect)
        self._scroll_view.requestChildRectangleOnScreen(
            self._linear_layout,
            hit_rect,
            True,  # Immediate, not animated
        )
