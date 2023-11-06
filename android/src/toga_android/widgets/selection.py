from decimal import ROUND_UP

from android import R
from android.view import View
from android.widget import AdapterView, ArrayAdapter, Spinner
from java import dynamic_proxy

from .base import Widget


class TogaOnItemSelectedListener(dynamic_proxy(AdapterView.OnItemSelectedListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onItemSelected(self, parent, view, position, id):
        self.impl.on_change(position)

    def onNothingSelected(self, parent):
        self.impl.on_change(None)


class Selection(Widget):
    focusable = False

    def create(self):
        self.native = Spinner(self._native_activity, Spinner.MODE_DROPDOWN)
        self.native.setOnItemSelectedListener(TogaOnItemSelectedListener(impl=self))
        self.adapter = ArrayAdapter(self._native_activity, R.layout.simple_spinner_item)
        self.adapter.setDropDownViewResource(R.layout.simple_spinner_dropdown_item)
        self.native.setAdapter(self.adapter)
        self.last_selection = None

    # Programmatic selection changes do cause callbacks, but they may be delayed until a
    # later iteration of the main loop. So we always generate events immediately after
    # the change, and use self.last_selection to prevent duplication.
    def on_change(self, index):
        if index != self.last_selection:
            self.interface.on_change()
            self.last_selection = index

    def insert(self, index, item):
        self.adapter.insert(self.interface._title_for_item(item), index)
        if self.last_selection is None:
            self.select_item(0)
        elif index <= self.last_selection:
            # Adjust the selection index, but do not generate an event.
            self.last_selection += 1
            self.select_item(self.last_selection)

    def change(self, item):
        # Instead of calling self.insert and self.remove, use direct native calls to
        # avoid disturbing the selection.
        index = self.interface._items.index(item)
        self.adapter.insert(self.interface._title_for_item(item), index)
        self.adapter.remove(self.adapter.getItem(index + 1))

    def remove(self, index, item=None):
        self.adapter.remove(self.adapter.getItem(index))

        # Adjust the selection index, but only generate an event if the selected item
        # has been removed.
        removed_selection = self.last_selection == index
        if index <= self.last_selection:
            if self.adapter.getCount() == 0:
                self.last_selection = None
            else:
                self.last_selection = max(0, self.last_selection - 1)
                self.select_item(self.last_selection)

        if removed_selection:
            self.interface.on_change()

    def select_item(self, index, item=None):
        self.native.setSelection(index)
        self.on_change(index)

    def get_selected_index(self):
        selected = self.native.getSelectedItemPosition()
        return None if selected == Spinner.INVALID_POSITION else selected

    def clear(self):
        self.adapter.clear()
        self.on_change(None)

    def rehint(self):
        self.native.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
        self.interface.intrinsic.height = self.scale_out(
            self.native.getMeasuredHeight(), ROUND_UP
        )
