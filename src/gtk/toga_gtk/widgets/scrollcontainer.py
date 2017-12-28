from gi.repository import Gtk

from toga_gtk.window import GtkViewport

from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface

    def set_content(self, widget):
        self.inner_container = widget

        widget.viewport = GtkViewport(self.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

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
