from rubicon.objc import NSPoint

from toga.colors import TRANSPARENT
from toga_cocoa.libs import (
    NSEventType,
    NSRange,
    NSStepper,
    NSTextField,
    NSTextView,
    NSView,
)

from .base import SimpleProbe
from .properties import toga_alignment, toga_color


class NumberInputProbe(SimpleProbe):
    native_class = NSView
    allows_invalid_value = True

    def __init__(self, widget):
        super().__init__(widget)
        self.native_input = self.impl.native_input
        assert isinstance(self.native_input, NSTextField)

        self.native_stepper = self.impl.native_stepper
        assert isinstance(self.native_stepper, NSStepper)

    def clear_input(self):
        self.widget.value = ""

    @property
    def value(self):
        return str(self.native_input.stringValue)

    async def increment(self):
        # Click a point on the middle line of the stepper horizontally, but very
        # slightly above the midpoint vertically. Remember Cocoa's coordinate
        # system is reversed.
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            self.native_stepper.convertPoint(
                NSPoint(
                    self.native_stepper.frame.size.width / 2,
                    self.native_stepper.frame.size.height / 2 + 5,
                ),
                toView=None,
            ),
        )

    async def decrement(self):
        # Click a point on the middle line of the stepper horizontally, but very
        # slightly below the midpoint vertically. Remember Cocoa's coordinate
        # system is reversed.
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            self.native_stepper.convertPoint(
                NSPoint(
                    self.native_stepper.frame.size.width / 2,
                    self.native_stepper.frame.size.height / 2 - 5,
                ),
                toView=None,
            ),
        )

    @property
    def color(self):
        return toga_color(self.native_input.textColor)

    @property
    def background_color(self):
        if self.native_input.drawsBackground:
            # Confirm the widget is bezeled
            assert self.native_input.isBezeled()
            if self.native_input.backgroundColor:
                return toga_color(self.native_input.backgroundColor)
            else:
                return None
        else:
            # Confirm the widget is not bezeled
            assert not self.native_input.isBezeled()
            return TRANSPARENT

    @property
    def font(self):
        return self.native_input.font

    @property
    def alignment(self):
        return toga_alignment(self.native_input.alignment)

    def assert_vertical_alignment(self, expected):
        # Vertical alignment isn't configurable on NSTextField
        pass

    @property
    def enabled(self):
        return self.native_input.isEnabled

    @property
    def readonly(self):
        return not self.native_input.isEditable()

    @property
    def has_focus(self):
        # When the NSTextField gets focus, a field editor is created, and that editor
        # has the original widget as the delegate. The first responder is the Field Editor.
        return isinstance(self.native.window.firstResponder, NSTextView) and (
            self.native_input.window.firstResponder.delegate == self.native_input
        )

    def set_cursor_at_end(self):
        self.native_input.currentEditor().selectedRange = NSRange(len(self.value), 0)
