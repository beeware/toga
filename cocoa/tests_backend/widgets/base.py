import asyncio

from rubicon.objc import SEL, NSArray, NSObject, objc_method

from toga.colors import TRANSPARENT
from toga.fonts import CURSIVE, FANTASY, MONOSPACE, SANS_SERIF, SERIF, SYSTEM
from toga_cocoa.libs import NSDefaultRunLoopMode, NSRunLoop

from .properties import toga_color


class EventListener(NSObject):
    @objc_method
    def init(self):
        self.event = asyncio.Event()
        return self

    @objc_method
    def onEvent(self):
        self.event.set()
        self.event.clear()


class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

        self.event_listener = EventListener.alloc().init()

    async def post_event(self, event):
        self.native.window.postEvent(event, atStart=False)

        # Add another event to the queue behind the original event, to notify us once
        # it's been processed.
        NSRunLoop.currentRunLoop.performSelector(
            SEL("onEvent"),
            target=self.event_listener,
            argument=None,
            order=0,
            modes=NSArray.arrayWithObject(NSDefaultRunLoopMode),
        )
        await self.event_listener.event.wait()

    def assert_container(self, container):
        container_native = container._impl.native
        for control in container_native.subviews:
            if control == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    def assert_alignment(self, expected):
        assert self.alignment == expected

    def assert_font_family(self, expected):
        assert self.font.family == {
            CURSIVE: "Apple Chancery",
            FANTASY: "Papyrus",
            MONOSPACE: "Courier New",
            SANS_SERIF: "Helvetica",
            SERIF: "Times",
            SYSTEM: ".AppleSystemUIFont",
        }.get(expected, expected)

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a repaint
        self.widget.window.content._impl.native.displayIfNeeded()

        # If we're running slow, wait for a second
        if self.widget.app.run_slow:
            await asyncio.sleep(1)

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

    @property
    def background_color(self):
        if self.native.drawsBackground:
            if self.native.backgroundColor:
                return toga_color(self.native.backgroundColor)
            else:
                return None
        else:
            return TRANSPARENT

    def press(self):
        self.native.performClick(None)
