from toga.interface import Selection as SelectionInterface

from .base import WidgetMixin

from ..libs.appkit import NSPopUpButton
from ..libs.foundation import NSMakeRect
from ..libs import *

from ..utils import process_callback

class TogaSelection(NSPopUpButton):
    @objc_method
    def onSelect_(self, obj) -> None:
        if self._interface.on_select:
            process_callback(self._interface.on_select(self._interface))


class Selection(WidgetMixin, SelectionInterface):

    def __init__(self, id=None, style=None, items=tuple(), on_select=None):
        super().__init__(id=id, style=style, items=items, on_select=on_select)
        self._create()

    def create(self):
        rect = NSMakeRect(0, 0, 0, 0)
        self._impl = TogaSelection.alloc().initWithFrame_pullsDown_(rect, 0)
        self._impl._interface = self

        self._impl.setTarget_(self._impl)
        self._impl.setAction_(SEL('onSelect:'))

        self._add_constraints()

    def rehint(self):
        fitting_size = self._impl.fittingSize()
        self.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width
        )
        # Hacky hack! But, Russ told me to do it.
        self.style.margin_top = -2

    def _remove_all_items(self):
        self._impl.removeAllItems()

    def _add_item(self, item):
        self._impl.addItemWithTitle_(item)

    def _select_item(self, item):
        self._impl.selectItemWithTitle_(item)

    def _get_selected_item(self):
        return self._impl.titleOfSelectedItem
