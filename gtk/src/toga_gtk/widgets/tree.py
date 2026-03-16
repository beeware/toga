from travertino.size import at_least

from toga.handlers import WeakrefCallable

from ..libs import GTK_VERSION, GdkPixbuf, Gtk
from .base import Widget
from .table import TogaRow


class Tree(Widget):
    def create(self):
        self.store = None

        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.native_tree = Gtk.TreeView(model=self.store)
        self.native_tree.connect(
            "row-activated", WeakrefCallable(self.gtk_on_row_activated)
        )

        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.selection = self.native_tree.get_selection()
            if self.interface.multiple_select:
                self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)
            else:
                self.selection.set_mode(Gtk.SelectionMode.SINGLE)
            self.selection.connect("changed", WeakrefCallable(self.gtk_on_select))

            self._create_columns()
        else:  # pragma: no-cover-if-gtk3
            pass

        self.native = Gtk.ScrolledWindow()
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            self.native.add(self.native_tree)
            self.native.set_min_content_width(200)
            self.native.set_min_content_height(200)
        else:  # pragma: no-cover-if-gtk3
            pass

    def _create_columns(self):
        self.native_tree.set_headers_visible(self.interface._show_headings)
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

            self.native_tree.append_column(column)

    def focus(self):
        self.native_tree.grab_focus()

    def gtk_on_select(self, selection):
        self.interface.on_select()

    def gtk_on_row_activated(self, widget, path, column):
        node = self.store[path][0].value
        self.interface.on_activate(node=node)

    def change_source(self, source):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # Temporarily disconnecting the TreeStore improves performance for large
            # updates by deferring row rendering until the update is complete.
            self.native_tree.set_model(None)

            for column in self.native_tree.get_columns():
                self.native_tree.remove_column(column)
            self._create_columns()

            types = [TogaRow] + [GdkPixbuf.Pixbuf, str] * len(self.interface.columns)
            self.store = Gtk.TreeStore(*types)

            for i, row in enumerate(self.interface.data):
                self.insert(parent=None, index=i, item=row)

            self.native_tree.set_model(self.store)
            self.refresh()
        else:  # pragma: no-cover-if-gtk3
            pass

    def insert(self, index, item, parent=None):
        row = TogaRow(item)
        values = [row]
        for column in self.interface._columns:
            values.extend(
                [
                    row.icon(column),
                    row.text(column, self.interface.missing_value),
                ]
            )
            row.warn_widget(column)

        if parent is None:
            iter = None
        else:
            iter = parent._impl

        item._impl = self.store.insert(iter, index, values)

        for i, child in enumerate(item):
            self.insert(parent=item, index=i, item=child)

    def change(self, item):
        row = self.store[item._impl]
        for i, column in enumerate(self.interface._columns):
            row[i * 2 + 1] = row[0].icon(column)
            row[i * 2 + 2] = row[0].text(column, self.interface.missing_value)
            row[0].warn_widget(column)

    def remove(self, index, item, parent=None):
        del self.store[item._impl]
        item._impl = None

    def clear(self):
        self.store.clear()

    def get_selection(self):
        if self.interface.multiple_select:
            store, itrs = self.selection.get_selected_rows()
            return [store[itr][0].value for itr in itrs]
        else:
            store, iter = self.selection.get_selected()
            if iter is None:
                return None
            return store[iter][0].value

    def expand_node(self, node):
        self.native_tree.expand_row(
            self.native_tree.get_model().get_path(node._impl), True
        )

    def expand_all(self):
        self.native_tree.expand_all()

    def collapse_node(self, node):
        self.native_tree.collapse_row(self.native_tree.get_model().get_path(node._impl))

    def collapse_all(self):
        self.native_tree.collapse_all()

    def insert_column(self, index, columns):
        # Adding/removing a column means completely rebuilding the ListStore
        self.change_source(self.interface.data)

    def remove_column(self, index):
        self.change_source(self.interface.data)

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
            self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
        else:  # pragma: no-cover-if-gtk3
            pass
