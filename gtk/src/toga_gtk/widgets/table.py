import warnings

from travertino.size import at_least

from toga.handlers import WeakrefCallable

from ..libs import GTK_VERSION, GdkPixbuf, Gio, GObject, Gtk, Pango
from .base import Widget


class TogaRow(GObject.Object):
    @GObject.Signal
    def changed(self):
        pass

    def __init__(self, value):
        super().__init__()
        self.value = value

    def icon(self, toga_column):
        icon = toga_column.icon(self.value)
        if icon is not None:
            return icon._impl.native(16)
        return None

    def text(self, toga_column, missing_value):
        return toga_column.text(self.value, missing_value)

    def warn_widget(self, toga_column):
        if toga_column.widget(self.value) is not None:
            warnings.warn(
                "GTK does not support the use of widgets in cells",
                stacklevel=2,
            )


class Table(Widget):
    def create(self):
        self.store = None
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native_table = Gtk.TreeView(model=self.store)
            self.native_table.connect(
                "row-activated", WeakrefCallable(self.gtk_on_row_activated)
            )

            self.selection = self.native_table.get_selection()
            if self.interface.multiple_select:
                self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)
            else:
                self.selection.set_mode(Gtk.SelectionMode.SINGLE)
            self.selection.connect("changed", WeakrefCallable(self.gtk_on_select))

            self._create_columns()
        else:  # pragma: no-cover-if-gtk3
            self.store = Gio.ListStore.new(TogaRow)
            if self.interface.multiple_select:
                self.selection = Gtk.MultiSelection.new(self.store)
            else:
                self.selection = Gtk.SingleSelection(
                    model=self.store, autoselect=False, can_unselect=True
                )
            self.selection.connect(
                "selection-changed", WeakrefCallable(self.gtk_on_select)
            )
            self.native_table = Gtk.ColumnView(model=self.selection)
            self.native_table.connect("activate", WeakrefCallable(self.gtk_on_activate))
            self._create_gtk4_columns()

        self.native = Gtk.ScrolledWindow()
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            self.native.add(self.native_table)
            self.native.set_min_content_width(200)
            self.native.set_min_content_height(200)
        else:  # pragma: no-cover-if-gtk3
            self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            self.native.set_child(self.native_table)
            self.native.set_min_content_width(200)
            self.native.set_min_content_height(200)

    def _create_gtk4_columns(self):
        existing = {
            column.interface: column for column in self.native_table.get_columns()
        }
        for column in existing.values():
            self.native_table.remove_column(column)

        for toga_column in self.interface._columns:
            column = existing.get(toga_column)
            if column is None:
                factory = Gtk.SignalListItemFactory()
                factory.connect("setup", WeakrefCallable(self.gtk_setup_cell))
                factory.connect(
                    "bind", WeakrefCallable(self.gtk_bind_cell), toga_column
                )
                factory.connect("unbind", WeakrefCallable(self.gtk_unbind_cell))
                column = Gtk.ColumnViewColumn(
                    title=toga_column.heading or "",
                    factory=factory,
                    expand=True,
                    resizable=True,
                )
                column.interface = toga_column
            self.native_table.append_column(column)

        # ColumnView exposes no show-headings property. Its first child is the
        # native header; hiding it leaves the row view and column model intact.
        self.native_table.get_first_child().set_visible(self.interface._show_headings)

    def gtk_setup_cell(self, factory, item):
        cell = Gtk.Box(spacing=6)
        cell.icon = Gtk.Image(pixel_size=16)
        cell.text = Gtk.Label(xalign=0, hexpand=True, ellipsize=Pango.EllipsizeMode.END)
        cell.append(cell.icon)
        cell.append(cell.text)
        item.set_child(cell)

    def gtk_bind_cell(self, factory, item, column):
        cell = item.get_child()
        cell.row = item.get_item()
        cell.column = column
        cell.handler = cell.row.connect(
            "changed", WeakrefCallable(self.gtk_update_cell), cell
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
        cell = item.get_child()
        cell.row.disconnect(cell.handler)
        cell.row = None

    def gtk_on_activate(self, view, position):
        self.interface.on_activate(row=self.store[position].value)

    def _create_columns(self):
        self.native_table.set_headers_visible(self.interface._show_headings)
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

            # Preserve a reference to the accessor for the column
            column.interface = toga_column

            self.native_table.append_column(column)

    def focus(self):
        self.native_table.grab_focus()

    def set_bounds(self, x, y, width, height):
        if GTK_VERSION >= (4, 0, 0) and self.native.get_width() != width:
            columns = list(self.native_table.get_columns())
            if any(column.get_fixed_width() >= 0 for column in columns):
                # After a user resizes a column, preserve the resulting proportions
                # when the whole table changes size. ColumnView only exposes the
                # requested fixed width; the header widgets have the actual widths.
                header = self.native_table.get_first_child().get_first_child()
                widths = []
                while header is not None:
                    widths.append(header.get_width())
                    header = header.get_next_sibling()
                total = sum(widths)
                if total:
                    for column, old_width in zip(columns, widths, strict=True):
                        column.set_fixed_width(
                            max(16, round(old_width * width / total))
                        )
        super().set_bounds(x, y, width, height)

    def gtk_on_row_activated(self, widget, path, column):
        row = self.store[path][0].value
        self.interface.on_activate(row=row)

    def gtk_on_select(self, selection, *args):
        self.interface.on_select()

    def change_source(self, source):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # Temporarily disconnecting the TreeStore improves performance for large
            # updates by deferring row rendering until the update is complete.
            self.native_table.set_model(None)

            # Preserve widths when columns are re-created.
            existing_columns = self.native_table.get_columns()
            preserved_widths = {
                column.interface: column.get_width() for column in existing_columns
            }

            for column in existing_columns:
                self.native_table.remove_column(column)

            self._create_columns()

            for column in self.native_table.get_columns():
                try:
                    width = preserved_widths[column.interface]
                    if width > 0:
                        column.set_fixed_width(width)
                except KeyError:
                    # It's a new or unknown column
                    pass

            types = [TogaRow] + [GdkPixbuf.Pixbuf, str] * len(self.interface._columns)
            self.store = Gtk.ListStore(*types)

            for i, row in enumerate(self.interface.data):
                self.source_insert(index=i, item=row)

            self.native_table.set_model(self.store)
            self.refresh()
        else:  # pragma: no-cover-if-gtk3
            self._create_gtk4_columns()
            rows = [TogaRow(item) for item in source]
            for row in rows:
                for column in self.interface._columns:
                    row.warn_widget(column)
            self.store.splice(0, self.store.get_n_items(), rows)
            self.refresh()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item):
        import warnings

        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item)

    def source_insert(self, *, index, item):
        row = TogaRow(item)
        if GTK_VERSION >= (4, 0, 0):
            for column in self.interface._columns:
                row.warn_widget(column)
            self.store.insert(index, row)
            return
        values = [row]
        for column in self.interface._columns:
            values.extend(
                [
                    row.icon(column),
                    row.text(column, self.interface.missing_value),
                ]
            )
            # warn about widgets
            row.warn_widget(column)

        self.store.insert(index, values)

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
        index = self.interface.data.index(item)
        row = self.store[index]
        if GTK_VERSION >= (4, 0, 0):
            for column in self.interface._columns:
                row.warn_widget(column)
            row.emit("changed")
            return
        for i, column in enumerate(self.interface._columns):
            row[i * 2 + 1] = row[0].icon(column)
            row[i * 2 + 2] = row[0].text(column, self.interface.missing_value)
            row[0].warn_widget(column)

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item):
        import warnings

        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item)

    def source_remove(self, *, index, item):
        if GTK_VERSION < (4, 0, 0):
            del self.store[index]
        else:
            self.store.remove(index)

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

    def get_selection(self):
        if GTK_VERSION >= (4, 0, 0):
            if self.interface.multiple_select:
                selected = self.selection.get_selection()
                return [selected.get_nth(i) for i in range(selected.get_size())]
            index = self.selection.get_selected()
            return None if index == Gtk.INVALID_LIST_POSITION else index
        if self.interface.multiple_select:
            store, itrs = self.selection.get_selected_rows()
            return [self.interface.data.index(store[itr][0].value) for itr in itrs]
        else:
            store, iter = self.selection.get_selected()
            if iter is None:
                return None
            return self.interface.data.index(store[iter][0].value)

    def scroll_to_row(self, row):
        # Core API guarantees row exists, and there's > 1 row.
        n_rows = len(self.interface.data)
        pos = row / n_rows * self.native.get_vadjustment().get_upper()
        self.native.get_vadjustment().set_value(pos)

    def insert_column(self, index, column):
        # Adding/removing a column means completely rebuilding the ListStore
        self.change_source(self.interface.data)

    def remove_column(self, accessor):
        self.change_source(self.interface.data)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
