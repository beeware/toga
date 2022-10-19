from travertino.size import at_least

from ..libs import Gtk, gtk_alignment

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = Gtk.Label()
        self.native.set_line_wrap(False)

        self.native.interface = self.interface

        self.native.connect('show', lambda event: self.rehint())

    def set_alignment(self, value):
        xalign, justify = gtk_alignment(value)
        self.native.set_xalign(xalign)    # Aligns the whole text block within the widget.
        self.native.set_yalign(0.5)
        self.native.set_justify(justify)  # Aligns multiple lines relative to each other.

    def set_text(self, value):
        # FIXME after setting the label the label jumps to the top left
        # corner and only jumps back at its place after resizing the window.
        self.native.set_text(self.interface._text)

    def rehint(self):
        # print("REHINT", self,
        #     self.native.get_preferred_width(), self.native.get_preferred_height(),
        #     getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False)
        # )
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[1]
