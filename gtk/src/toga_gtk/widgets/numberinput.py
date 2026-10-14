import sys
from decimal import InvalidOperation

from travertino.size import at_least

from toga.handlers import WeakrefCallable
from toga.keys import Key
from toga.widgets.numberinput import _clean_decimal
from toga_gtk.keys import toga_key

from ..libs import GTK_VERSION, Gtk, gtk_text_align
from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.adjustment = Gtk.Adjustment()

        self.native = Gtk.SpinButton()
        self.native.set_adjustment(self.adjustment)
        self.native.set_numeric(True)

        self.native.connect("changed", self.gtk_on_change)
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.connect("key-press-event", self.gtk_key_press_event)
        else:  # pragma: no-cover-if-gtk3
            self.key_controller = Gtk.EventControllerKey.new()
            self.native.add_controller(self.key_controller)
            self.key_controller.connect(
                "key-pressed", WeakrefCallable(self.gtk_key_pressed)
            )

    def gtk_on_change(self, widget):
        self.interface.on_change()

    if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4

        def gtk_key_press_event(self, _entry, event):
            key_pressed = toga_key(event.keyval, event.state)
            if key_pressed and self.get_readonly() and key_pressed["key"] == Key.TAB:
                direction = (
                    Gtk.DirectionType.TAB_BACKWARD
                    if Key.SHIFT in key_pressed["modifiers"]
                    else Gtk.DirectionType.TAB_FORWARD
                )
                toplevel = self.native.get_toplevel()
                if toplevel and toplevel.is_toplevel():
                    toplevel.child_focus(direction)
                return True

    else:  # pragma: no-cover-if-gtk3

        def gtk_key_pressed(self, _controller, keyval, _keycode, state):
            key_pressed = toga_key(keyval, state)
            if key_pressed and self.get_readonly() and key_pressed["key"] == Key.TAB:
                direction = (
                    Gtk.DirectionType.TAB_BACKWARD
                    if Key.SHIFT in key_pressed["modifiers"]
                    else Gtk.DirectionType.TAB_FORWARD
                )
                root = self.native.get_root()
                if root:
                    root.child_focus(direction)
                return True

    def get_readonly(self):
        return not self.native.get_property("editable")

    def set_readonly(self, value):
        self.native.set_property("editable", not value)

    def set_step(self, step):
        self.adjustment.set_step_increment(float(self.interface.step))
        self.native.set_adjustment(self.adjustment)
        self.native.set_digits(abs(self.interface.step.as_tuple().exponent))

    def set_min_value(self, value):
        if value is None:
            self.adjustment.set_lower(-sys.float_info.max)
        else:
            self.adjustment.set_lower(float(value))
        self.native.set_adjustment(self.adjustment)

    def set_max_value(self, value):
        if value is None:
            self.adjustment.set_upper(sys.float_info.max)
        else:
            self.adjustment.set_upper(float(value))
        self.native.set_adjustment(self.adjustment)

    def get_value(self):
        try:
            return _clean_decimal(self.native.get_text(), self.interface.step)
        except InvalidOperation:
            return None

    def set_value(self, value):
        if value is None:
            self.native.set_value(0)
        else:
            self.native.set_value(value)

    def set_text_align(self, value):
        xalign, _justify = gtk_text_align(value)
        self.native.set_alignment(xalign)

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            width = self.native.get_preferred_width()
            height = self.native.get_preferred_height()

            self.interface.intrinsic.width = at_least(
                max(self.interface._MIN_WIDTH, width[1])
            )
            self.interface.intrinsic.height = height[1]
        else:  # pragma: no-cover-if-gtk3
            pass
