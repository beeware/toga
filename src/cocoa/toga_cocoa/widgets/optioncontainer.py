from rubicon.objc import at

from toga_cocoa.libs import (
    NSObject,
    objc_method,
    NSTabView,
    NSTabViewItem
)
from toga_cocoa.window import CocoaViewport

from .base import Widget


class OptionException(ValueError):
    pass


class TogaTabViewDelegate(NSObject):
    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        index = at(item.identifier).longValue
        if self.interface.on_select:
            self.interface.on_select(self.interface, option=self.interface.content[index])


class OptionContainer(Widget):
    def create(self):
        self.native = NSTabView.alloc().init()
        self.delegate = TogaTabViewDelegate.alloc().init()
        self.delegate.interface = self.interface
        self.delegate._impl = self
        self.native.delegate = self.delegate

        # Add the layout constraints
        self.add_constraints()

    def add_content(self, label, widget):
        """ Adds a new option to the option container.

        Args:
            label (str): The label for the option container
            widget: The widget or widget tree that belongs to the label.
        """
        widget.viewport = CocoaViewport(widget.native)

        for child in widget.interface.children:
            child._impl.container = widget

        item = NSTabViewItem.alloc().initWithIdentifier(len(self.interface.content) - 1)
        item.label = label

        # Turn the autoresizing mask on the widget widget
        # into constraints. This makes the widget fill the
        # available space inside the OptionContainer.
        widget.native.translatesAutoresizingMaskIntoConstraints = True

        item.view = widget.native
        self.native.addTabViewItem(item)

    def remove_content(self, index):
        if self.native.numberOfTabViewItem == 1:
            # don't allow remove if there is one tab left
            raise OptionException('Option cannot be deleted because there is only one left')

        tabview = self.native.tabViewItemAtIndex(index)
        self.native.removeTabViewItem(tabview)

    def set_on_select(self, handler):
        pass

    def set_option_enabled(self, index, enabled):
        tabview = self.native.tabViewItemAtIndex(index)
        if not enabled and tabview == self.native.selectedTabViewItem:
            # Don't allow to disable selected tab
            raise OptionException('Selected Option cannot be disabled')

        if self.native.numberOfTabViewItem == 1:
            # don't allow disable if there is one tab left
            raise OptionException('Option cannot be disabled because there is only one left')

        tabview._setTabEnabled(enabled)

    def is_option_enabled(self, index):
        tabview = self.native.tabViewItemAtIndex(index)
        return tabview._isTabEnabled()

    def set_option_label(self, index, value):
        tabview = self.native.tabViewItemAtIndex(index)
        tabview.label = value

    def get_option_label(self, index):
        tabview = self.native.tabViewItemAtIndex(index)
        return tabview.label
