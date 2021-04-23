import toga
from toga.constants import ON, OFF, MIXED

from ..libs import Gtk, Gdk
from .base import Widget
from .internal.sourcetreemodel import SourceTreeModel


class Tree(Widget):
    def create(self):
        # Tree is reused for table, where it's a ListSource, not a tree
        # so check here if the actual widget is a Tree or a Table.
        # It can't be based on the source, since it determines flags
        # and GtkTreeModel.flags is not allowed to change after creation
        is_tree = isinstance(self.interface, toga.Tree)
        self.store = SourceTreeModel(is_tree)

        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self.treeview = Gtk.TreeView(model=self.store)
        self.selection = self.treeview.get_selection()
        if self.interface.multiple_select:
            self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        else:
            self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self.gtk_on_select)

        for column in self.interface.columns:
            self.treeview.append_column(column._impl.native)

        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.set_shadow_type(Gtk.ShadowType.IN)
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

        self._update_columns()

        self.treeview.set_model(self.store)

    def _update_columns(self):

        # Gtk renderer requires the index of the data in the source
        # However, our interface does not guarantee that the accessor actually
        # exists in the source. We therefore update the indices when the source changes.

        for column in self.interface.columns:
            gtk_column = column._impl.native
            gtk_column.clear()  # remove all existing renderers and mappings

            if column.icon:
                renderer = Gtk.CellRendererPixbuf()
                gtk_column.pack_start(renderer, False)
                gtk_column.set_cell_data_func(renderer, self._set_icon)

            if column.checked_state:
                renderer = Gtk.CellRendererToggle()
                renderer.connect("toggled", self.gtk_on_toggled, column)
                renderer.set_alignment(0, 0)
                gtk_column.pack_start(renderer, False)
                gtk_column.set_cell_data_func(renderer, self._set_toggle)

            if column.text:
                renderer = Gtk.CellRendererText()
                renderer.connect("edited", self.gtk_on_edited, column)
                gtk_column.pack_start(renderer, True)
                gtk_column.set_cell_data_func(renderer, self._set_text)

    def gtk_on_edited(self, renderer, path, new_text, column):
        iter_ = self.store.get_iter(path)
        node = self.store.get_value(iter_, 0)
        column.set_data_for_node(node, "text", new_text)

    def gtk_on_toggled(self, renderer, path, column):
        iter_ = self.store.get_iter(path)
        node = self.store.get_value(iter_, 0)
        old_checked_state = column.get_data_for_node(node, "checked_state")
        column.set_data_for_node(node, "checked_state", int(not old_checked_state))

    def _set_icon(self, col, cell, model, iter_, user_data):
        node = model.get_value(iter_, 0)

        icon = col.interface.get_data_for_node(node, "icon")

        # bind icon and draw in hi-dpi on cairo surface
        pixbuf = icon.bind(self.interface.factory).native_32.get_pixbuf()
        surface = Gdk.cairo_surface_create_from_pixbuf(
            pixbuf, 0, self.native.get_window()
        )

        cell.set_property("surface", surface)

    def _set_toggle(self, col, cell, model, iter_, user_data):
        node = model.get_value(iter_, 0)
        checked_state = col.interface.get_data_for_node(node, "checked_state")

        if checked_state in (ON, OFF):
            cell.set_property("active", bool(checked_state))
        cell.set_property("inconsistent", checked_state == MIXED)
        cell.set_property("activatable", True)

    def _set_text(self, col, cell, model, iter_, user_data):
        node = model.get_value(iter_, 0)
        text = col.interface.get_data_for_node(node, "text")

        cell.set_property("text", text)
        cell.set_property("editable", col.interface.editable)

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
        self.interface.factory.not_implemented('Tree.set_on_double_click()')

    def scroll_to_node(self, node):
        path = self.store.path_to_node(node)
        self.treeview.scroll_to_cell(path)
