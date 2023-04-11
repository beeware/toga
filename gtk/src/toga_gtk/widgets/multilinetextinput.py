from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        # Wrap the TextView in a ScrolledWindow in order to show a
        # vertical scroll bar when necessary.
        self.native = Gtk.ScrolledWindow()
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.textview = Gtk.TextView()
        self.buffer = Gtk.TextBuffer()
        self.textview.set_buffer(self.buffer)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.native.add(self.textview)

        self._placeholder = ""
        self.textview.connect("focus-in-event", self.gtk_on_focus_in)
        self.textview.connect("focus-out-event", self.gtk_on_focus_out)
        self.tag_placeholder = self.buffer.create_tag("placeholder", foreground="gray")

    def set_value(self, value):
        self.buffer.set_text(value)

    def get_value(self):
        return self.buffer.get_text(
            self.buffer.get_start_iter(), self.buffer.get_end_iter(), True
        )

    def set_readonly(self, value):
        self.textview.set_property("editable", not value)
        self.textview.set_property("cursor-visible", not value)

    def set_placeholder(self, value):
        """Set the placeholder text of the widget.

        GTK.TextView does not have a placeholder option by default so we
        have to create one. We do this with the two helper functions
        `on_focus_in` and `on_focus_out`.
        """
        if self.get_value() == self._placeholder:
            self._placeholder = value
            self.buffer.set_text(self.interface.value)
            self.buffer.apply_tag(
                self.tag_placeholder,
                self.buffer.get_start_iter(),
                self.buffer.get_end_iter(),
            )  # make the placeholder text gray.
        else:
            self._placeholder = value

    def gtk_on_focus_in(self, *args):
        if self.get_value() == self._placeholder:
            self.buffer.set_text("")
        return False

    def gtk_on_focus_out(self, *args):
        if self.get_value() == "":
            self.buffer.set_text(self.interface.placeholder)
            self.buffer.apply_tag(
                self.tag_placeholder,
                self.buffer.get_start_iter(),
                self.buffer.get_end_iter(),
            )  # make the placeholder text gray.
        return False

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def set_on_change(self, handler):
        self.interface.factory.not_implemented("MultilineTextInput.set_on_change()")

    def scroll_to_bottom(self):
        self.buffer.place_cursor(self.buffer.get_end_iter())
        self.textview.scroll_to_mark(self.buffer.get_insert(), 0.0, True, 0.0, 0.0)

    def scroll_to_top(self):
        self.buffer.place_cursor(self.buffer.get_start_iter())
        self.textview.scroll_to_mark(self.buffer.get_insert(), 0.0, True, 0.0, 0.0)
