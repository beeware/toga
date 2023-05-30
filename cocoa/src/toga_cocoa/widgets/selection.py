from travertino.size import at_least

from toga_cocoa.libs import SEL, NSPopUpButton, objc_method, objc_property

from .base import Widget


class TogaPopupButton(NSPopUpButton):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onSelect_(self, obj) -> None:
        self.interface.on_change(self.interface)


class Selection(Widget):
    def create(self):
        self.native = TogaPopupButton.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.target = self.native
        self.native.action = SEL("onSelect:")

        self.add_constraints()

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.height = content_size.height
        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, content_size.width)
        )

    def _title_for_item(self, item):
        if self.interface._accessor:
            title = getattr(item, self.interface._accessor)
        else:
            title = item.value

        return str(title)

    def change_source(self, source):
        self.native.removeAllItems()
        for item in source:
            self.native.addItemWithTitle(self._title_for_item(item))
        self.interface.on_change(self.interface)

    def insert(self, index, item):
        self.native.insertItemWithTitle(self._title_for_item(item), atIndex=index)

    def change(self, item):
        index = self.interface._items.index(item)
        native_item = self.native.itemAtIndex(index)
        native_item.title = self._title_for_item(item)

    def remove(self, index, item):
        selection_change = self.native.indexOfSelectedItem == index

        self.native.removeItemAtIndex(index)

        if selection_change:
            self.interface.on_change(self.interface)

    def clear(self):
        self.native.removeAllItems()
        self.interface.on_change(self.interface)

    def select_item(self, index, item):
        self.native.selectItemAtIndex(index)
        self.interface.on_change(self.interface)

    def get_selected_item(self):
        index = self.native.indexOfSelectedItem
        if index == -1:
            return None
        else:
            return self.interface._items[self.native.indexOfSelectedItem]
