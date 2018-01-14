from gi.repository import Gtk

from .base import Widget


class Tree(Widget):
    def create(self):
        self.store = Gtk.TreeStore(*[object] + [str for h in self.interface.headings])

        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.treeview = Gtk.TreeView(model=self.store)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self.on_select)

        for i, heading in enumerate(self.interface.headings):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=i + 1)
            self.treeview.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        self.native.set_min_content_width(200)
        self.native.set_min_content_height(200)

    def row_data(self, item):
        return [item] + [
            str(getattr(item, attr))
            for attr in self.interface._accessors
        ]

    def on_select(self, selection):
        if self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()
            if tree_iter:
                node = tree_model.get(tree_iter, 0)[0]
            else:
                node = None
            self.interface.on_select(None, node=node)

    def change_source(self, source):
        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None)

        self.store.clear()

        def append_children(data, parent=None):
            for i, node in enumerate(data):
                self.insert(parent, i, node)
                append_children(node, parent=node)

        append_children(self.interface.data, parent=None)

        self.treeview.set_model(self.store)

    def insert(self, parent, index, item, **kwargs):
        impl = self.store.insert(
            parent._impl[self] if parent else None,
            index,
            self.row_data(item)
        )
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
        # No special handling required
        pass

    def scroll_to_node(self, node):
        raise NotImplementedError
