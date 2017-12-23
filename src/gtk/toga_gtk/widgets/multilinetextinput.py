from gi.repository import Gtk

from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        self.native = Gtk.TextView()
        self.native.interface = self.interface
        self.buffer = Gtk.TextBuffer()
        self.native.set_buffer(self.buffer)

        self._placeholder = ''
        self.native.connect("focus-in-event", self.on_focus_in)
        self.native.connect("focus-out-event", self.on_focus_out)
        self.tag_placholder = self.buffer.create_tag("placeholder", foreground="gray")

    def set_value(self, value):
        self.buffer.set_text(value)

    def get_value(self):
        return self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)

    def set_readonly(self, value):
        self.native.set_property('editable', not value)
        self.native.set_property('cursor-visible', not value)

    def set_placeholder(self, value):
        """ Set the placeholder text of the widget.
        GTK.TextView does not have a placeholder option by default so we have to create one.
        We do this with the two helper functions `on_focus_in` and `on_focus_out`.
        """
        if self.get_value() == self._placeholder:
            self._placeholder = value
            self.buffer.set_text(value)
            self.buffer.apply_tag(self.tag_placholder,
                                  self.buffer.get_start_iter(),
                                  self.buffer.get_end_iter())  # make the placeholder text gray.
        else:
            self._placeholder = value

    def on_focus_in(self, *args):
        if self.get_value() == self._placeholder:
            self.buffer.set_text("")
        return False

    def on_focus_out(self, *args):
        if self.get_value() == "":
            self.buffer.set_text(self.interface.placeholder)
            self.buffer.apply_tag(self.tag_placholder,
                                  self.buffer.get_start_iter(),
                                  self.buffer.get_end_iter())  # make the placeholder text gray.
        return False

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
