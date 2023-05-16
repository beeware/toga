from travertino.size import at_least

from ..libs import (
    Gtk,
    get_background_color_css,
    get_color_css,
    get_font_css,
    gtk_alignment,
)
from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        # Wrap the TextView in a ScrolledWindow in order to show a
        # vertical scroll bar when necessary.
        self.native = Gtk.ScrolledWindow()
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.buffer = Gtk.TextBuffer()
        self._add_change_handler()

        # The GTK TextView doesn't have an implementation of placeholder. We
        # fake it by using a different buffer that contains placeholder text.
        # This bufer is installed by default, until the value for the widget
        # becomes something non-empty. The placeholder buffer is also swapped
        # out when focus is gained, or a key press event occurs. The latter
        # is needed because the value can be changed programatically when
        # the widget already has focus.
        self.placeholder = Gtk.TextBuffer()
        self.tag_placeholder = self.placeholder.create_tag(
            "placeholder", foreground="gray"
        )

        self.native_textview = Gtk.TextView()
        self.native_textview.set_name(f"toga-{self.interface.id}-textview")
        self.native_textview.get_style_context().add_class("toga")

        self.native_textview.set_buffer(self.placeholder)
        self.native_textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.native_textview.connect("focus-in-event", self.gtk_on_focus_in)
        self.native_textview.connect("focus-out-event", self.gtk_on_focus_out)
        self.native_textview.connect("key-press-event", self.gtk_on_key_press)

        self.native.add(self.native_textview)

    def set_color(self, color):
        self.apply_css(
            "color",
            get_color_css(color),
            native=self.native_textview,
            selector=".toga, .toga text",
        )

    def set_background_color(self, color):
        self.apply_css(
            "background_color",
            get_background_color_css(color),
            native=self.native_textview,
            selector=".toga, .toga text",
        )

    def set_font(self, font):
        self.apply_css("font", get_font_css(font), native=self.native_textview)

    def get_value(self):
        return self.buffer.get_text(
            self.buffer.get_start_iter(), self.buffer.get_end_iter(), True
        )

    def set_value(self, value):
        # Temporarily disable change handlers so we don't get on_change
        # events for user content.
        self._remove_change_handler()
        self.buffer.set_text(value)
        self._add_change_handler()

        # If there's a non-empty value, use the "real" buffer; otherwise, use
        # the placeholder.
        if value:
            self.native_textview.set_buffer(self.buffer)
        else:
            self.native_textview.set_buffer(self.placeholder)

    def get_readonly(self):
        return not self.native_textview.get_property("editable")

    def set_readonly(self, value):
        self.native_textview.set_property("editable", not value)
        self.native_textview.set_property("cursor-visible", not value)

    def get_placeholder(self):
        return self.placeholder.get_text(
            self.placeholder.get_start_iter(), self.placeholder.get_end_iter(), True
        )

    def set_placeholder(self, value):
        """Set the placeholder text of the widget.

        GTK.TextView does not have a placeholder option by default so we have to create
        one. We do this by using a separate buffer, and swapping the buffer with the
        "real" buffer whenever focus or content changes.
        """
        self.placeholder.set_text(value)
        self.placeholder.apply_tag(
            self.tag_placeholder,
            self.placeholder.get_start_iter(),
            self.placeholder.get_end_iter(),
        )  # make the placeholder text gray.

    def set_alignment(self, value):
        _, justification = gtk_alignment(value)
        self.native_textview.set_justification(justification)

    def focus(self):
        self.native_textview.grab_focus()

    def _add_change_handler(self):
        print("ADD CHANGE HANDLER")
        self.change_handler = self.buffer.connect("changed", self.gtk_on_changed)

    def _remove_change_handler(self):
        print("REMOVE CHANGE HANDLER")
        self.buffer.disconnect(self.change_handler)

    def gtk_on_changed(self, *args):
        self.interface.on_change(None)

    def gtk_on_focus_in(self, *args):
        # When focus is gained, make sure the content buffer is active.
        print("FOCUS IN")
        self.native_textview.set_buffer(self.buffer)
        return False

    def gtk_on_focus_out(self, *args):
        # When focus is lost, if there's no content, install the placeholder
        print("FOCUS OUT")
        if self.get_value() == "":
            self.native_textview.set_buffer(self.placeholder)
        return False

    def gtk_on_key_press(self, *args):
        # If there's a key press, make sure the content buffer is active
        print("ON KEY PRESS")
        self.native_textview.set_buffer(self.buffer)
        return False

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def scroll_to_bottom(self):
        self.buffer.place_cursor(self.buffer.get_end_iter())
        self.native_textview.scroll_to_mark(
            self.buffer.get_insert(), 0.0, True, 0.0, 0.0
        )

    def scroll_to_top(self):
        self.buffer.place_cursor(self.buffer.get_start_iter())
        self.native_textview.scroll_to_mark(
            self.buffer.get_insert(), 0.0, True, 0.0, 0.0
        )
