from .tree import Tree


class Table(Tree):
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

            # Covert the tree iter into the actual row.
            if tree_iter:
                row = tree_model.get(tree_iter, 0)[0]
            else:
                row = None
            self.interface.on_select(None, row=row)

    def change_source(self, source):
        # Temporarily disconnecting the TreeStore improves performance for large
        # updates by deferring row rendering until the update is complete.
        self.treeview.set_model(None)

        self.store.change_source(source)

        for i, row in enumerate(self.interface.data):
            self.insert(i, row)

        self.treeview.set_model(self.store)

    def insert(self, index, item):
        super().insert(None, index, item)

    def scroll_to_row(self, row):
        return NotImplementedError

    def add_column(self, heading, accessor):
        return NotImplementedError

    def remove_column(self, accessor):
        return NotImplementedError

    # =================================
    # UNCHANGED METHODS (inherited from Tree)
    # They are included here only to satisfy the implementation tests, which
    # do not currently check for inherited methods.

    def create(self):
        super().create()

    def change(self, item):
        super().change(item)

    def remove(self, index, item):
        super().remove(item, index=index, parent=None)

    def clear(self):
        super().clear()

    def get_selection(self):
        return super().get_selection()

    def set_on_select(self, handler):
        super().set_on_select(handler)

    def set_on_double_click(self, handler):
        self.interface.factory.not_implemented("Table.set_on_double_click()")
