import pytest
from rubicon.objc import ObjCClass

from toga_iOS.libs import UIApplication

from ..fonts import FontMixin
from ..probe import BaseProbe
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


CATransaction = ObjCClass("CATransaction")


class SimpleProbe(BaseProbe, FontMixin):
    native_attr = "native"

    def __init__(self, widget):
        super().__init__()
        self.app = widget.app
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        assert isinstance(getattr(self.impl, self.native_attr), self.native_class)

    def assert_container(self, container):
        assert container._impl.container == self.impl.container

        container_native = container._impl.container.native
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

    async def redraw(self, message=None, delay=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a widget repaint
        self.widget.window.content._impl.native.layer.displayIfNeeded()

        # Flush CoreAnimation; this ensures all animations are complete
        # and all constraints have been evaluated.
        CATransaction.flush()

        await super().redraw(message=message, delay=delay)

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
        height = self.native.frame.size.height
        # If the widget is the top level container, the frame height will
        # include the allocation for the app titlebar.
        if self.impl.container is None:
            height = height - self.impl.viewport.top_offset
        return height

    @property
    def shrink_on_resize(self):
        return True

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.widget._impl.container is not None
        assert self.native.superview() is not None

        # size and position is as expected.
        assert (self.native.frame.size.width, self.native.frame.size.height) == size

        # Allow for the status bar and navigation bar in vertical position
        statusbar_frame = UIApplication.sharedApplication.statusBarFrame
        nav_controller = self.widget.window._impl.native.rootViewController
        navbar_frame = nav_controller.navigationBar.frame
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

    @property
    def font(self):
        return self.native.font

    async def press(self):
        self.native.sendActionsForControlEvents(UIControlEventTouchDown)

    @property
    def is_hidden(self):
        return self.native.isHidden()

    @property
    def has_focus(self):
        return self.native.isFirstResponder

    def type_return(self):
        self.native.insertText("\n")

    def _prevalidate_input(self, char):
        return True

    async def type_character(self, char):
        if char == "<esc>":
            # There's no analog of esc on iOS
            pass
        elif char == "\n":
            self.type_return()
        else:
            # Perform any prevalidation that is required. If the input isn't
            # valid, do a dummy "empty" insertion.
            valid = self._prevalidate_input(char)
            if valid:
                self.native.insertText(char)
            else:
                self.native.insertText("")

    async def undo(self):
        pytest.skip("Undo not supported on this platform")

    async def redo(self):
        pytest.skip("Redo not supported on this platform")
