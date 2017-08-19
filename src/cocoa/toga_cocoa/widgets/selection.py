from toga_cocoa.utils import process_callback

from .base import Widget

from ..libs.appkit import *
from ..libs.foundation import NSMakeRect


class TogaSelection(NSPopUpButton):
    @objc_method
    def popUpButtonUsed_(self, sender) -> None:
        if self.interface.on_select:
            process_callback(self.interface.on_select(self.interface))


class Selection(Widget):
    def create(self):
        rect = NSMakeRect(0, 0, 0, 0)
        self.native = TogaSelection.alloc().initWithFrame_pullsDown_(rect, 0)
        self.native.interface = self.interface

        self.native.target = self.native
        self.native.action = SEL('popUpButtonUsed:')

        self.add_constraints()

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width
        )
        # Hacky hack! But, Russ told me to do it.
        self.interface.style.margin_top = -2

    def remove_all_items(self):
        self.native.removeAllItems()

    def add_item(self, item):
        self.native.addItemWithTitle(item)

    def select_item(self, item):
        self.native.selectItemWithTitle(item)

    def get_selected_item(self):
        return self.native.titleOfSelectedItem
