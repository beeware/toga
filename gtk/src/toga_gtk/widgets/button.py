from travertino.size import at_least

from toga.colors import TRANSPARENT

from ..libs import GTK_VERSION, Gtk
from .base import Widget


class Button(Widget):
    def create(self):
        self.native = Gtk.Button()
        self.native.connect("clicked", self.gtk_clicked)

        self._icon = None

    def get_text(self):
        text = self.native.get_label()
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            return text
        return text if text else ""  # pragma: no-cover-if-gtk3

    def set_text(self, text):
        self.native.set_label(text)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            if icon:
                self.native.set_image(Gtk.Image.new_from_pixbuf(icon._impl.native(32)))
                self.native.set_always_show_image(True)
            else:
                self.native.set_image(None)
                self.native.set_always_show_image(False)
        else:  # pragma: no-cover-if-gtk3
            if icon:
                icon._impl.native.set_icon_size(Gtk.IconSize.LARGE)
                self.native.set_child(icon._impl.native)
            else:
                text = self.native.get_label()
                if text:
                    self.native.set_label(text)
                self.native.set_child(None)

    def set_enabled(self, value):
        self.native.set_sensitive(value)

    def set_background_color(self, color):
        # Buttons interpret TRANSPARENT backgrounds as a reset
        super().set_background_color(None if color is TRANSPARENT else color)

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # print(
            #     "REHINT",
            #     self,
            #     self.native.get_preferred_width(),
            #     self.native.get_preferred_height(),
            # )
            width = self.native.get_preferred_width()
            height = self.native.get_preferred_height()

            self.interface.intrinsic.width = at_least(width[0])
            self.interface.intrinsic.height = height[1]
        else:  # pragma: no-cover-if-gtk3
            pass

    def gtk_clicked(self, event):
        self.interface.on_press()
