import warnings

import toga
from toga_web.libs import create_proxy

from .base import Widget


class TogaRow:
    def __init__(self, value):
        self.value = value

    # All paths return none as Icon is not implemented in web.
    def icon(self, attr):
        data = getattr(self.value, attr, None)
        if isinstance(data, tuple):
            if data[0] is not None:
                return None
            return None
        else:
            try:
                return None
            except AttributeError:
                return None

    def text(self, attr, missing_value):
        data = getattr(self.value, attr, None)

        if isinstance(data, toga.Widget):
            warnings.warn("Web does not support the use of widgets in cells")
            text = None
        elif isinstance(data, tuple):
            text = data[1]
        else:
            text = data

        if text is None:
            return missing_value

        return str(text)


class Table(Widget):
    def create(self):

        self.native = self._create_native_widget("table")

        self.table_header = self._create_native_widget("thead")
        self.native.appendChild(self.table_header)

        self.table_body = self._create_native_widget("tbody")
        self.native.appendChild(self.table_body)

    def change_source(self, source):
        self.selection = {}

        # remove old table data
        for row_child in list(self.table_body.children):
            for td_child in list(row_child.children):
                row_child.removeChild(td_child)
            self.table_body.removeChild(row_child)

        for row_child in list(self.table_header.children):
            for td_child in list(row_child.children):
                row_child.removeChild(td_child)
            self.table_header.removeChild(row_child)

        if source is not None:
            self._create_table_headers()

            for i, row in enumerate(source):
                self._create_table_row(row, i)

        self.refresh()

    def get_selection(self):
        selection = sorted(self.selection)
        if self.interface.multiple_select:
            return selection
        elif len(selection) == 0:
            return None
        else:
            return selection[0]

    def add_selection(self, index, table_row):
        self.selection[index] = table_row
        table_row.classList.add("selected")

    def remove_selection(self, index):
        table_row = self.selection.pop(index)
        table_row.classList.remove("selected")

    def clear_selection(self):
        for index in list(self.selection):
            self.remove_selection(index)

    def _create_table_headers(self):
        if self.interface.headings:
            headings = self.interface.headings
        else:
            headings = self.interface.accessors
        self.table_header_row = self._create_native_widget("tr")

        for heading in headings:
            th = self._create_native_widget("th", content=heading)
            self.table_header_row.appendChild(th)

        self.table_header.appendChild(self.table_header_row)

    def _create_table_row(self, item, index):
        row = TogaRow(item)
        values = []
        for accessor in self.interface.accessors:
            values.extend(
                [
                    # Removed icon accessor for now as not sure how to handle icon
                    # row.icon(accessor),
                    row.text(accessor, self.interface.missing_value),
                ]
            )
        tr = self._create_native_widget("tr")

        tr.addEventListener(
            "click", create_proxy(lambda event: self.dom_row_click(event, index, tr))
        )

        for value in values:
            td = self._create_native_widget("td", content=value)
            tr.appendChild(td)
        self.table_body.appendChild(tr)

    def dom_row_click(self, event, index, table_row):
        if index in self.selection:
            self.remove_selection(index)
        else:
            if not self.interface.multiple_select:
                self.clear_selection()
            self.add_selection(index, table_row)

    def insert(self, index, item):
        self.change_source(self.interface.data)

    def clear(self):
        self.change_source(self.interface.data)

    def change(self, item):
        self.change_source(self.interface.data)

    def remove(self, index, item):
        self.change_source(self.interface.data)

    def insert_column(self, index, heading, accessor):
        self.change_source(self.interface.data)

    def remove_column(self, accessor):
        self.change_source(self.interface.data)
