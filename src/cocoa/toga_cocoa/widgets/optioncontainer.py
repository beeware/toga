from toga.interface import OptionContainer as OptionContainerInterface

from ..container import Container
from ..libs import *
from ..utils import process_callback
from .base import WidgetMixin


class TogaTabViewDelegate(NSObject):
    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        id_tab_view = item.identifier.split('-')[2]
        process_callback(self._interface._update_current_tab_view(id_tab_view))


class OptionContainer(OptionContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, content=None):
        super(OptionContainer, self).__init__(id=id, style=style, content=content)
        self._create()

    def create(self):
        self._impl = NSTabView.alloc().init()

        self._delegate = TogaTabViewDelegate.alloc().init()
        self._delegate._interface = self

        self._impl.setDelegate_(self._delegate)

        # Add the layout constraints
        self._add_constraints()

    def _update_current_tab_view(self, value):
        self._selected = value

    def _add_content(self, label, container, widget):
        item = NSTabViewItem.alloc().initWithIdentifier_('%s-Tab-%s' % (id(self), id(widget)))
        item.setLabel_(label)

        # Turn the autoresizing mask on the container widget
        # into constraints. This makes the container fill the
        # available space inside the OptionContainer.
        container._impl.setTranslatesAutoresizingMaskIntoConstraints_(True)

        item.setView_(container._impl)

        self._impl.addTabViewItem_(item)
