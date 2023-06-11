from travertino.size import at_least

from ..libs import Gtk, gtk_alignment
from .base import Widget


class Label(Widget):
    def create(self):
        self.native = Gtk.Label()
        self.native.set_wrap(False)

    def set_alignment(self, value):
        xalign, justify = gtk_alignment(value)
        self.native.set_xalign(xalign)  # Aligns the whole text block within the widget.
        self.native.set_yalign(0.0)  # Aligns the text block to the top
        self.native.set_justify(
            justify
        )  # Aligns multiple lines relative to each other.

    def get_text(self):
        return self.native.get_text()

    def set_text(self, value):
        self.native.set_text(value)

    def rehint(self):
        # print(
        #     "REHINT",
        #     self,
        #     self.native.get_preferred_size()[0].width,
        #     self.native.get_preferred_size()[0].height,
        # )
        min_size, size = self.native.get_preferred_size()

        self.interface.intrinsic.width = at_least(min_size.width)
        self.interface.intrinsic.height = size.height
