from rubicon.objc import at

from toga_cocoa.container import Container
from toga_cocoa.libs import *

from .base import Widget


class TogaTabViewDelegate(NSObject):
    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        ident = at(item.identifier).longValue
        if self.interface.on_select:
            self.interface.on_select(self.interface, option=self._impl.options[ident][2].interface)


class OptionContainer(Widget):
    def create(self):
        self.native = NSTabView.alloc().init()

        self.delegate = TogaTabViewDelegate.alloc().init()
        self.delegate.interface = self.interface
        self.delegate._impl = self
        self.native.delegate = self.delegate

        self.options = {}

        # Add the layout constraints
        self.add_constraints()

    def add_content(self, label, widget):
        """ Adds a new option to the option container.

        Args:
            label (str): The label for the option container
            widget: The widget or widget tree that belongs to the label.
        """
        if widget.native is None:
            container = Container()
            container.content = widget
        else:
            container = widget

        item = NSTabViewItem.alloc().initWithIdentifier(id(widget))
        item.label = label
        self.options[id(widget)] = (label, container, widget)

        # Turn the autoresizing mask on the container widget
        # into constraints. This makes the container fill the
        # available space inside the OptionContainer.
        container.native.translatesAutoresizingMaskIntoConstraints = True

        item.view = container.native
        self.native.addTabViewItem(item)

    def set_on_select(self, handler):
        pass
