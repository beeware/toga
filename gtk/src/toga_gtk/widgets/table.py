import warnings

from travertino.size import at_least

from ..libs import GTK_VERSION, GdkPixbuf, GObject, Gtk
from .base import Widget


class TogaRow(GObject.Object):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def icon(self, toga_column):
        icon = toga_column.icon(self.value)
        if icon is not None:
            return icon._impl.native(16)
        return None

    def text(self, toga_column, missing_value):
        return toga_column.text(self.value, missing_value)

    def warn_widget(self, toga_column):
        if toga_column.widget(self.value) is not None:
            warnings.warn(
                "GTK does not support the use of widgets in cells",
                stacklevel=2,
            )


class Table(Widget):
    def create(self):
        self.store = None
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native_table = Gtk.TreeView(model=self.store)
            self.native_table.connect("row-activated", self.gtk_on_row_activated)

            self.selection = self.native_table.get_selection()
            if self.interface.multiple_select:
                self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)
            else:
                self.selection.set_mode(Gtk.SelectionMode.SINGLE)
            self.selection.connect("changed", self.gtk_on_select)

            self._create_columns()
        else:  # pragma: no-cover-if-gtk3
            pass

        self.native = Gtk.ScrolledWindow()
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            self.native.add(self.native_table)
            self.native.set_min_content_width(200)
            self.native.set_min_content_height(200)
        else:  # pragma: no-cover-if-gtk3
            pass

    def _create_columns(self):
        self.native_table.set_headers_visible(self.interface._show_headings)
        toga_columns = self.interface._columns

        for i, toga_column in enumerate(toga_columns):
            column = Gtk.TreeViewColumn(
                toga_column.heading if toga_column.heading else str(id(toga_column))
            )
            column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
            column.set_expand(True)
            column.set_resizable(True)
            column.set_min_width(16)

            icon = Gtk.CellRendererPixbuf()
            column.pack_start(icon, False)
            column.add_attribute(icon, "pixbuf", i * 2 + 1)

            value = Gtk.CellRendererText()
            column.pack_start(value, True)
            column.add_attribute(value, "text", i * 2 + 2)

            self.native_table.append_column(column)

    def focus(self):
        self.native_table.grab_focus()

    def gtk_on_row_activated(self, widget, path, column):
        row = self.store[path][0].value
        self.interface.on_activate(row=row)

    def gtk_on_select(self, selection):
        self.interface.on_select()

    def change_source(self, source):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # Temporarily disconnecting the TreeStore improves performance for large
            # updates by deferring row rendering until the update is complete.
            self.native_table.set_model(None)

            for column in self.native_table.get_columns():
                self.native_table.remove_column(column)
            self._create_columns()

            types = [TogaRow] + [GdkPixbuf.Pixbuf, str] * len(self.interface._columns)
            self.store = Gtk.ListStore(*types)

            for i, row in enumerate(self.interface.data):
                self.insert(i, row)

            self.native_table.set_model(self.store)
            self.refresh()
        else:  # pragma: no-cover-if-gtk3
            pass

    def insert(self, index, item):
        row = TogaRow(item)
        values = [row]
        for column in self.interface._columns:
            values.extend(
                [
                    row.icon(column),
                    row.text(column, self.interface.missing_value),
                ]
            )
            # warn about widgets
            row.warn_widget(column)

        self.store.insert(index, values)

    def change(self, item):
        index = self.interface.data.index(item)
        row = self.store[index]
        for i, column in enumerate(self.interface._columns):
            row[i * 2 + 1] = row[0].icon(column)
            row[i * 2 + 2] = row[0].text(column, self.interface.missing_value)
            row[0].warn_widget(column)

    def remove(self, index, item):
        del self.store[index]

    def clear(self):
        self.store.clear()

    def get_selection(self):
        if self.interface.multiple_select:
            store, itrs = self.selection.get_selected_rows()
            return [self.interface.data.index(store[itr][0].value) for itr in itrs]
        else:
            store, iter = self.selection.get_selected()
            if iter is None:
                return None
            return self.interface.data.index(store[iter][0].value)

    def scroll_to_row(self, row):
        # Core API guarantees row exists, and there's > 1 row.
        n_rows = len(self.interface.data)
        pos = row / n_rows * self.native.get_vadjustment().get_upper()
        self.native.get_vadjustment().set_value(pos)

    def insert_column(self, index, heading, accessor):
        # Adding/removing a column means completely rebuilding the ListStore
        self.change_source(self.interface.data)

    def remove_column(self, accessor):
        self.change_source(self.interface.data)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
