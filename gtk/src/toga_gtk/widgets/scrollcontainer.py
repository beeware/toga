from ..container import TogaContainer
from ..libs import Gtk
from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = Gtk.ScrolledWindow()

        # Set this minimum size of scroll windows because we must reserve space for
        # scrollbars when splitter resized. See, https://gitlab.gnome.org/GNOME/gtk/-/issues/210
        self.native.set_min_content_width(self.interface._MIN_WIDTH)
        self.native.set_min_content_height(self.interface._MIN_HEIGHT)

        self.native.set_overlay_scrolling(True)

        self.inner_container = TogaContainer()
        self.native.add(self.inner_container)

    def set_content(self, widget):
        self.inner_container.content = widget

        # Force the display of the new content
        self.native.show_all()

    def set_app(self, app):
        if self.interface.content:
            self.interface.content.app = app

    def set_window(self, window):
        if self.interface.content:
            self.interface.content.window = window

    def set_horizontal(self, value):
        self.native.set_policy(
            Gtk.PolicyType.AUTOMATIC
            if self.interface.horizontal
            else Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
            if self.interface.vertical
            else Gtk.PolicyType.NEVER,
        )

    def set_vertical(self, value):
        self.native.set_policy(
            Gtk.PolicyType.AUTOMATIC
            if self.interface.horizontal
            else Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
            if self.interface.vertical
            else Gtk.PolicyType.NEVER,
        )

    def set_on_scroll(self, on_scroll):
        self.interface.factory.not_implemented("ScrollContainer.set_on_scroll()")

    def get_vertical_position(self):
        self.interface.factory.not_implemented(
            "ScrollContainer.get_vertical_position()"
        )
        return 0

    def set_vertical_position(self, vertical_position):
        self.interface.factory.not_implemented(
            "ScrollContainer.set_vertical_position()"
        )

    def get_horizontal_position(self):
        self.interface.factory.not_implemented(
            "ScrollContainer.get_horizontal_position()"
        )
        return 0

    def set_horizontal_position(self, horizontal_position):
        self.interface.factory.not_implemented(
            "ScrollContainer.set_horizontal_position()"
        )
