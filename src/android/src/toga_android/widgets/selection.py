from travertino.size import at_least

from ..libs.android import R__layout
from ..libs.android.view import Gravity, View__MeasureSpec
from ..libs.android.widget import ArrayAdapter, OnItemSelectedListener, Spinner
from .base import Widget, align


class TogaOnItemSelectedListener(OnItemSelectedListener):
    def __init__(self, impl):
        super().__init__()
        self._impl = impl

    def onItemSelected(self, _parent, _view, _position, _id):
        if self._impl.interface.on_select:
            self._impl.interface.on_select(widget=self._impl.interface)


class Selection(Widget):
    def create(self):
        self.native = Spinner(self._native_activity, Spinner.MODE_DROPDOWN)
        self.native.setOnItemSelectedListener(TogaOnItemSelectedListener(
            impl=self
        ))
        self.adapter = ArrayAdapter(
            self._native_activity,
            R__layout.simple_spinner_item
        )
        self.adapter.setDropDownViewResource(R__layout.simple_spinner_dropdown_item)
        self.native.setAdapter(self.adapter)
        # Create a mapping from text to numeric index to support `select_item()`.
        self._indexByItem = {}

    def add_item(self, item):
        new_index = self.adapter.getCount()
        self.adapter.add(str(item))
        self._indexByItem[item] = new_index

    def select_item(self, item):
        self.native.setSelection(self._indexByItem[item])

    def get_selected_item(self):
        selected = self.native.getSelectedItem()
        if selected:
            return str(selected)
        else:
            return None

    def remove_all_items(self):
        self.adapter.clear()

    def rehint(self):
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()

    def set_alignment(self, value):
        self.native.setGravity(Gravity.CENTER_VERTICAL | align(value))

    def set_on_select(self, handler):
        # No special handling is required.
        pass
