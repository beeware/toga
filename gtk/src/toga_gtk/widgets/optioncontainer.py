from ..container import TogaContainer
from ..libs import Gtk
from .base import Widget


class OptionContainer(Widget):
    def create(self):
        # We want a single unified widget; the vbox is the representation of that widget.
        self.native = Gtk.Notebook()
        self.native.connect("switch-page", self.gtk_on_switch_page)

    def gtk_on_switch_page(self, widget, page, page_num):
        if self.interface.on_select:
            self.interface.on_select(
                self.interface, option=self.interface.content[page_num]
            )

    def add_content(self, index, text, widget):
        sub_container = TogaContainer()
        sub_container.content = widget

        self.native.insert_page(sub_container, Gtk.Label(label=text), index)

        # Tabs aren't visible by default;
        # tell the notebook to show all content.
        self.native.show_all()

    def set_on_select(self, handler):
        # No special handling required
        pass

    def remove_content(self, index):
        if index == self.native.get_current_page():
            # Don't allow removal of a selected tab
            raise self.interface.OptionException(
                "Currently selected option cannot be removed"
            )
        self.native.remove_page(index)

    def set_option_enabled(self, index, enabled):
        self.interface.factory.not_implemented("OptionContainer.set_option_enabled()")

    def is_option_enabled(self, index):
        self.interface.factory.not_implemented("OptionContainer.is_option_enabled()")

    def set_option_text(self, index, value):
        tab = self.native.get_nth_page(index)
        self.native.set_tab_label(tab, Gtk.Label(label=value))

    def get_option_text(self, index):
        tab = self.native.get_nth_page(index)
        return self.native.get_tab_label(tab).get_label()

    def get_current_tab_index(self):
        return self.native.get_current_page()

    def set_current_tab_index(self, current_tab_index):
        self.native.set_current_page(current_tab_index)
