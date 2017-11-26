from gi.repository import Gtk
from .base import Widget


class Table(Widget):
    def create(self):
        self.store = Gtk.ListStore(*[str for h in self.interface.headings])
        self.rows = {}

        # Create a table view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.treeview = Gtk.TreeView(self.store)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self._on_select)

        for i, heading in enumerate(self.interface.headings):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=i)
            self.treeview.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        self.native.set_min_content_width(200)
        self.native.set_min_content_height(200)
        self.native.interface = self.interface

    def _on_select(self, selection):
        if hasattr(self.interface, "_on_select") and self.interface.on_select:
            tree_model, impl = selection.get_selected()
            self.interface.on_select(None, row=self.rows.get(impl, None))

    def row_data(self, row):
        return [
            str(getattr(row, attr))
            for attr in self.interface._accessors
        ]

    def set_impl(self, item, impl):
        try:
            item._impl[self] = impl
        except AttributeError:
            item._impl = {self: impl}

        self.rows[impl] = item

    def change_source(self, source):
        """
        Synchronize self.data with self.interface.data
        """

        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None) # temporarily disconnect the view

        self.store.clear()
        for item in self.interface.data:
            impl = self.store.append(self.row_data(item))
            self.set_impl(item, impl)

        self.treeview.set_model(self.store)

    def insert(self, index, item):
        impl = self.store.insert(index, self.row_data(item))
        self.set_impl(item, impl)

    def change(self, item):
        item._impl[self] = self.row_data(item)

    def remove(self, item):
        self.store.remove(item._impl[self])
        del self.rows[item._impl[self]]

    def clear(self):
        self.store.clear()

    def set_on_select(self, handler):
        pass
