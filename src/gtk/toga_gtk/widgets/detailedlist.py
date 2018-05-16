from gi.repository import Gtk

from .base import Widget


class DetailedList(Widget):
    def create(self):
        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface

        # Create DetailedList
        self.vbox = Gtk.VBox()

        self.native.add_with_viewport(self.vbox)

    def change_source(self, source):
        # TODO
        self.interface.factory.not_implemented('DetailedList.change_source()')

    def insert(self, index, item):
        # TODO
        self.interface.factory.not_implemented('DetailedList.insert()')

    def change(self, item):
        # TODO
        self.interface.factory.not_implemented('DetailedList.change()')

    def remove(self, item):
        # TODO
        self.interface.factory.not_implemented('DetailedList.remove()')

    def clear(self):
        # TODO
        self.interface.factory.not_implemented('DetailedList.clear()')

    def set_on_refresh(self, handler):
        pass

    def after_on_refresh(self):
        # TODO
        self.interface.factory.not_implemented('DetailedList.after_on_refresh()')

    def set_on_select(self, handler):
        pass

    def set_on_delete(self, handler):
        pass

    def scroll_to_row(self, row):
        # TODO
        self.interface.factory.not_implemented('DetailedList.scroll_to_row()')

    def rehint(self):
        # TODO
        self.interface.factory.not_implemented('DetailedList.rehint()')
