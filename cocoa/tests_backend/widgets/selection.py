from pytest import xfail
from rubicon.objc import NSPoint

from toga_cocoa.libs import NSEventType, NSPopUpButton

from .base import SimpleProbe


class SelectionProbe(SimpleProbe):
    native_class = NSPopUpButton

    def assert_resizes_on_content_change(self):
        pass

    @property
    def alignment(self):
        xfail("Can't change the alignment of Selection on macOS")

    @property
    def color(self):
        xfail("Can't change the color of Selection on macOS")

    @property
    def font(self):
        xfail("Can't change the font of Selection on macOS")

    @property
    def background_color(self):
        xfail("Can't change the background color of Selection on macOS")

    @property
    def titles(self):
        return [str(title) for title in self.native.itemTitles]

    @property
    def selected_title(self):
        title = self.native.titleOfSelectedItem
        return str(title) if title else None

    async def select_item(self):
        point = self.native.convertPoint(
            NSPoint(self.width / 2, self.height / 2), toView=None
        )
        # Selection maintains an inner mouse event loop, so we can't
        # use the "wait for another event" approach for the mouse events.
        # Use a short delaly instead.
        await self.mouse_event(NSEventType.LeftMouseDown, point, delay=0.1)

        self.native.menu.performActionForItemAtIndex(1)
        self.native.menu.cancelTracking()
