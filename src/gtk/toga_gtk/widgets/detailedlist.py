from ..libs import Gtk
from .base import Widget
from .internal.sourcetreemodel import SourceTreeModel
from .internal.detailedlistrenderers import IconTextRenderer


class DetailedList(Widget):
    """
    gtk DetailedList implementation.
    This is based on a Gtk.TreeView because the contents is still basic.
    Should the need arise for more complex contents (buttons on each row, etc.),
    we should use a Gtk.ListBox (see gtk3-demo).
    """

    def create(self):
        self.renderer = IconTextRenderer.from_style(self.interface)

        self.store = SourceTreeModel(self.renderer.row_columns(), is_tree=False)

        self.treeview = Gtk.TreeView(model=self.store)
        self.treeview.set_headers_visible(False)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self.gtk_on_select)

        self.renderer.create_columns(self.treeview)

        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface
        # same scrolling policies as in the tree widget
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        self.native.set_min_content_width(self.interface.MIN_WIDTH)
        self.native.set_min_content_height(self.interface.MIN_HEIGHT)

    def change_source(self, source):
        self.treeview.set_model(None)
        self.store.change_source(source)
        for i, node in enumerate(source):
            self.insert(i, node)

        self.treeview.set_model(self.store)

    def insert(self, index, item):
        self.store.insert(item)

    def change(self, item):
        self.store.change(item)

    def remove(self, item, index):
        self.store.remove(item, index)

    def clear(self):
        self.store.clear()

    def set_on_refresh(self, handler):
        pass

    def after_on_refresh(self):
        # No special handling required
        pass

    def get_selection(self):
        tree_model, tree_iter = self.selection.get_selected()
        if tree_iter:
            row = tree_model.get(tree_iter, 0)[0]
        else:
            row = None

        return row

    def set_on_select(self, handler):
        # No special handling required
        pass

    def set_on_delete(self, handler):
        pass

    def scroll_to_row(self, row):
        path = Gtk.TreePath.new_from_indices([row])
        self.treeview.scroll_to_cell(path)

    def gtk_on_select(self, selection):
        if self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()
            if tree_iter:
                node = tree_model.get(tree_iter, 0)[0]
            else:
                node = None
            # TODO See #682 DetailedList should have a _selection attribute + selection property like Tree
            # self.interface._selection = node
            self.interface.on_select(self.interface, row=node)
