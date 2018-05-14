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
        raise NotImplementedError()

    def insert(self, index, item):
        # TODO
        raise NotImplementedError()

    def change(self, item):
        # TODO
        raise NotImplementedError()

    def remove(self, item):
        # TODO
        raise NotImplementedError()

    def clear(self):
        # TODO
        raise NotImplementedError()

    def set_on_refresh(self, handler):
        pass

    def after_on_refresh(self):
        # TODO
        raise NotImplementedError()

    def set_on_select(self, handler):
        pass

    def set_on_delete(self, handler):
        pass

    def scroll_to_row(self, row):
        # TODO
        raise NotImplementedError()

    def rehint(self):
        # TODO
        raise NotImplementedError()
