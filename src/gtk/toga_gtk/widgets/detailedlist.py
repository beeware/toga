from ..libs import Gtk, Gio, GLib
from .base import Widget
from .internal.rows import TextIconRow

# Remove imports below after implementing DetailedList with
# Gtk.ListBox
from .internal.sourcetreemodel import SourceTreeModel
from .internal.detailedlistrenderers import IconTextRenderer


class DetailedListNew(Widget):
    """
    Gtk DetailedList implementation.
    Gtk.ListBox inside a Gtk.ScrolledWindow.
    The rows are Gtk.ListBoxRow and are kept inside a Gio.ListStore.
    toga.sources.ListSource is converted to Gtk.ListBoxRow in self.change_source.
    """
    def create(self):
        self.store = None

        self.list_box = Gtk.ListBox()

        self.native = Gtk.ScrolledWindow()
        self.native.add(self.list_box)
        self.native.interface = self.interface

      
    def change_source(self, source):
        if self.store is not None:
            self.store.remove_all()
        else:
            self.store = Gio.ListStore()
        for row in source:
            self.store.append(
                TextIconRow(row, self.interface))

        # Gtk.ListBox.bind_model() requires a function to convert
        # the objects in the store to presentation objects.
        # But the objects in the store are already what we want.
        # Thus the identity function.
        # ListStore only accepts GObjects so we can't put
        # toga.sources.Row in it.
        self.list_box.bind_model(self.store, lambda a: a)

    def insert(self, index, item):
        row = TextIconRow(item, self.interface)
        self.store.insert(index, row)
        self.list_box.show_all()

    def change(self, item):
        pass

    def remove(self, item):
        index = self._find(item)
        self.store.remove(index)
        
    def clear(self):
        self.store.remove_all()

    def set_on_refresh(self, handler):
        pass

    def after_on_refresh(self):
        # No special handling required
        pass

    def get_selection(self):
        pass

    def set_on_select(self, handler):
        # No special handling required
        pass

    def set_on_delete(self, handler):
        pass

    def scroll_to_row(self, row):
        list_box_row = self.store[row]
        
        # Wait for 'size-allocate' because we will need the
        # dimensions of the widget. At this point 
        # widget.size_request is already available but that's
        # only the requested size, not the size it will get.
        list_box_row.scroll_handler_id = list_box_row.connect(
            'size-allocate',
            lambda widget, gpointer: self._do_scroll_to_row(list_box_row) # We don't need 'wdiget' and 'gpointer'.
            )

    def gtk_on_select(self, selection):
        pass

    def _do_scroll_to_row(self, list_box_row):
        list_box_row.scroll_handler_id = None

        adj = self.list_box.get_adjustment()
        page_size = adj.get_page_size()

        # 'y' and 'height' are always valid because we are
        # being called after 'size-allocate'
        height = list_box_row.get_allocation().height
        _, y = list_box_row.translate_coordinates(self.list_box, 0, 0)
        adj.set_value(y - (page_size - height)/2)

    def _find(self, item):
        found, index = self.store.find_with_equal_func(
            item,
            lambda a, b: a == b.row)

        if not found:
            return -1
        else:
            return index


class DetailedListOld(Widget):
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


DetailedList = DetailedListNew
