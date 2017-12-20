from gi.repository import Gtk

from .base import Widget


class Tree(Widget):
    def create(self):
        self.store = Gtk.TreeStore(*[str for h in self.interface.headings])

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

    # Gtk.TreeIter cannot be compared with __eq__ !!!
    def compare_tree_iters(self, one, two):
        return self.store.get_path(one) == self.store.get_path(two)

    # TODO: Remove this function once a consistent API exists for
    # checking if a TreeSource OR Node has children.
    def node_has_children(self, parent):
        return (
            hasattr(parent, '_children') and parent._children) or (
            hasattr(parent, '_roots') and parent._roots)

    def get_node(self, tree_iter):
        def iterate_tree(node, root=False):
            yield node
            if self.node_has_children(node):
                for child in node:
                    yield from iterate_tree(child)

        for node in iterate_tree(self.interface.data, root=True):
            if self.get_impl(node) and tree_iter:
                if self.compare_tree_iters(tree_iter, self.get_impl(node)):
                    return node

    def set_impl(self, node, impl):
        node._impl = getattr(node, '_impl', {})
        node._impl[self] = impl

    def del_impl(self, node):
        if hasattr(node, '_impl'):
            del node._impl[self]

    def get_impl(self, node):
        if hasattr(node, '_impl'):
            return node._impl.get(self, None)

    def _on_select(self, selection):
        if hasattr(self.interface, "_on_select") and self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()
            row = self.get_node(tree_iter)
            self.interface.on_select(None, row=row)

    def change_source(self, source):
        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None)

        self.store.clear()

        def append_node(parent, root=False):
            if self.node_has_children(parent):
                for i, child_node in enumerate(parent):
                    self.insert(parent, i, child_node)
                    append_node(child_node)

        append_node(self.interface.data, root=True)

        self.treeview.set_model(self.store)

    def insert(self, parent, index, item, **kwargs):
        impl = self.store.insert(
            self.get_impl(parent),
            index,
            self.row_data(item)
        )
        self.set_impl(item, impl)

    def change(self, item):
        self.store[self.get_impl(item)] = self.row_data(item)

    def remove(self, item):
        del self.store[self.get_impl(item)]
        self.del_impl(item)

    def clear(self):
        self.store.clear()

    def set_on_select(self, handler):
        pass
