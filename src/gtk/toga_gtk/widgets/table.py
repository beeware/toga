from gi.repository import Gtk

from .tree import Tree


class Table(Tree):

    def on_select(self, selection):
        if hasattr(self.interface, "on_select") and self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()
            if tree_iter:
                row = tree_model.get(tree_iter, 0)[0]
            else:
                row = None
            self.interface.on_select(None, row=row)

    def change_source(self, source):
        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None)

        self.store.clear()

        for i, row in enumerate(self.interface.data):
            self.insert(i, row)

        self.treeview.set_model(self.store)

    def insert(self, index, item, **kwargs):
        super().insert(None, index, item, **kwargs)

    # =================================
    # UNCHANGED METHODS (inherited from Tree)
    # They are included here only to satisfy the implementation tests, which
    # do not currently check for inherited methods.

    def create(self):
        super().create()

    def scroll_to_row(self, row):
        super().scroll_to_row(row)

    def change(self, item):
        super().change(item)

    def remove(self, item):
        super().remove(item)

    def clear(self):
        super().clear()

    def set_on_select(self, handler):
        super().set_on_select(handler)
