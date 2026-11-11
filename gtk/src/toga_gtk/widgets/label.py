from travertino.size import at_least

from ..libs import GTK_VERSION, Gdk, Gtk, Pango, gtk_text_align
from .base import Widget


class Label(Widget):
    def create(self):
        self.native = Gtk.Label()
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.set_line_wrap(False)
            self.native.connect("size-allocate", self.gtk_on_size_allocate)
        else:  # pragma: no-cover-if-gtk3
            self.native.set_wrap(False)
            self.native.set_overflow(Gtk.Overflow.HIDDEN)
        self.native.set_ellipsize(Pango.EllipsizeMode.END)

    if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4  # pragma: no branch

        def gtk_on_size_allocate(self, widget, allocation):
            clip = Gdk.Rectangle()
            clip.x = allocation.x
            clip.y = allocation.y
            clip.width = allocation.width
            clip.height = allocation.height

            self.native.set_clip(clip)

    def set_text_align(self, value):
        xalign, justify = gtk_text_align(value)

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
        # We must use the preferred size rather than minimum size here, as the ellipsize
        # mode makes the label possible to shrink to a minimum size of just 3 dots.
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            _, preferred_width = self.native.get_preferred_width()
            _, preferred_height = self.native.get_preferred_height()

            self.interface.intrinsic.width = at_least(preferred_width)
            self.interface.intrinsic.height = preferred_height
        else:  # pragma: no-cover-if-gtk3
            _, preferred_size = self.native.get_preferred_size()

            self.interface.intrinsic.width = at_least(preferred_size.width)
            self.interface.intrinsic.height = preferred_size.height
