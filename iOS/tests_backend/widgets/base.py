from pytest import skip

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
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        container_native = container._impl.native
        for control in container_native.subviews():
            if control == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Refresh the layout
        self.widget.window.content.refresh()
        # Force a repaint
        #        self.widget.window.content._impl.native.layer.setNeedsDisplay_(True)
        self.widget.window.content._impl.native.layer.displayIfNeeded()

    @property
    def enabled(self):
        return self.native.enabled

    @property
    def hidden(self):
        return self.native.hidden

    @property
    def width(self):
        return self.native.frame.size.width

    @property
    def height(self):
        return self.native.frame.size.height

    def press(self):
        skip("Can't simulate button presses yet")
        # ?? self.native.sendActionsForControlEvents(UIControlEventTouchUpInside)
