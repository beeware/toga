from travertino.size import at_least

from ..container import TogaContainer
from ..libs import Gtk
from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = Gtk.ScrolledWindow()

        self.native.get_hadjustment().connect("changed", self.gtk_on_changed)
        self.native.get_vadjustment().connect("changed", self.gtk_on_changed)

        # Set this minimum size of scroll windows because we must reserve space for
        # scrollbars when splitter resized. See, https://gitlab.gnome.org/GNOME/gtk/-/issues/210
        self.native.set_min_content_width(self.interface._MIN_WIDTH)
        self.native.set_min_content_height(self.interface._MIN_HEIGHT)

        self.native.set_overlay_scrolling(True)

        self.document_container = TogaContainer()
        self.native.add(self.document_container)

    def gtk_on_changed(self, *args):
        self.interface.on_scroll()

    def set_content(self, widget):
        self.document_container.content = widget

        # Force the display of the new content
        self.native.show_all()

    def set_app(self, app):
        self.interface.content.app = app

    def set_window(self, window):
        self.interface.content.window = window

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def get_horizontal(self):
        return self.native.get_policy()[0] == Gtk.PolicyType.AUTOMATIC

    def set_horizontal(self, value):
        self.native.set_policy(
            Gtk.PolicyType.AUTOMATIC if value else Gtk.PolicyType.NEVER,
            (
                Gtk.PolicyType.AUTOMATIC
                if self.interface.vertical
                else Gtk.PolicyType.NEVER
            ),
        )
        # Disabling scrolling implies a position reset; that's a scroll event.
        if not value:
            self.native.get_hadjustment().set_value(0)
            self.interface.on_scroll()

    def get_vertical(self):
        return self.native.get_policy()[1] == Gtk.PolicyType.AUTOMATIC

    def set_vertical(self, value):
        self.native.set_policy(
            (
                Gtk.PolicyType.AUTOMATIC
                if self.interface.horizontal
                else Gtk.PolicyType.NEVER
            ),
            Gtk.PolicyType.AUTOMATIC if value else Gtk.PolicyType.NEVER,
        )
        # Disabling scrolling implies a position reset; that's a scroll event.
        if not value:
            self.native.get_vadjustment().set_value(0)
            self.interface.on_scroll()

    def get_max_vertical_position(self):
        return max(
            0,
            int(
                self.native.get_vadjustment().get_upper()
                - self.native.get_allocation().height
            ),
        )

    def get_vertical_position(self):
        return int(self.native.get_vadjustment().get_value())

    def get_max_horizontal_position(self):
        return max(
            0,
            int(
                self.native.get_hadjustment().get_upper()
                - self.native.get_allocation().width
            ),
        )

    def get_horizontal_position(self):
        return int(self.native.get_hadjustment().get_value())

    def set_position(self, horizontal_position, vertical_position):
        self.native.get_hadjustment().set_value(horizontal_position)
        self.native.get_vadjustment().set_value(vertical_position)
        self.interface.on_scroll()
