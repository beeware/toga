from ..container import TogaContainer
from ..libs import Gtk
from .base import Widget


class OptionContainer(Widget):
    def create(self):
        self.native = Gtk.Notebook()
        self.native.connect("switch-page", self.gtk_on_switch_page)
        self.sub_containers = []

    def gtk_on_switch_page(self, widget, page, page_num):
        self.interface.on_select(None)

    def add_content(self, index, text, widget):
        sub_container = TogaContainer()
        sub_container.content = widget

        self.sub_containers.insert(index, sub_container)
        self.native.insert_page(sub_container, Gtk.Label(label=text), index)
        # Tabs aren't visible by default;
        # tell the notebook to show all content.
        self.native.show_all()

    def remove_content(self, index):
        self.native.remove_page(index)
        self.sub_containers[index].content = None
        del self.sub_containers[index]

    def set_option_enabled(self, index, enabled):
        self.sub_containers[index].set_visible(enabled)

    def is_option_enabled(self, index):
        return self.sub_containers[index].get_visible()

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
