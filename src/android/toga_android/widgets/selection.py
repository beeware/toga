from travertino.size import at_least

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from ..libs.android_widgets import (
    ArrayAdapter,
    Gravity,
    OnItemSelectedListener,
    R__layout,
    Spinner,
    View__MeasureSpec
)
from .base import Widget


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
        # On Android, the list of options is provided to the `Spinner` wrapped in
        # an `ArrayAdapter`. We store `self.adapter` to avoid having to typecast it
        # in `add_item()`.
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
        return self.native.getSelectedItem().toString()

    def remove_all_items(self):
        self.native.getAdapter().clear()

    def rehint(self):
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()

    def set_alignment(self, value):
        self.native.setGravity(
            {
                LEFT: Gravity.CENTER_VERTICAL | Gravity.LEFT,
                RIGHT: Gravity.CENTER_VERTICAL | Gravity.RIGHT,
                CENTER: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
                JUSTIFY: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
            }[value]
        )

    def set_on_select(self, handler):
        # No special handling is required.
        pass
