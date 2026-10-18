from travertino.size import at_least

from toga.handlers import WeakrefCallable

from ..libs import GTK_VERSION, GdkPixbuf, Gio, GLib, GObject, Gtk, Pango
from .base import Widget
from .table import TogaRow


class TogaTreeRow(TogaRow):
    @GObject.Signal
    def updated(self):
        pass

    def __init__(self, value):
        super().__init__(value)
        self.children = Gio.ListStore.new(TogaTreeRow)
        self.expandable = value.can_have_children()


class Tree(Widget):
    def create(self):
        self.store = None

        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native_tree = Gtk.TreeView(model=self.store)
            self.native_tree.connect(
                "row-activated", WeakrefCallable(self.gtk_on_row_activated)
            )
            self.selection = self.native_tree.get_selection()
            if self.interface.multiple_select:
                self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)
            else:
                self.selection.set_mode(Gtk.SelectionMode.SINGLE)
            self.selection.connect("changed", WeakrefCallable(self.gtk_on_select))

            self._create_columns()
        else:  # pragma: no-cover-if-gtk3
            self._rows = {}
            self._expanded = set()
            self._syncing_expansion = False
            self._expansion_idle = None
            self.store = Gio.ListStore.new(TogaTreeRow)
            self.tree_model = Gtk.TreeListModel.new(
                self.store,
                False,
                False,
                lambda row: row.children if row.expandable else None,
            )
            self.tree_model.connect(
                "items-changed", WeakrefCallable(self.gtk_on_items_changed)
            )
            if self.interface.multiple_select:
                self.selection = Gtk.MultiSelection.new(self.tree_model)
            else:
                self.selection = Gtk.SingleSelection(
                    model=self.tree_model, autoselect=False, can_unselect=True
                )
            self.selection.connect(
                "selection-changed", WeakrefCallable(self.gtk_on_select)
            )
            self.native_tree = Gtk.ColumnView(model=self.selection)
            self.native_tree.connect("activate", WeakrefCallable(self.gtk_on_activate))
            self._create_gtk4_columns()

        self.native = Gtk.ScrolledWindow()
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            self.native.add(self.native_tree)
            self.native.set_min_content_width(200)
            self.native.set_min_content_height(200)
        else:  # pragma: no-cover-if-gtk3
            self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            self.native.set_child(self.native_tree)
            self.native.set_min_content_width(200)
            self.native.set_min_content_height(200)

    def _create_gtk4_columns(self):
        for column in list(self.native_tree.get_columns()):
            self.native_tree.remove_column(column)

        for index, toga_column in enumerate(self.interface._columns):
            factory = Gtk.SignalListItemFactory()
            factory.connect("setup", WeakrefCallable(self.gtk_setup_cell), index == 0)
            factory.connect("bind", WeakrefCallable(self.gtk_bind_cell), toga_column)
            factory.connect("unbind", WeakrefCallable(self.gtk_unbind_cell))
            column = Gtk.ColumnViewColumn(
                title=toga_column.heading or "",
                factory=factory,
                expand=True,
                resizable=True,
            )
            self.native_tree.append_column(column)

        # ColumnView exposes no show-headings property. Its first child is the
        # native header; hiding it leaves the row view and column model intact.
        self.native_tree.get_first_child().set_visible(self.interface._show_headings)

    def gtk_setup_cell(self, factory, item, first_column):
        cell = Gtk.Box(spacing=6)
        cell.icon = Gtk.Image(pixel_size=16)
        cell.text = Gtk.Label(xalign=0, hexpand=True, ellipsize=Pango.EllipsizeMode.END)
        cell.append(cell.icon)
        cell.append(cell.text)
        if first_column:
            expander = Gtk.TreeExpander(child=cell)
            expander.cell = cell
            item.set_child(expander)
        else:
            item.set_child(cell)

    def gtk_bind_cell(self, factory, item, column):
        child = item.get_child()
        tree_row = item.get_item()
        if isinstance(child, Gtk.TreeExpander):
            child.set_list_row(tree_row)
        cell = getattr(child, "cell", child)
        cell.row = tree_row.get_item()
        cell.column = column
        cell.handler = cell.row.connect(
            "updated", WeakrefCallable(self.gtk_update_cell), cell
        )
        self.gtk_update_cell(cell.row, cell)

    def gtk_update_cell(self, row, cell):
        cell.text.set_text(row.text(cell.column, self.interface.missing_value))
        icon = cell.column.icon(row.value)
        cell.icon.set_from_paintable(
            icon._impl.native().get_paintable() if icon else None
        )
        cell.icon.set_visible(icon is not None)

    def gtk_unbind_cell(self, factory, item):
        child = item.get_child()
        if isinstance(child, Gtk.TreeExpander):
            child.set_list_row(None)
        cell = getattr(child, "cell", child)
        cell.row.disconnect(cell.handler)
        cell.row = None

    def gtk_on_activate(self, view, position):
        self.interface.on_activate(node=self.tree_model[position].get_item().value)

    def _create_columns(self):
        self.native_tree.set_headers_visible(self.interface._show_headings)
        toga_columns = self.interface._columns

        for i, toga_column in enumerate(toga_columns):
            column = Gtk.TreeViewColumn(
                toga_column.heading if toga_column.heading else str(id(toga_column))
            )
            column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
            column.set_expand(True)
            column.set_resizable(True)
            column.set_min_width(16)

            icon = Gtk.CellRendererPixbuf()
            column.pack_start(icon, False)
            column.add_attribute(icon, "pixbuf", i * 2 + 1)

            value = Gtk.CellRendererText()
            column.pack_start(value, True)
            column.add_attribute(value, "text", i * 2 + 2)

            self.native_tree.append_column(column)

    def focus(self):
        self.native_tree.grab_focus()

    def gtk_on_select(self, selection, *args):
        self.interface.on_select()

    def gtk_on_row_activated(self, widget, path, column):
        node = self.store[path][0].value
        self.interface.on_activate(node=node)

    def change_source(self, source):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # Temporarily disconnecting the TreeStore improves performance for large
            # updates by deferring row rendering until the update is complete.
            self.native_tree.set_model(None)

            for column in self.native_tree.get_columns():
                self.native_tree.remove_column(column)
            self._create_columns()

            types = [TogaRow] + [GdkPixbuf.Pixbuf, str] * len(self.interface.columns)
            self.store = Gtk.TreeStore(*types)

            for i, row in enumerate(self.interface.data):
                self.source_insert(parent=None, index=i, item=row)

            self.native_tree.set_model(self.store)
            self.refresh()
        else:  # pragma: no-cover-if-gtk3
            self._create_gtk4_columns()
            self._rows.clear()
            self._expanded.clear()
            rows = [self.create_tree_row(node) for node in source]
            self.store.splice(0, self.store.get_n_items(), rows)
            self.refresh()

    def create_tree_row(self, node):
        row = TogaTreeRow(node)
        self._rows[node] = row
        for column in self.interface._columns:
            row.warn_widget(column)
        for child in node:
            row.children.append(self.create_tree_row(child))
        return row

    def gtk_on_items_changed(self, *args):
        if self._syncing_expansion:
            return
        self._syncing_expansion = True
        try:
            index = 0
            while index < self.tree_model.get_n_items():
                row = self.tree_model.get_row(index)
                if not getattr(row, "observed", False):
                    row.observed = True
                    row.connect(
                        "notify::expanded", WeakrefCallable(self.gtk_on_expanded)
                    )
                index += 1
        finally:
            self._syncing_expansion = False

    def gtk_on_expanded(self, row, _property):
        node = row.get_item().value
        if row.get_expanded():
            self._expanded.add(node)
            if self._expansion_idle is None:
                # Wait until GTK has finished notifying every observer about the
                # inserted rows before restoring descendant expansion state.
                self._expansion_idle = GLib.idle_add(
                    WeakrefCallable(self.restore_expansion)
                )
        else:
            self._expanded.discard(node)

    def restore_expansion(self):
        self._expansion_idle = None
        self.apply_expansion()
        return False

    def visible_row(self, node):
        for row in self.tree_model:
            if row.get_item().value is node:
                return row
        return None

    def apply_expansion(self):
        index = 0
        while index < self.tree_model.get_n_items():
            row = self.tree_model.get_row(index)
            if row.get_item().value in self._expanded:
                row.set_expanded(True)
            index += 1

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item, parent=None):
        import warnings

        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item, parent=parent)

    def source_insert(self, *, index, item, parent=None):
        if GTK_VERSION >= (4, 0, 0):
            store = self.store if parent is None else self._rows[parent].children
            store.insert(index, self.create_tree_row(item))
            if parent is not None and not self._rows[parent].expandable:
                self._rows[parent].expandable = True
                grandparent = parent._parent
                parent_store = (
                    self.store
                    if grandparent is None
                    else self._rows[grandparent].children
                )
                found, position = parent_store.find(self._rows[parent])
                if found:
                    parent_store.items_changed(position, 1, 1)
            return
        row = TogaRow(item)
        values = [row]
        for column in self.interface._columns:
            values.extend(
                [
                    row.icon(column),
                    row.text(column, self.interface.missing_value),
                ]
            )
            row.warn_widget(column)

        if parent is None:
            iter = None
        else:
            iter = parent._impl

        item._impl = self.store.insert(iter, index, values)

        for i, child in enumerate(item):
            self.source_insert(parent=item, index=i, item=child)

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def change(self, item):
        import warnings

        warnings.warn(
            "The change() method is deprecated. Use source_change() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_change(item=item)

    def source_change(self, *, item):
        if GTK_VERSION >= (4, 0, 0):
            row = self._rows[item]
            for column in self.interface._columns:
                row.warn_widget(column)
            row.emit("updated")
            return
        row = self.store[item._impl]
        for i, column in enumerate(self.interface._columns):
            row[i * 2 + 1] = row[0].icon(column)
            row[i * 2 + 2] = row[0].text(column, self.interface.missing_value)
            row[0].warn_widget(column)

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item, parent=None):
        import warnings

        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item, parent=parent)

    def source_remove(self, *, index, item, parent=None):
        if GTK_VERSION < (4, 0, 0):
            del self.store[item._impl]
            item._impl = None
        else:
            store = self.store if parent is None else self._rows[parent].children
            store.remove(index)
            self.forget_tree_row(item)

    def forget_tree_row(self, node):
        for child in node:
            self.forget_tree_row(child)
        self._rows.pop(node, None)
        self._expanded.discard(node)

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def clear(self):
        import warnings

        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
        if GTK_VERSION < (4, 0, 0):
            self.store.clear()
        else:
            self.store.remove_all()
            self._rows.clear()
            self._expanded.clear()

    def get_selection(self):
        if GTK_VERSION >= (4, 0, 0):
            if self.interface.multiple_select:
                selected = self.selection.get_selection()
                return [
                    self.tree_model[selected.get_nth(i)].get_item().value
                    for i in range(selected.get_size())
                ]
            row = self.selection.get_selected_item()
            return row.get_item().value if row is not None else None
        if self.interface.multiple_select:
            store, itrs = self.selection.get_selected_rows()
            return [store[itr][0].value for itr in itrs]
        else:
            store, iter = self.selection.get_selected()
            if iter is None:
                return None
            return store[iter][0].value

    def expand_node(self, node):
        if GTK_VERSION < (4, 0, 0):
            self.native_tree.expand_row(
                self.native_tree.get_model().get_path(node._impl), True
            )
        else:
            self.mark_expanded(node)
            self.apply_expansion()

    def mark_expanded(self, node):
        if len(node):
            self._expanded.add(node)
            for child in node:
                self.mark_expanded(child)

    def expand_all(self):
        if GTK_VERSION < (4, 0, 0):
            self.native_tree.expand_all()
        else:
            for node in self.interface.data:
                self.mark_expanded(node)
            self.apply_expansion()

    def collapse_node(self, node):
        if GTK_VERSION < (4, 0, 0):
            self.native_tree.collapse_row(
                self.native_tree.get_model().get_path(node._impl)
            )
        else:
            self._expanded.discard(node)
            row = self.visible_row(node)
            if row is not None:
                row.set_expanded(False)

    def collapse_all(self):
        if GTK_VERSION < (4, 0, 0):
            self.native_tree.collapse_all()
        else:
            self._expanded.clear()
            for node in self.interface.data:
                self.collapse_node(node)

    def insert_column(self, index, columns):
        # Adding/removing a column means completely rebuilding the ListStore
        self.change_source(self.interface.data)

    def remove_column(self, index):
        self.change_source(self.interface.data)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
