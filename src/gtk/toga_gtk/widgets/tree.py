from gi.repository import Gtk

from .base import Widget


class Tree(Widget):
    def create(self):
        self.store = Gtk.TreeStore(*[object] + [str for h in self.interface.headings])

        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.treeview = Gtk.TreeView(self.store)
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

    # TODO: Remove this function once a consistent API exists for
    # checking if a TreeSource OR Node has children.
    def node_has_children(self, parent):
        return (
            hasattr(parent, '_children') and parent._children) or (
            hasattr(parent, '_roots') and parent._roots)

    def on_select(self, selection):
        if hasattr(self.interface, "on_select") and self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()
            row = tree_model.get(tree_iter, 0)[0]
            self.interface.on_select(None, row=row)

    def change_source(self, source):
        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None)

        self.store.clear()

        def append_node(parent):
            for i, child_node in enumerate(parent):
                self.insert(parent, i, child_node)
                append_node(child_node)

        append_node(self.interface.data)

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
        pass
