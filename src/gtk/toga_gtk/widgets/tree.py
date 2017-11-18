from gi.repository import Gtk
from .base import Widget
from itertools import chain


class Tree(Widget):
    def create(self):
        self.store = Gtk.TreeStore(*[str for h in self.interface.headings])
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.treeview = Gtk.TreeView(self.store)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self._on_select)

        for heading in self.interface.headings:
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=0)
            self.treeview.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        self.native.set_min_content_width(200)
        self.native.set_min_content_height(200)

    # TODO: The interface (or data source?) should provide the row list items instead of using
    # this method to access a private property.

    # toga.sources.base.Row -> list (row's items, converted to string)
    def _row_items(self, row):
        return [str(getattr(row, attr)) for attr in self.interface._accessors]

    # sources.base.Node -> int (node's index)
    def _node_index(self, node):
        def _parent(node):
            return getattr(node, "_parent", None) or getattr(node, "_source", None)

        for i, sibling in enumerate(_parent(node)):
            if sibling is node:
                return i

    # sources.base.Node -> tuple (node's path)
    def _node_path(self, node):
        def f(node, path=[]):
            if hasattr(node, "_parent"):
                path.insert(0, self._node_index(node))
                return f(node._parent, path)
            else:
                return path

        return tuple(f(node))

    # sources.base.Node -> Gtk.TreeIter
    def _node_iter(self, node):
        if hasattr(node, "_parent"):
            return self.store.get_iter(self._node_path(node))
        else:
            return None

    # tuple (node's path) -> sources.base.Node
    def _get_node(self, path: tuple):
        lpath = list(path)
        lpath.reverse() # [level2, level1, level0]

        def _children(node):
            return getattr(node, "_children", None) or getattr(node, "_roots", None)

        def f(node, path):
            if _children(node) and lpath:
                index = lpath.pop()
                return f(node[index], lpath)
            else:
                return node

        return f(self.interface.data, lpath)

    def _on_select(self, selection):
        if hasattr(self.interface, "_on_select") and self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()

            if tree_iter:
                tree_path = tree_model.get_path(tree_iter)
                path = tree_path.get_indices()
            else:
                path = None

            self.interface.on_select(None, node=self._get_node(path))

    def _refresh(self):

        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None)

        self.store.clear()

        def append_node(parent_node, it):
            for i, child_node in enumerate(parent_node):
                self.store.append(it, self._row_items(child_node))
                it = self.store.iter_nth_child(it, i)
                append_node(child_node, it)

        append_node(self.interface.data, None)

        self.treeview.set_model(self.store)

    def change_source(self, source):
        self._refresh()

    def insert(self, item):
        self.store.insert(
            self._node_iter(item._parent),
            index,
            self._row_items(item)
        )

    def change(self, item):
        self.store.set(
            self._node_iter(item._parent),
            # `TreeModel.set()` expects *flat* column-value pairs
            *chain.from_iterable(enumerate(self._row_items(node))
        )

    def remove(self, item):
        self.store.remove(self._node_iter(item))

    def clear(self):
        self.store.clear()

    def set_on_select(self, handler):
        pass
