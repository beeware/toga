from gi.repository import Gtk
from toga_gtk.container import Container

from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface

    def set_content(self, widget):
        if widget.native is None:
            self.inner_container = Container()
            self.inner_container.content = widget
        else:
            self.inner_container = widget

        if self.native.get_child():
            self.native.get_child().destroy()

        self.native.add(self.inner_container.native)
        self.native.show_all()

    def set_app(self, app):
        if self.interface.content:
            self.interface.content.app = app

    def set_window(self, window):
        if self.interface.content:
            self.interface.content.window = window

    def apply_sub_layout(self):
        if self.interface.content is not None:
            self.inner_container.content.interface._update_layout(
                min_height=self.inner_container.content.interface.layout.height)

    def set_vertical(self, value):
        self.native.set_policy(
            Gtk.PolicyType.AUTOMATIC if getattr(self, 'horizontal', True) else Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC if getattr(self, 'vertical', True) else Gtk.PolicyType.NEVER,
        )

    def set_horizontal(self, value):
        self.native.set_policy(
            Gtk.PolicyType.AUTOMATIC if getattr(self, 'horizontal', True) else Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC if getattr(self, 'vertical', True) else Gtk.PolicyType.NEVER,
        )
