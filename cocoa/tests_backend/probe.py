import asyncio
from ctypes import c_void_p

from rubicon.objc import SEL, NSArray, NSObject, ObjCClass, objc_method
from rubicon.objc.api import NSString

import toga
from toga_cocoa.libs.appkit import appkit

NSRunLoop = ObjCClass("NSRunLoop")
NSRunLoop.declare_class_property("currentRunLoop")
NSDefaultRunLoopMode = NSString(c_void_p.in_dll(appkit, "NSDefaultRunLoopMode"))


class EventListener(NSObject):
    @objc_method
    def init(self):
        self.event = asyncio.Event()
        return self

    @objc_method
    def onEvent(self):
        self.event.set()
        self.event.clear()


class BaseProbe:
    def __init__(self):
        self.event_listener = EventListener.alloc().init()

    async def post_event(self, event, delay=None):
        self.window._impl.native.postEvent(event, atStart=False)

        if delay is not None:
            # Some widgets enter an internal runloop when processing certain events;
            # this lets the internal runloop finish properly, since the onEvent approach
            # of the *current* runloop will not work.
            await asyncio.sleep(delay)
        else:
            # Add another event to the queue behind the original event, to notify us
            # once it's been processed.
            NSRunLoop.currentRunLoop.performSelector(
                SEL("onEvent"),
                target=self.event_listener,
                argument=None,
                order=0,
                modes=NSArray.arrayWithObject(NSDefaultRunLoopMode),
            )
            await self.event_listener.event.wait()

    async def redraw(self, message=None, delay=0, wait_for=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # If we're running slow, or we have a wait condition,
        # wait for at least a second
        if toga.App.app.run_slow or wait_for:
            delay = max(1, delay)

        if delay or wait_for:
            print("Waiting for redraw" if message is None else message)
            if toga.App.app.run_slow or wait_for is None:
                await asyncio.sleep(delay)
            else:
                delta = 0.1
                interval = 0.0
                while not wait_for() and interval < delay:
                    await asyncio.sleep(delta)
                    interval += delta

        else:
            # Running at "normal" speed, we need to release to the event loop
            # for at least one iteration. `runUntilDate:None` does this.
            NSRunLoop.currentRunLoop.runUntilDate(None)

    def assert_image_size(self, image_size, size, screen, window=None):
        # Screenshots are captured in native device resolution, not in CSS pixels.
        scale = int(screen._impl.native.backingScaleFactor)
        assert image_size == (size[0] * scale, size[1] * scale)
