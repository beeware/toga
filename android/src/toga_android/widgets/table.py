from warnings import warn

from android import R
from android.graphics import Color, Rect, Typeface
from android.view import Gravity, View
from android.widget import LinearLayout, ScrollView, TableLayout, TableRow, TextView
from java import dynamic_proxy

import toga

from .base import Widget
from .label import set_textview_font


class TogaOnClickListener(dynamic_proxy(View.OnClickListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onClick(self, view):
        tr_id = view.getId()
        if self.impl.interface.multiple_select:
            if tr_id in self.impl.selection:
                self.impl.remove_selection(tr_id)
            else:
                self.impl.add_selection(tr_id, view)
        else:
            self.impl.clear_selection()
            self.impl.add_selection(tr_id, view)
        self.impl.interface.on_select()


class TogaOnLongClickListener(dynamic_proxy(View.OnLongClickListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onLongClick(self, view):
        self.impl.clear_selection()
        index = view.getId()
        self.impl.add_selection(index, view)
        self.impl.interface.on_select()
        self.impl.interface.on_activate(row=self.impl.interface.data[index])
        return True


class Table(Widget):
    table_layout = None
    color_selected = None
    _font_impl = None

    def create(self):
        # get the selection color from the current theme
        attrs = [R.attr.colorControlHighlight]
        typed_array = self._native_activity.obtainStyledAttributes(attrs)
        self.color_selected = typed_array.getColor(0, 0)
        typed_array.recycle()

        # add vertical scroll view
        self.native = vscroll_view = ScrollView(self._native_activity)
        vscroll_view_layout_params = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.MATCH_PARENT,
        )
        vscroll_view_layout_params.gravity = Gravity.TOP
        vscroll_view.setLayoutParams(vscroll_view_layout_params)

        self.table_layout = TableLayout(self._native_activity)
        table_layout_params = TableLayout.LayoutParams(
            TableLayout.LayoutParams.MATCH_PARENT,
            TableLayout.LayoutParams.WRAP_CONTENT,
        )

        # add table layout to scrollbox
        self.table_layout.setLayoutParams(table_layout_params)
        vscroll_view.addView(self.table_layout)

    def change_source(self, source):
        self.selection = {}
        self.table_layout.removeAllViews()

        # StretchAllColumns mode causes a divide by zero error if there are no columns.
        self.table_layout.setStretchAllColumns(bool(self.interface.accessors))

        if source is not None:
            if self.interface.headings is not None:
                self.table_layout.addView(self.create_table_header())
            for row_index in range(len(source)):
                table_row = self.create_table_row(row_index)
                self.table_layout.addView(table_row)
        self.table_layout.invalidate()

    def add_selection(self, index, table_row):
        self.selection[index] = table_row
        table_row.setBackgroundColor(self.color_selected)

    def remove_selection(self, index):
        table_row = self.selection.pop(index)
        table_row.setBackgroundColor(Color.TRANSPARENT)

    def clear_selection(self):
        for index in list(self.selection):
            self.remove_selection(index)

    def create_table_header(self):
        table_row = TableRow(self._native_activity)
        table_row_params = TableRow.LayoutParams(
            TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.WRAP_CONTENT
        )
        table_row.setLayoutParams(table_row_params)
        for col_index in range(len(self.interface._accessors)):
            text_view = TextView(self._native_activity)
            text_view.setText(self.interface.headings[col_index])
            set_textview_font(
                text_view,
                self._font_impl,
                text_view.getTypeface(),
                text_view.getTextSize(),
            )
            text_view.setTypeface(
                Typeface.create(
                    text_view.getTypeface(),
                    text_view.getTypeface().getStyle() | Typeface.BOLD,
                )
            )
            text_view_params = TableRow.LayoutParams(
                TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.WRAP_CONTENT
            )
            text_view_params.setMargins(10, 5, 10, 5)  # left, top, right, bottom
            text_view_params.gravity = Gravity.START
            text_view.setLayoutParams(text_view_params)
            table_row.addView(text_view)
        return table_row

    def create_table_row(self, row_index):
        table_row = TableRow(self._native_activity)
        table_row_params = TableRow.LayoutParams(
            TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.WRAP_CONTENT
        )
        table_row.setLayoutParams(table_row_params)
        table_row.setClickable(True)
        table_row.setOnClickListener(TogaOnClickListener(impl=self))
        table_row.setLongClickable(True)
        table_row.setOnLongClickListener(TogaOnLongClickListener(impl=self))
        table_row.setId(row_index)
        for col_index in range(len(self.interface._accessors)):
            text_view = TextView(self._native_activity)
            text_view.setText(self.get_data_value(row_index, col_index))
            set_textview_font(
                text_view,
                self._font_impl,
                text_view.getTypeface(),
                text_view.getTextSize(),
            )
            text_view_params = TableRow.LayoutParams(
                TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.WRAP_CONTENT
            )
            text_view_params.setMargins(10, 5, 10, 5)  # left, top, right, bottom
            text_view_params.gravity = Gravity.START
            text_view.setLayoutParams(text_view_params)
            table_row.addView(text_view)
        return table_row

    def get_data_value(self, row_index, col_index):
        value = getattr(
            self.interface.data[row_index],
            self.interface._accessors[col_index],
            None,
        )
        if isinstance(value, toga.Widget):
            warn("This backend does not support the use of widgets in cells")
            value = None
        if isinstance(value, tuple):  # TODO: support icons
            value = value[1]
        if value is None:
            value = self.interface.missing_value
        return str(value)

    def get_selection(self):
        selection = sorted(self.selection)
        if self.interface.multiple_select:
            return selection
        elif len(selection) == 0:
            return None
        else:
            return selection[0]

    def insert(self, index, item):
        self.change_source(self.interface.data)

    def clear(self):
        self.change_source(self.interface.data)

    def change(self, item):
        self.change_source(self.interface.data)

    def remove(self, index, item):
        self.change_source(self.interface.data)

    def scroll_to_row(self, index):
        if (index != 0) and (self.interface.headings is not None):
            index += 1
        table_row = self.table_layout.getChildAt(index)
        table_row.requestRectangleOnScreen(
            Rect(0, 0, 0, table_row.getHeight()),
            True,  # Immediate, not animated
        )

    def insert_column(self, index, heading, accessor):
        self.change_source(self.interface.data)

    def remove_column(self, index):
        self.change_source(self.interface.data)

    def set_font(self, font):
        self._font_impl = font._impl
        self.change_source(self.interface.data)
