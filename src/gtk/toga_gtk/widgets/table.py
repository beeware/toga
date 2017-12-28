from gi.repository import Gtk

from .base import Widget


class Table(Widget):
    def create(self):
        self.store = Gtk.ListStore(*[object] + [str for h in self.interface.headings])

        # Create a table view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.treeview = Gtk.TreeView(model=self.store)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self.on_select)

        for i, heading in enumerate(self.interface.headings):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=i + 1)
            self.treeview.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        # self.native.set_min_content_width(200)
        # self.native.set_min_content_height(200)
        self.native.interface = self.interface

    def on_select(self, selection):
        if self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()
            if tree_iter:
                row = tree_model.get(tree_iter, 0)[0]
            else:
                row = None
            self.interface.on_select(None, row=row)

    def row_data(self, row):
        return [row] + [
            str(getattr(row, attr))
            for attr in self.interface._accessors
        ]

    def change_source(self, source):
        """
        Synchronize self.data with self.interface.data
        """

        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None) # temporarily disconnect the view

        self.store.clear()
        for i, row in enumerate(self.interface.data):
            self.insert(i, row)

        self.treeview.set_model(self.store)

    def insert(self, index, item):
        impl = self.store.insert(index, self.row_data(item))
        try:
            item._impl[self] = impl
        except AttributeError:
            item._impl = {self: impl}

    def change(self, item):
        self.store[item._impl[self]] = self.row_data(item)

    def remove(self, item):
        del self.store[item._impl[self]]
        del item._impl[self]

    def clear(self):
        self.store.clear()

    def set_on_select(self, handler):
        pass

    def scroll_to_row(self, row):
        raise NotImplementedError()
