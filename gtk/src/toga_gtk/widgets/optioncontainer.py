import asyncio

from ..container import TogaContainer
from ..libs import Gtk
from .base import Widget


class OptionContainer(Widget):
    uses_icons = False

    def create(self):
        self.native = Gtk.Notebook()
        self.native.connect("switch-page", self.gtk_on_switch_page)
        self.sub_containers = []

    def gtk_on_switch_page(self, widget, page, page_num):
        # Inside the switch-page event handler, the page_num argument gives the
        # correct value for the page that has just been selected, but
        # self.native.current_page() does not. It won't return the correct value
        # until the switch-page event has completed. Since `on_select()` will
        # likely need to retrieve the current tab, we need to defer triggering
        # on_select() until we know current_page will return the correct value.
        # We do this by deferring the callback to execute on the event loop.
        asyncio.get_event_loop().call_soon(self.interface.on_select)

    def add_option(self, index, text, widget, icon):
        sub_container = TogaContainer()
        sub_container.content = widget

        self.sub_containers.insert(index, sub_container)
        self.native.insert_page(sub_container, Gtk.Label(label=text), index)
        # Tabs aren't visible by default;
        # tell the notebook to show all content.
        self.native.show_all()

    def remove_option(self, index):
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

    def set_option_icon(self, index, value):  # pragma: nocover
        # This shouldn't ever be invoked, but it's included for completeness.
        pass

    def get_option_icon(self, index):
        # Icons aren't supported
        return None

    def get_current_tab_index(self):
        return self.native.get_current_page()

    def set_current_tab_index(self, current_tab_index):
        self.native.set_current_page(current_tab_index)
