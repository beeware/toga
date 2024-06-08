from rubicon.objc import NSPoint

from toga.colors import TRANSPARENT
from toga_cocoa.keys import NSEventModifierFlagCommand, NSEventModifierFlagShift
from toga_cocoa.libs import NSEvent, NSEventType

from ..fonts import FontMixin
from ..probe import BaseProbe
from .properties import toga_color


class SimpleProbe(BaseProbe, FontMixin):
    def __init__(self, widget):
        super().__init__()
        self.app = widget.app
        self.window = widget.window
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        assert container._impl.container == self.impl.container
        container_native = container._impl.container.native
        for control in container_native.subviews:
            if control == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.superview is None
        assert self.native.window is None

    def assert_alignment(self, expected):
        assert self.alignment == expected

    async def redraw(self, message=None, delay=0):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a widget repaint
        self.widget.window.content._impl.native.displayIfNeeded()

        await super().redraw(message=message, delay=delay)

    @property
    def enabled(self):
        return self.native.isEnabled

    @property
    def hidden(self):
        return self.native.hidden

    @property
    def width(self):
        return self.native.frame.size.width

    @property
    def height(self):
        return self.native.frame.size.height

    @property
    def shrink_on_resize(self):
        return True

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.widget._impl.container is not None
        assert self.native.superview is not None
        assert self.native.window is not None

        # size and position is as expected.
        assert (self.native.frame.size.width, self.native.frame.size.height) == size
        assert (self.native.frame.origin.x, self.native.frame.origin.y) == position

    def assert_width(self, min_width, max_width):
        assert (
            min_width <= self.width <= max_width
        ), f"Width ({self.width}) not in range ({min_width}, {max_width})"

    def assert_height(self, min_height, max_height):
        assert (
            min_height <= self.height <= max_height
        ), f"Height ({self.height}) not in range ({min_height}, {max_height})"

    @property
    def background_color(self):
        if self.native.drawsBackground:
            if self.native.backgroundColor:
                return toga_color(self.native.backgroundColor)
            else:
                return None
        else:
            return TRANSPARENT

    @property
    def font(self):
        return self.native.font

    async def press(self):
        self.native.performClick(None)

    @property
    def is_hidden(self):
        return self.native.isHidden()

    @property
    def has_focus(self):
        return self.native.window.firstResponder == self.native

    async def type_character(self, char, modifierFlags=0):
        # Convert the requested character into a Cocoa keycode.
        # This table is incomplete, but covers all the basics.
        key_code = {
            "<backspace>": 51,
            "<esc>": 53,
            " ": 49,
            "\n": 36,
            "a": 0,
            "b": 11,
            "c": 8,
            "d": 2,
            "e": 14,
            "f": 3,
            "g": 5,
            "h": 4,
            "i": 34,
            "j": 38,
            "k": 40,
            "l": 37,
            "m": 46,
            "n": 45,
            "o": 31,
            "p": 35,
            "q": 12,
            "r": 15,
            "s": 1,
            "t": 17,
            "u": 32,
            "v": 9,
            "w": 13,
            "x": 7,
            "y": 16,
            "z": 6,
        }.get(char.lower(), 0)

        if modifierFlags:
            char = None

        # This posts a single keyDown followed by a keyUp, matching "normal" keyboard operation.
        await self.post_event(
            NSEvent.keyEventWithType(
                NSEventType.KeyDown,
                location=NSPoint(0, 0),  # key presses don't have a location.
                modifierFlags=modifierFlags,
                timestamp=0,
                windowNumber=self.native.window.windowNumber,
                context=None,
                characters=char,
                charactersIgnoringModifiers=char,
                isARepeat=False,
                keyCode=key_code,
            ),
        )
        await self.post_event(
            NSEvent.keyEventWithType(
                NSEventType.KeyUp,
                location=NSPoint(0, 0),  # key presses don't have a location.
                modifierFlags=modifierFlags,
                timestamp=0,
                windowNumber=self.native.window.windowNumber,
                context=None,
                characters=char,
                charactersIgnoringModifiers=char,
                isARepeat=False,
                keyCode=key_code,
            ),
        )

    async def mouse_event(
        self,
        event_type,
        location,
        delay=None,
        modifierFlags=0,
        clickCount=1,
    ):
        await self.post_event(
            NSEvent.mouseEventWithType(
                event_type,
                location=location,
                modifierFlags=modifierFlags,
                timestamp=0,
                windowNumber=self.native.window.windowNumber,
                context=None,
                eventNumber=0,
                clickCount=clickCount,
                pressure=1.0 if event_type == NSEventType.LeftMouseDown else 0.0,
            ),
            delay=delay,
        )

    async def undo(self):
        await self.type_character("z", modifierFlags=NSEventModifierFlagCommand)

    async def redo(self):
        await self.type_character(
            "z", modifierFlags=NSEventModifierFlagCommand | NSEventModifierFlagShift
        )
