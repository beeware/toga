from gi.repository import Gtk
from ..container import Container
from .base import Widget


class OptionContainer(Widget):
    def create(self):
        # We want a single unified widget; the vbox is the representation of that widget.
        self.native = Gtk.Notebook()
        self.native.interface = self.interface

        self.containers = []

    def add_content(self, label, widget):
        # FIXME? Is there a better way to prevent the content of being occluded from the tabs?
        # Also 25 is just a guesstimate not based on anything.
        widget.interface.style.margin_top += 25  # increase top margin to prevent occlusion.
        if widget.native is None:
            container = Container()
            container.content = widget
        else:
            container = widget

        self.containers.append((label, container, widget))
        self.native.append_page(container.native, Gtk.Label(label))
