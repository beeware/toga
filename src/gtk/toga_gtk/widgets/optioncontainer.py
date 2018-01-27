from gi.repository import Gtk

from toga_gtk.window import GtkViewport

from .base import Widget


class OptionContainer(Widget):
    def create(self):
        # We want a single unified widget; the vbox is the representation of that widget.
        self.native = Gtk.Notebook()
        self.native.interface = self.interface

    def add_content(self, label, widget):
        widget.viewport = GtkViewport(widget.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        self.native.append_page(widget.native, Gtk.Label(label))

    def set_on_select(self, handler):
        # No special handling required
        pass
