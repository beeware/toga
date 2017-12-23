from travertino.size import at_least

from toga_cocoa.libs import *

from .base import Widget


class TogaSelection(NSPopUpButton):
    @objc_method
    def onSelect_(self, obj) -> None:
        if self.interface.on_select:
            self.interface.on_select(self.interface)


class Selection(Widget):
    def create(self):
        rect = NSMakeRect(0, 0, 0, 0)
        self.native = NSPopUpButton.alloc().initWithFrame_pullsDown_(rect, 0)
        self.native.interface = self.interface

        self.add_constraints()

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.height = fitting_size.height
        self.interface.intrinsic.width = at_least(fitting_size.width)

    def remove_all_items(self):
        self.native.removeAllItems()

    def add_item(self, item):
        self.native.addItemWithTitle(item)

    def select_item(self, item):
        self.native.selectItemWithTitle(item)

    def get_selected_item(self):
        return self.native.titleOfSelectedItem

    def set_on_select(self, handler):
        pass
