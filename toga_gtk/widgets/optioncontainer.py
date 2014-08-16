from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .base import Widget


class OptionContainer(Widget):
    def __init__(self, horizontal=True, vertical=True):
        super(OptionContainer, self).__init__()
        self._content = []

        self.startup()

    def startup(self):
        # We want a single unified widget; the vbox is the representation of that widget.
        self._impl = Gtk.Notebook()

    def add(self, label, container):
        self._content.append((label, container))
        container.window = self.window
        container.app = self.app
        self._impl.append_page(container._impl, Gtk.Label(label))
