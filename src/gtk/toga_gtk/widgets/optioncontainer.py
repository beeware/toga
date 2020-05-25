from ..libs import Gtk
from ..window import GtkViewport
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

    def remove_content(self, index):
        self.interface.factory.not_implemented('OptionContainer.remove_content()')

    def set_option_enabled(self, index, enabled):
        self.interface.factory.not_implemented('OptionContainer.set_option_enabled()')

    def is_option_enabled(self, index):
        self.interface.factory.not_implemented('OptionContainer.is_option_enabled()')

    def set_option_label(self, index, value):
        self.interface.factory.not_implemented('OptionContainer.set_option_label()')

    def get_option_label(self, index):
        self.interface.factory.not_implemented('OptionContainer.get_option_label()')
