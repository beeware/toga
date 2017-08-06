from ..container import Container
from ..libs import *
from .base import Widget


class TogaTabViewDelegate(NSObject):
    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        pass


class OptionContainer(Widget):
    def create(self):
        self.native = NSTabView.alloc().init()

        self.delegate = TogaTabViewDelegate.alloc().init()
        self.delegate.interface = self
        self.native.delegate = self.delegate

        self.containers = []

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

        self.containers.append((label, container, widget))

        item = NSTabViewItem.alloc().initWithIdentifier('%s-Tab-%s' % (id(self), id(widget)))
        item.label = label

        # Turn the autoresizing mask on the container widget
        # into constraints. This makes the container fill the
        # available space inside the OptionContainer.
        container.native.translatesAutoresizingMaskIntoConstraints = True

        item.view = container.native
        self.native.addTabViewItem(item)
