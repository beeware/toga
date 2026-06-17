from travertino.size import at_least

from toga_gtk.libs import GTK_VERSION, Gtk, gtk_text_align
from toga_gtk.widgets.base import Widget


class HelloWorld(Widget):
    def create(self):
        self.native = Gtk.Label()
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.set_line_wrap(False)
        else:  # pragma: no-cover-if-gtk3
            self.native.set_wrap(False)

        self.native.set_text("Hello World!")

    def set_text_align(self, value):
        xalign, justify = gtk_text_align(value)
        self.native.set_xalign(xalign)  # Aligns the whole text block within the widget.
        self.native.set_yalign(0.0)  # Aligns the text block to the top
        self.native.set_justify(
            justify
        )  # Aligns multiple lines relative to each other.

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # print(
            #     "REHINT",
            #     self,
            #     self.native.get_preferred_width(),
            #     self.native.get_preferred_height(),
            #     getattr(self, "_fixed_height", False),
            #     getattr(self, "_fixed_width", False),
            # )
            width = self.native.get_preferred_width()
            height = self.native.get_preferred_height()

            self.interface.intrinsic.width = at_least(width[0])
            self.interface.intrinsic.height = height[1]
        else:  # pragma: no-cover-if-gtk3
            # print(
            #     "REHINT",
            #     self,
            #     self.native.get_preferred_size()[0].width,
            #     self.native.get_preferred_size()[0].height,
            # )
            min_size, size = self.native.get_preferred_size()

            self.interface.intrinsic.width = at_least(min_size.width)
            self.interface.intrinsic.height = size.height
