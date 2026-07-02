import warnings

from textual._context import active_app
from textual.widgets import DataTable as TextualDataTable
from travertino.size import at_least

from .base import Widget


class TogaDataTable(TextualDataTable):
    def __init__(self, impl):
        super().__init__(
            show_header=impl.interface.show_headings,
            show_row_labels=False,
            cursor_type="row",
        )
        self.interface = impl.interface
        self.impl = impl

    def on_mount(self):
        self.impl.on_mount()

    def on_data_table_row_selected(self, event: TextualDataTable.RowSelected):
        if event.data_table is self:
            self.impl.select_row(event.cursor_row)


class Table(Widget):
    ROW_HEIGHT = 24

    def create(self):
        self.native = TogaDataTable(self)
        self._rows = []
        self._row_keys = []
        self._column_keys = []
        self._selection = [] if self.interface.multiple_select else None
        self._next_row_key = 0
        self._next_column_key = 0
        self._scroll_position = 0
        self._viewport_height = self.interface._MIN_HEIGHT
        self._table_width = self.interface._MIN_WIDTH
        self._column_widths = []
        self._has_manual_column_widths = False

    def _native_is_ready(self):
        return self.native.is_attached and self.interface.app is not None

    def _ensure_active_app(self):
        if self.interface.app is not None:
            active_app.set(self.interface.app._impl.native)

    def _new_row_key(self):
        self._next_row_key += 1
        return f"toga-row-{self._next_row_key}"

    def _new_column_key(self):
        self._next_column_key += 1
        return f"toga-column-{self._next_column_key}"

    @property
    def max_scroll_position(self):
        return max(0, len(self._rows) * self.ROW_HEIGHT - self._viewport_height)

    def _clamp_state(self):
        if self.interface.multiple_select:
            self._selection = [
                row for row in self._selection if 0 <= row < len(self._rows)
            ]
        elif self._selection is not None and self._selection >= len(self._rows):
            self._selection = None

        self._scroll_position = min(self._scroll_position, self.max_scroll_position)

    def cell_text(self, row, column):
        if column.widget(row) is not None:
            warnings.warn(
                "Textual does not support the use of widgets in cells",
                stacklevel=2,
            )
            return self.interface.missing_value

        return column.text(row, self.interface.missing_value)

    def row_cells(self, row):
        return [self.cell_text(row, column) for column in self.interface._columns]

    def _default_column_widths(self):
        count = len(self.interface._columns)
        if count == 0:
            return []

        width = max(self._table_width, count)
        base_width, remainder = divmod(round(width), count)
        return [base_width + (1 if index < remainder else 0) for index in range(count)]

    def _ensure_column_widths(self):
        count = len(self.interface._columns)
        if count == 0:
            self._column_widths = []
        elif len(self._column_widths) != count or not self._has_manual_column_widths:
            self._column_widths = self._default_column_widths()

    def _apply_column_widths(self):
        if not self._native_is_ready():
            return

        self._ensure_active_app()
        self._ensure_column_widths()
        for column_key, width in zip(
            self._column_keys,
            self._column_widths,
            strict=False,
        ):
            column = self.native.columns[column_key]
            column.width = max(1, self.scale_in_horizontal(round(width)))
            column.auto_width = False
        self.native.refresh(layout=True)

    def _resize_column_widths(self, width):
        if not self._column_widths or not self._has_manual_column_widths:
            self._column_widths = self._default_column_widths()
            return

        old_width = sum(self._column_widths)
        if old_width <= 0:
            self._column_widths = self._default_column_widths()
        else:
            scale = width / old_width
            self._column_widths = [
                max(1, round(column_width * scale))
                for column_width in self._column_widths
            ]

    def _add_native_column(self, column):
        column_key = self.native.add_column(
            column.heading,
            key=self._new_column_key(),
        )
        self._column_keys.append(column_key)

    def _rebuild_native_columns(self):
        if not self._native_is_ready():
            return

        self._ensure_active_app()
        self.native.clear(columns=True)
        self._column_keys = []

        for column in self.interface._columns:
            self._add_native_column(column)

        self._apply_column_widths()
        self._rebuild_native_rows()

    def _add_native_row(self, row):
        row_key = self.native.add_row(*self.row_cells(row), key=self._new_row_key())
        self._row_keys.append(row_key)

    def _rebuild_native_rows(self):
        if not self._native_is_ready():
            return

        self._ensure_active_app()
        self.native.clear(columns=False)
        self._row_keys = []

        for row in self._rows:
            self._add_native_row(row)

        self._sync_native_selection()

    def _sync_native_selection(self):
        if not self._native_is_ready():
            return

        if self.interface.multiple_select:
            if self._selection:
                self.native.move_cursor(
                    row=self._selection[-1],
                    column=0,
                    animate=False,
                )
        elif self._selection is not None:
            self.native.move_cursor(row=self._selection, column=0, animate=False)

    def on_mount(self):
        self._rebuild_native_columns()

    def focus(self):
        self.native.app.set_focus(self.native)

    def change_source(self, source):
        self._rows = list(source)
        self._clamp_state()
        self._rebuild_native_rows()

    # Listener Protocol implementation

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item):
        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item)

    def source_insert(self, *, index, item):
        self._rows.insert(index, item)
        if self.interface.multiple_select:
            self._selection = [
                row + 1 if index <= row else row for row in self._selection
            ]
        elif self._selection is not None and index <= self._selection:
            self._selection += 1
        self._clamp_state()

        if self._native_is_ready():
            if index == len(self._rows) - 1:
                self._ensure_active_app()
                self._add_native_row(item)
                self._sync_native_selection()
            else:
                self._rebuild_native_rows()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def change(self, item):
        warnings.warn(
            "The change() method is deprecated. Use source_change() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_change(item=item)

    def source_change(self, *, item):
        try:
            index = self.interface.data.index(item)
        except ValueError:
            self.change_source(self.interface.data)
            return

        self._rows[index] = item

        if self._native_is_ready():
            self._ensure_active_app()
            row_key = self._row_keys[index]
            for column_key, value in zip(
                self._column_keys,
                self.row_cells(item),
                strict=False,
            ):
                self.native.update_cell(row_key, column_key, value)

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item):
        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item)

    def source_remove(self, *, index, item):
        self._rows.pop(index)
        if self.interface.multiple_select:
            selection = []
            for row in self._selection:
                if row < index:
                    selection.append(row)
                elif row > index:
                    selection.append(row - 1)
            self._selection = selection
        elif self._selection == index:
            self._selection = None
        elif self._selection is not None and index < self._selection:
            self._selection -= 1
        self._clamp_state()

        if self._native_is_ready():
            self._ensure_active_app()
            self.native.remove_row(self._row_keys.pop(index))
            self._sync_native_selection()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def clear(self):
        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
        self._rows = []
        self._row_keys = []
        self._selection = [] if self.interface.multiple_select else None
        self._clamp_state()

        if self._native_is_ready():
            self._ensure_active_app()
            self.native.clear(columns=False)

    def get_selection(self):
        return self._selection

    def select_row(self, row, add=False):
        if not 0 <= row < len(self._rows):
            return

        if self.interface.multiple_select:
            if add:
                if row in self._selection:
                    self._selection.remove(row)
                else:
                    self._selection.append(row)
                    self._selection.sort()
            else:
                self._selection = [row]
        else:
            self._selection = row

        self._sync_native_selection()
        self.interface.on_select()

    def activate_row(self, row):
        if 0 <= row < len(self._rows):
            self.select_row(row)
            self.interface.on_activate(row=self.interface.data[row])

    def scroll_to_row(self, row):
        self._scroll_position = min(
            max(row * self.ROW_HEIGHT, 0),
            self.max_scroll_position,
        )
        self.native.scroll_y = self.scale_in_vertical(self._scroll_position)

    def insert_column(self, index, column):
        self._has_manual_column_widths = False
        self._ensure_column_widths()
        self._rebuild_native_columns()

    def remove_column(self, index):
        self._has_manual_column_widths = False
        self._ensure_column_widths()
        self._rebuild_native_columns()

    def column_width(self, index):
        self._ensure_column_widths()
        return self._column_widths[index]

    def resize_column(self, index, width):
        self._ensure_column_widths()
        self._has_manual_column_widths = True
        self._column_widths[index] = round(width)
        self._apply_column_widths()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        old_width = self._table_width
        self._table_width = width
        self._viewport_height = self.scale_out_vertical(self.scale_in_vertical(height))
        self._scroll_position = min(self._scroll_position, self.max_scroll_position)

        if self._has_manual_column_widths:
            self._resize_column_widths(width)
        elif old_width != width:
            self._column_widths = self._default_column_widths()
        self._apply_column_widths()

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.scale_in_horizontal(self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            self.scale_in_vertical(self.interface._MIN_HEIGHT)
        )
