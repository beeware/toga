from travertino.size import at_least

from ..libs.activity import MainActivity
from ..libs.android import R__attr
from ..libs.android.graphics import Typeface
from ..libs.android.util import TypedValue
from ..libs.android.view import Gravity, OnClickListener, View__MeasureSpec
from ..libs.android.widget import (
    HorizontalScrollView,
    LinearLayout,
    LinearLayout__LayoutParams,
    ScrollView,
    TableLayout,
    TableLayout__Layoutparams,
    TableRow,
    TableRow__Layoutparams,
    TextView
)
from .base import Widget


class TogaOnClickListener(OnClickListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onClick(self, view):
        tr_id = view.getId()
        row = self.impl.interface.data[tr_id]
        if self.impl.interface.multiple_select:
            if tr_id in self.impl.selection:
                self.impl.selection.pop(tr_id)
                view.setBackgroundColor(self.impl.color_unselected)
            else:
                self.impl.selection[tr_id] = row
                view.setBackgroundColor(self.impl.color_selected)
        else:
            self.impl.clear_selection()
            self.impl.selection[tr_id] = row
            view.setBackgroundColor(self.impl.color_selected)
        if self.impl.interface.on_select:
            self.impl.interface.on_select(self.impl.interface, row=row)


class Table(Widget):
    table_layout = None
    color_selected = None
    color_unselected = None
    selection = {}
    _deleted_column = None
    _font_impl = None

    def create(self):
        # get the selection color from the current theme
        current_theme = MainActivity.singletonThis.getApplication().getTheme()
        attrs = [R__attr.colorBackground, R__attr.colorControlHighlight]
        typed_array = current_theme.obtainStyledAttributes(attrs)
        self.color_unselected = typed_array.getColor(0, 0)
        self.color_selected = typed_array.getColor(1, 0)
        typed_array.recycle()

        parent = LinearLayout(self._native_activity)
        parent.setOrientation(LinearLayout.VERTICAL)
        parent_layout_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT
        )
        parent_layout_params.gravity = Gravity.TOP
        parent.setLayoutParams(parent_layout_params)
        vscroll_view = ScrollView(self._native_activity)
        # add vertical scroll view
        vscroll_view_layout_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT
        )
        vscroll_view_layout_params.gravity = Gravity.TOP
        self.table_layout = TableLayout(MainActivity.singletonThis)
        table_layout_params = TableLayout__Layoutparams(
            TableLayout__Layoutparams.MATCH_PARENT,
            TableLayout__Layoutparams.WRAP_CONTENT
        )
        # add horizontal scroll view
        hscroll_view = HorizontalScrollView(self._native_activity)
        hscroll_view_layout_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT
        )
        hscroll_view_layout_params.gravity = Gravity.LEFT
        vscroll_view.addView(hscroll_view, hscroll_view_layout_params)

        # add table layout to scrollbox
        self.table_layout.setLayoutParams(table_layout_params)
        hscroll_view.addView(self.table_layout)
        # add scroll box to parent layout
        parent.addView(vscroll_view, vscroll_view_layout_params)
        self.native = parent
        if self.interface.data is not None:
            self.change_source(self.interface.data)

    def change_source(self, source):
        self.selection = {}
        self.table_layout.removeAllViews()
        if source is not None:
            self.table_layout.addView(self.create_table_header())
            for row_index in range(len(source)):
                table_row = self.create_table_row(row_index)
                self.table_layout.addView(table_row)
        self.table_layout.invalidate()

    def clear_selection(self):
        for i in range(self.table_layout.getChildCount()):
            row = self.table_layout.getChildAt(i)
            row.setBackgroundColor(self.color_unselected)
        self.selection = {}

    def create_table_header(self):
        table_row = TableRow(MainActivity.singletonThis)
        table_row_params = TableRow__Layoutparams(
            TableRow__Layoutparams.MATCH_PARENT,
            TableRow__Layoutparams.WRAP_CONTENT
        )
        table_row.setLayoutParams(table_row_params)
        for col_index in range(len(self.interface._accessors)):
            if self.interface._accessors[col_index] == self._deleted_column:
                continue
            text_view = TextView(MainActivity.singletonThis)
            text_view.setText(self.interface.headings[col_index])
            if self._font_impl:
                text_view.setTextSize(TypedValue.COMPLEX_UNIT_SP, self._font_impl.get_size())
                text_view.setTypeface(self._font_impl.get_typeface(), Typeface.BOLD)
            else:
                text_view.setTypeface(text_view.getTypeface(), Typeface.BOLD)
            text_view_params = TableRow__Layoutparams(
                TableRow__Layoutparams.MATCH_PARENT,
                TableRow__Layoutparams.WRAP_CONTENT
            )
            text_view_params.setMargins(10, 5, 10, 5)  # left, top, right, bottom
            text_view_params.gravity = Gravity.START
            text_view.setLayoutParams(text_view_params)
            table_row.addView(text_view)
        return table_row

    def create_table_row(self, row_index):
        table_row = TableRow(MainActivity.singletonThis)
        table_row_params = TableRow__Layoutparams(
            TableRow__Layoutparams.MATCH_PARENT,
            TableRow__Layoutparams.WRAP_CONTENT
        )
        table_row.setLayoutParams(table_row_params)
        table_row.setClickable(True)
        table_row.setOnClickListener(TogaOnClickListener(impl=self))
        table_row.setId(row_index)
        for col_index in range(len(self.interface._accessors)):
            if self.interface._accessors[col_index] == self._deleted_column:
                continue
            text_view = TextView(MainActivity.singletonThis)
            text_view.setText(self.get_data_value(row_index, col_index))
            if self._font_impl:
                text_view.setTextSize(TypedValue.COMPLEX_UNIT_SP, self._font_impl.get_size())
                text_view.setTypeface(self._font_impl.get_typeface(), self._font_impl.get_style())
            text_view_params = TableRow__Layoutparams(
                TableRow__Layoutparams.MATCH_PARENT,
                TableRow__Layoutparams.WRAP_CONTENT
            )
            text_view_params.setMargins(10, 5, 10, 5)  # left, top, right, bottom
            text_view_params.gravity = Gravity.START
            text_view.setLayoutParams(text_view_params)
            table_row.addView(text_view)
        return table_row

    def get_data_value(self, row_index, col_index):
        if self.interface.data is None or self.interface._accessors is None:
            return None
        row_object = self.interface.data[row_index]
        value = getattr(row_object, self.interface._accessors[col_index])
        return value

    def get_selection(self):
        selection = []
        for row_index in range(len(self.interface.data)):
            if row_index in self.selection:
                selection.append(self.selection[row_index])
        if len(selection) == 0:
            selection = None
        elif not self.interface.multiple_select:
            selection = selection[0]
        return selection

    # data listener method
    def insert(self, index, item):
        self.change_source(self.interface.data)

    # data listener method
    def clear(self):
        self.change_source(self.interface.data)

    def change(self, item):
        self.interface.factory.not_implemented('Table.change()')

    # data listener method
    def remove(self, item, index):
        self.change_source(self.interface.data)

    def scroll_to_row(self, row):
        pass

    def set_on_select(self, handler):
        pass

    def set_on_double_click(self, handler):
        self.interface.factory.not_implemented('Table.set_on_double_click()')

    def add_column(self, heading, accessor):
        self.change_source(self.interface.data)

    def remove_column(self, accessor):
        self._deleted_column = accessor
        self.change_source(self.interface.data)
        self._deleted_column = None

    def set_font(self, font):
        if font:
            self._font_impl = font.bind(self.interface.factory)
        if self.interface.data is not None:
            self.change_source(self.interface.data)

    def rehint(self):
        # Android can crash when rendering some widgets until
        # they have their layout params set. Guard for that case.
        if not self.native.getLayoutParams():
            return

        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = at_least(self.native.getMeasuredHeight())
