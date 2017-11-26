from gi.repository import Gtk
from .base import Widget
from itertools import chain


class Tree(Widget):
    def create(self):
        self.store = Gtk.TreeStore(*[str for h in self.interface.headings])
        self.nodes = {}

        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.treeview = Gtk.TreeView(self.store)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self._on_select)

        for i, heading in enumerate(self.interface.headings):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=i)
            self.treeview.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        self.native.set_min_content_width(200)
        self.native.set_min_content_height(200)

    def row_data(self, item):
        return [
            str(getattr(item, attr))
            for attr in self.interface._accessors
        ]

    def set_impl(self, item, impl):
        try:
            item._impl[self] = impl
        except AttributeError:
            item._impl = {self: impl}

        self.nodes[impl] = item

    def _on_select(self, selection):
        if hasattr(self.interface, "_on_select") and self.interface.on_select:
            tree_model, impl = selection.get_selected()
            self.interface.on_select(None, row=self.nodes.get(impl, None))

    def change_source(self, source):
        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None)

        self.store.clear()

        def append_node(parent, root=False):
            parent_impl = None if root else parent._impl[self]
            for i, child_node in enumerate(parent):
                impl = self.store.append(parent_impl, self.row_data(child_node))
                self.set_impl(child_node, impl)
                append_node(child_node)

        append_node(self.interface.data, root=True)

        self.treeview.set_model(self.store)

    def insert(self, parent, index, item, **kwargs):
        impl = self.store.insert(
            parent._impl[self] if parent else None,
            index,
            self.row_data(item)
        )
        self.set_impl(item, impl)

    def change(self, item):
        self.store.set(
            item.parent._impl[self] if item.parent else None,
            *self.row_data(item)
        )

    def remove(self, item):
        self.store.remove(item._impl[self])
        del self.nodes[item_impl[self]]

    def clear(self):
        self.store.clear()

    def set_on_select(self, handler):
        pass
