import warnings

from textual._context import active_app
from textual.widgets import (
    Label as TextualLabel,
    ListItem as TextualListItem,
    ListView as TextualListView,
)
from travertino.size import at_least

from .base import Widget


class DetailedListItem(TextualListItem):
    def __init__(self, impl, row):
        self.label = TextualLabel()
        super().__init__(self.label)
        self.update(impl, row)

    def update(self, impl, row):
        self.row = row
        self.title = impl.row_text(row, 0)
        self.subtitle = impl.row_text(row, 1)
        self.icon = getattr(row, impl.interface.accessors[2], None)
        self.label.update(f"{self.title}\n{self.subtitle}")


class TogaListView(TextualListView):
    def __init__(self, impl):
        super().__init__(initial_index=None)
        self.interface = impl.interface
        self.impl = impl

    def on_mount(self):
        self.impl.on_mount()

    def on_list_view_selected(self, event: TextualListView.Selected):
        self.impl.select_item(event.item)


class DetailedList(Widget):
    ROW_HEIGHT = 48

    def create(self):
        self.native = TogaListView(self)
        self._source = None
        self._items = []
        self._selection = None
        self._scroll_position = 0
        self._viewport_height = self.interface._MIN_HEIGHT
        self._native_operation = None
        self.primary_action_enabled = False
        self.secondary_action_enabled = False
        self.refresh_enabled = False

    def row_text(self, row, accessor_index):
        value = getattr(row, self.interface.accessors[accessor_index], None)
        return self.interface.missing_value if value is None else str(value)

    def _clamp_state(self):
        if self._selection is not None and self._selection >= len(self._items):
            self._selection = None
        self._scroll_position = min(self._scroll_position, self.max_scroll_position)

    def _build_items(self):
        self._items = [DetailedListItem(self, row) for row in self.interface.data]
        self._clamp_state()

    @property
    def max_scroll_position(self):
        return max(0, len(self._items) * self.ROW_HEIGHT - self._viewport_height)

    def _native_is_ready(self):
        return self.native.is_attached and self.interface.app is not None

    def _ensure_active_app(self):
        if self.interface.app is not None:
            active_app.set(self.interface.app._impl.native)

    def _queue_native_operation(self, operation):
        previous = self._native_operation

        async def perform_operation():
            if previous is not None:
                await previous
            await operation()

        self._native_operation = self.interface.app._impl.track_dom_operation(
            perform_operation()
        )

    async def _replace_native_items(self, items):
        self._ensure_active_app()
        if self.native.children:
            await self.native.clear()
        if items:
            await self.native.extend(items)
        self.native.index = self._selection

    async def _insert_native_item(self, index, item):
        self._ensure_active_app()
        await self.native.insert(index, [item])
        self.native.index = self._selection

    async def _remove_native_item(self, index):
        self._ensure_active_app()
        await self.native.pop(index)
        self.native.index = self._selection

    async def _clear_native_items(self):
        self._ensure_active_app()
        if self.native.children:
            await self.native.clear()

    def _sync_native_items(self):
        if self._native_is_ready():
            self._queue_native_operation(
                lambda: self._replace_native_items(self._items.copy())
            )

    def on_mount(self):
        self._sync_native_items()

    def change_source(self, source):
        self._source = source
        self._build_items()
        self._sync_native_items()

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
        item_impl = DetailedListItem(self, item)
        self._items.insert(index, item_impl)
        if self._selection is not None and index <= self._selection:
            self._selection += 1
        self._clamp_state()

        if self._native_is_ready():
            self._queue_native_operation(
                lambda: self._insert_native_item(index, item_impl)
            )

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
            self._build_items()
            self._sync_native_items()
        else:
            self._items[index].update(self, item)

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
        self._items.pop(index)
        if self._selection == index:
            self._selection = None
        elif self._selection is not None and index < self._selection:
            self._selection -= 1
        self._clamp_state()

        if self._native_is_ready():
            self._queue_native_operation(lambda: self._remove_native_item(index))

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
        self._items = []
        self._selection = None
        self._clamp_state()

        if self._native_is_ready():
            self._queue_native_operation(self._clear_native_items)

    def get_selection(self):
        return self._selection

    def select_item(self, item):
        try:
            self._selection = self._items.index(item)
        except ValueError:
            self._selection = None
        self.interface.on_select()

    def select_row(self, row):
        if 0 <= row < len(self._items):
            self._selection = row
            self.native.index = row
            self.interface.on_select()

    def deselect(self):
        self._selection = None
        self.native.index = None

    def scroll_to_row(self, row):
        self._scroll_position = min(
            max(row * self.ROW_HEIGHT, 0),
            self.max_scroll_position,
        )
        self.native.scroll_y = self.scale_in_vertical(self._scroll_position)

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled

    def set_refresh_enabled(self, enabled):
        self.refresh_enabled = enabled

    def after_on_refresh(self, widget, result):
        pass

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self._viewport_height = self.scale_out_vertical(self.scale_in_vertical(height))
        self._scroll_position = min(self._scroll_position, self.max_scroll_position)

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.scale_in_horizontal(self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            self.scale_in_vertical(self.interface._MIN_HEIGHT)
        )
