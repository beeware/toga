import toga

from ..libs import Gtk
from .base import Widget
from .internal.sourcetreemodel import SourceTreeModel


class Tree(Widget):
    def create(self):
        # Tree is reused for table, where it's a ListSource, not a tree
        # so check here if the actual widget is a Tree or a Table.
        # It can't be based on the source, since it determines flags
        # and GtkTreeModel.flags is not allowed to change after creation
        is_tree = isinstance(self.interface, toga.Tree)
        self.store = SourceTreeModel(
            [{"type": str, "attr": a} for a in self.interface._accessors],
            is_tree=is_tree,
        )

        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.treeview = Gtk.TreeView(model=self.store)
        self.selection = self.treeview.get_selection()
        if self.interface.multiple_select:
            self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        else:
            self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self.gtk_on_select)

        for i, heading in enumerate(self.interface.headings):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=i + 1)
            self.treeview.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        self.native.set_min_content_width(200)
        self.native.set_min_content_height(200)

    def gtk_on_select(self, selection):
        if self.interface.on_select:
            if self.interface.multiple_select:
                tree_model, tree_path = selection.get_selected_rows()
                if tree_path:
                    tree_iter = tree_model.get_iter(tree_path[-1])
                else:
                    tree_iter = None
            else:
                tree_model, tree_iter = selection.get_selected()

            # Covert the tree iter into the actual node.
            if tree_iter:
                node = tree_model.get(tree_iter, 0)[0]
            else:
                node = None
            self.interface.on_select(None, node=node)

    def change_source(self, source):
        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None)

        self.store.change_source(source)

        def append_children(data, parent=None):
            if data.can_have_children():
                for i, node in enumerate(data):
                    self.insert(parent, i, node)
                    append_children(node, parent=node)

        append_children(source, parent=None)

        self.treeview.set_model(self.store)

    def insert(self, parent, index, item, **kwargs):
        self.store.insert(item)

    def change(self, item):
        self.store.change(item)

    def remove(self, item, index, parent):
        self.store.remove(item, index=index, parent=parent)

    def clear(self):
        self.store.clear()

    def get_selection(self):
        if self.interface.multiple_select:
            tree_model, tree_paths = self.selection.get_selected_rows()
            return [
                tree_model.get(tree_model.get_iter(path), 0)[0] for path in tree_paths
            ]
        else:
            tree_model, tree_iter = self.selection.get_selected()
            if tree_iter:
                row = tree_model.get(tree_iter, 0)[0]
            else:
                row = None

        return row

    def set_on_select(self, handler):
        # No special handling required
        pass

    def set_on_double_click(self, handler):
        self.interface.factory.not_implemented("Tree.set_on_double_click()")

    def scroll_to_node(self, node):
        path = self.store.path_to_node(node)
        self.treeview.scroll_to_cell(path)
