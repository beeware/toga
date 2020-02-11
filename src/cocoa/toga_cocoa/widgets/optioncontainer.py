from rubicon.objc import (
    at,
    objc_method,
    NSObject,
)

# from toga_cocoa.libs import *
from toga_cocoa.libs import (
    NSTabView,
    NSTabViewItem,
)

from toga_cocoa.window import CocoaViewport

from .base import Widget



class TogaTabViewDelegate(NSObject):
    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        if self.interface.on_select:
            index = at(item.identifier).longValue
            option = self.interface.content[index]
            self.interface.on_select(self.interface, option=option, index=index)

        # required to redraw new tabs correctly (possible Toga bug?)
        # NOTE: does not work as `viewport` not set in cocoa `widget` impl.
        # self.interface.refresh()



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

    def set_on_select(self, handler):
        pass
