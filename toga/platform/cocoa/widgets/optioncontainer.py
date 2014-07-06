from __future__ import print_function, absolute_import, division

from ..libs import *
from .base import Widget


class OptionContainer(Widget):
    def __init__(self):
        super(OptionContainer, self).__init__()
        self._impl = None
        self._content = []

    def _startup(self):
        self._impl = NSTabView.alloc().init()
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        for label, container in self._content:
            self._add_panel(label, container)

    def add(self, label, container):
        self._content.append((label, container))
        container.window = self.window
        if self._impl:
            self._add_panel(label, container)

    def _add_panel(self, label, container):
        item = NSTabViewItem.alloc().initWithIdentifier_(get_NSString('Tab-%s' % id(container)))
        item.setLabel_(get_NSString(label))
        container.app = self.app
        item.setView_(container._impl)
        self._impl.addTabViewItem_(item)
