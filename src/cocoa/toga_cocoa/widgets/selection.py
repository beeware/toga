from rubicon.objc import objc_method, SEL
from travertino.size import at_least

from toga_cocoa.libs import NSPopUpButton

from .base import Widget


class TogaPopupButton(NSPopUpButton):
    @objc_method
    def onSelect_(self, obj) -> None:
        if self.interface.on_select:
            self.interface.on_select(self.interface)


class Selection(Widget):
    def create(self):
        self.native = TogaPopupButton.alloc().init()
        self.native.interface = self.interface

        self.native.target = self.native
        self.native.action = SEL('onSelect:')

        self.add_constraints()

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.height = content_size.height
        self.interface.intrinsic.width = at_least(max(self.interface.MIN_WIDTH, content_size.width))

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
