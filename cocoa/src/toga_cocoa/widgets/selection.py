from travertino.size import at_least

from toga_cocoa.libs import SEL, NSPopUpButton, objc_method, objc_property

from .base import Widget


class TogaPopupButton(NSPopUpButton):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onSelect_(self, obj) -> None:
        self.interface.on_change()


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

    def insert(self, index, item):
        # Issue 2319 - if item titles are not unique, macOS will move the existing item,
        # rather than creating a duplicate item. To work around this, create an item
        # with a temporary but unique name, then change the name. `_title_for_item()`
        # can't return newlines, so the use of a newline guarantees the name for the
        # initial item is unique.
        self.native.insertItemWithTitle(
            "\n<temp>",
            atIndex=index,
        )
        self.native.itemAtIndex(index).title = self.interface._title_for_item(item)

        # If this is the first time item in the list, it will be automatically
        # selected; trigger a change event.
        if len(self.interface.items) == 1:
            self.interface.on_change()

    def change(self, item):
        index = self.interface._items.index(item)
        native_item = self.native.itemAtIndex(index)
        native_item.title = self.interface._title_for_item(item)
        # Changing the item text can change the layout size
        self.interface.refresh()

    def remove(self, index, item):
        selection_change = self.native.indexOfSelectedItem == index

        self.native.removeItemAtIndex(index)

        if selection_change:
            self.interface.on_change()

    def clear(self):
        self.native.removeAllItems()
        self.interface.on_change()

    def select_item(self, index, item):
        self.native.selectItemAtIndex(index)
        self.interface.on_change()

    def get_selected_index(self):
        index = self.native.indexOfSelectedItem
        if index == -1:
            return None
        else:
            return index
