from toga.interface import OptionContainer as OptionContainerInterface

from ..container import Container
from ..libs import *
from ..utils import process_callback
from .base import WidgetMixin


class TogaTabViewDelegate(NSObject):
    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        id_tab_view = item.identifier.split('-')[2]
        process_callback(self._interface._update_current_tab_view(id_tab_view,
                                                                item.label))


class OptionContainer(OptionContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, content=None):
        super(OptionContainer, self).__init__(id=id, style=style, content=content)
        self._create()

    def create(self):
        self._impl = NSTabView.alloc().init()

        self._delegate = TogaTabViewDelegate.alloc().init()
        self._delegate._interface = self

        self._impl.delegate = self._delegate

        # Add the layout constraints
        self._add_constraints()

    def _update_current_tab_view(self, view_id, view_label):
        self._selected = {'id':view_id, 'label':view_label}

    def _add_content(self, label, container, widget):
        item = NSTabViewItem.alloc().initWithIdentifier('%s-Tab-%s' % (id(self), id(widget)))
        item.label = label

        # Turn the autoresizing mask on the container widget
        # into constraints. This makes the container fill the
        # available space inside the OptionContainer.
        container._impl.translatesAutoresizingMaskIntoConstraints = True

        item.view = container._impl

        self._impl.addTabViewItem(item)
