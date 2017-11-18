from gi.repository import Gtk
from .base import Widget
from toga.sources.base import Row


class Table(Widget):
    def create(self):
        self.store = Gtk.ListStore(*[str for h in self.interface.headings])
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
            tree_model, tree_iter = selection.get_selected()

            if tree_iter:
                tree_path = tree_model.get_path(tree_iter)
                row = tree_path.get_indices()[0]
            else:
                row = None
            self.interface.on_select(None, row=row)

    def _refresh(self):
        """
        Synchronize self.data with self.interface.data
        """

        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None) # temporarily disconnect the view

        self.store.clear()
        for row in self.interface.data:
            self.store.append(self._row_items(row))

        self.treeview.set_model(self.store)

    # TODO: The interface should provide the row index instead of using this
    # method to access a private property
    def _row_index(self, row: Row):
        return self.interface.data._data.index(row)

    # TODO: The interface should provide the row list items instead of using
    # this method to access a private property
    def _row_items(self, row: Row):
        return [getattr(row, attr) for attr in self.interface._accessors]

    def change_source(self, source):
        self._refresh()

    def insert(self, index, item: Row):
        self.store.insert(index, self._row_items(row))

    def change(self, item: Row):
        self.store[self._row_index(row)] = self._row_items(row)

    def remove(self, index, item: Row):
        self.store.remove(self.store.get_iter((index,)))

    def clear(self):
        self.store.clear()

    def set_on_select(self, handler):
        pass
