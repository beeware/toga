from toga.interface import OptionContainer as OptionContainerInterface

from ..container import Container
from ..libs import *
from .base import WidgetMixin


class TogaTabViewDelegate(NSObject):
    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        pass
        # print ("Select tab view item")


class OptionContainer(OptionContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, content=None):
        super(OptionContainer, self).__init__(id=id, style=style, content=content)
        self._create()

    def create(self):
        self._impl = NSTabView.alloc().init()

        self._delegate = TogaTabViewDelegate.alloc().init()
        self._delegate.interface = self

        self._impl.setDelegate_(self._delegate)

        # Add the layout constraints
        self._add_constraints()

    def _add_content(self, label, container, widget):
        item = NSTabViewItem.alloc().initWithIdentifier_('%s-Tab-%s' % (id(self), id(widget)))
        item.setLabel_(label)

        # Turn the autoresizing mask into constraints.
        # This could be overcome by describing the specific constraints
        # that the autoresize mask defines...
        widget._impl.setTranslatesAutoresizingMaskIntoConstraints_(True)

        item.setView_(container._impl)

        self._impl.addTabViewItem_(item)
