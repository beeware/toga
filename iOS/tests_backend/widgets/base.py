import asyncio

from toga.fonts import CURSIVE, FANTASY, MONOSPACE, SANS_SERIF, SERIF, SYSTEM
from toga_iOS.libs import NSRunLoop, UIApplication

from .properties import toga_color

# From UIControl.h
UIControlEventTouchDown = 1 << 0
UIControlEventTouchDownRepeat = 1 << 1
UIControlEventTouchDragInside = 1 << 2
UIControlEventTouchDragOutside = 1 << 3
UIControlEventTouchDragEnter = 1 << 4
UIControlEventTouchDragExit = 1 << 5
UIControlEventTouchUpInside = 1 << 6
UIControlEventTouchUpOutside = 1 << 7
UIControlEventTouchCancel = 1 << 8
UIControlEventValueChanged = 1 << 12  # sliders, etc.
UIControlEventPrimaryActionTriggered = 1 << 13  # semantic action: for buttons, etc.
UIControlEventMenuActionTriggered = (
    1 << 14
)  # triggered when the menu gesture fires but before the menu presents

UIControlEventEditingDidBegin = 1 << 16  # UITextField
UIControlEventEditingChanged = 1 << 17
UIControlEventEditingDidEnd = 1 << 18
UIControlEventEditingDidEndOnExit = 1 << 19  # 'return key' ending editing

UIControlEventAllTouchEvents = 0x00000FFF  # for touch events
UIControlEventAllEditingEvents = 0x000F0000  # for UITextField
UIControlEventApplicationReserved = 0x0F000000  # range available for application use
UIControlEventSystemReserved = 0xF0000000  # range reserved for internal framework use
UIControlEventAllEvents = 0xFFFFFFFF


class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        container_native = container._impl.native
        for control in container_native.subviews():
            if control == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.superview() is None

    def assert_alignment(self, expected):
        assert self.alignment == expected

    def assert_font_family(self, expected):
        assert self.font.family == {
            CURSIVE: "Apple Chancery",
            FANTASY: "Papyrus",
            MONOSPACE: "Courier New",
            SANS_SERIF: "Helvetica",
            SERIF: "Times New Roman",
            SYSTEM: ".AppleSystemUIFont",
        }.get(expected, expected)

    async def redraw(self, message=None, delay=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a repaint
        self.widget.window.content._impl.native.layer.displayIfNeeded()

        # If we're running slow, wait for a second
        if self.widget.app.run_slow:
            print("Waiting for redraw" if message is None else message)
            delay = 1

        if delay:
            await asyncio.sleep(delay)
        else:
            # Running at "normal" speed, we need to release to the event loop
            # for at least one iteration. `runUntilDate:None` does this.
            NSRunLoop.currentRunLoop.runUntilDate(None)

    @property
    def enabled(self):
        return self.native.isEnabled()

    @property
    def hidden(self):
        return self.native.hidden

    @property
    def width(self):
        return self.native.frame.size.width

    @property
    def height(self):
        return self.native.frame.size.height

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.widget._impl.container is not None
        assert self.native.superview() is not None

        # size and position is as expected.
        assert (self.native.frame.size.width, self.native.frame.size.height) == size

        # Allow for the status bar and navigation bar in vertical position
        statusbar_frame = UIApplication.sharedApplication.statusBarFrame
        navbar = self.widget.window._impl.controller.navigationController
        navbar_frame = navbar.navigationBar.frame
        offset = statusbar_frame.size.height + navbar_frame.size.height
        assert (
            self.native.frame.origin.x,
            self.native.frame.origin.y - offset,
        ) == position

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
        return toga_color(self.native.backgroundColor)

    async def press(self):
        self.native.sendActionsForControlEvents(UIControlEventTouchDown)

    @property
    def is_hidden(self):
        return self.native.isHidden()

    @property
    def has_focus(self):
        return self.native.isFirstResponder

    async def type_character(self, char):
        self.native.insertText(char)
