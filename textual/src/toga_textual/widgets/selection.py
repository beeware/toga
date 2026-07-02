import warnings

from textual.widgets import Select as TextualSelect
from travertino.size import at_least

from .base import Widget


class TogaSelect(TextualSelect):
    def __init__(self, impl):
        super().__init__([], prompt="", allow_blank=True)
        self.interface = impl.interface
        self.impl = impl

    def on_mount(self):
        self.impl.apply_native_state()

    def on_select_changed(self, event: TextualSelect.Changed) -> None:
        self.impl.on_select_changed(event.value)


class Selection(Widget):
    def create(self):
        self.native = TogaSelect(self)
        self._selected_item = None
        self._programmatic_native_values = []

    @property
    def items(self):
        return getattr(self.interface, "_items", [])

    @property
    def titles(self):
        return [self.interface._title_for_item(item) for item in self.items]

    @property
    def _options(self):
        return [(title, index) for index, title in enumerate(self.titles)]

    @property
    def intrinsic_width(self):
        return max(
            [
                self.scale_in_horizontal(self.interface._MIN_WIDTH),
                *(len(title) + 4 for title in self.titles),
            ]
        )

    def _selected_index(self):
        if self._selected_item is None:
            return None

        try:
            return self.items.index(self._selected_item)
        except ValueError:
            self._selected_item = None
            return None

    def _native_value(self, index):
        return TextualSelect.BLANK if index is None else index

    def apply_native_state(self):
        if not self.native.is_attached:
            return

        target = self._native_value(self._selected_index())
        if self.native.value != TextualSelect.BLANK:
            self._programmatic_native_values.append(TextualSelect.BLANK)
        if target != TextualSelect.BLANK:
            self._programmatic_native_values.append(target)

        self.native.set_options(self._options)
        self.native.value = target

    def _sync_options(self):
        self.apply_native_state()
        self.interface.refresh()

    def _select_item(self, item, notify):
        self._selected_item = item
        self._sync_options()
        if notify:
            self.interface.on_change()

    def on_select_changed(self, value):
        if value in self._programmatic_native_values:
            self._programmatic_native_values.remove(value)
            return

        item = None if value == TextualSelect.BLANK else self.items[value]
        self._select_item(item, notify=True)

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
        self._sync_options()

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
        notify = self._selected_item is None
        if notify:
            self._selected_item = self.items[0]
        self._sync_options()
        if notify:
            self.interface.on_change()

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
        notify = self._selected_item is item
        if notify:
            try:
                self._selected_item = self.items[0]
            except IndexError:
                self._selected_item = None
        self._sync_options()
        if notify:
            self.interface.on_change()

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
        notify = self._selected_item is not None
        self._selected_item = None
        self._sync_options()
        if notify:
            self.interface.on_change()

    def select_item(self, index, item):
        self._selected_item = item
        self.apply_native_state()
        self.interface.on_change()

    def get_selected_index(self):
        return self._selected_index()

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.intrinsic_width)
        self.interface.intrinsic.height = 3
