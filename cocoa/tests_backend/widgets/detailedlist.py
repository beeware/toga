import asyncio
from ctypes import c_int64, c_uint32, c_uint64

from rubicon.objc import CGPoint, NSPoint

from toga_cocoa.libs import (
    CGEventRef,
    NSEvent,
    NSEventType,
    NSScrollView,
    NSTableView,
    core_graphics,
    kCGScrollEventUnitPixel,
)

from .base import SimpleProbe

NSEventModifierFlagCommand = 1 << 20

kCGScrollWheelEventScrollPhase = 99
kCGScrollWheelEventMomentumPhase = 123

kCGScrollPhaseBegan = 1
kCGMomentumScrollPhaseBegin = 1

CGEventField = c_uint32
CGEventFlags = c_uint64

core_graphics.CGEventSetLocation.argtypes = [CGEventRef, CGPoint]
core_graphics.CGEventSetLocation.restype = None

core_graphics.CGEventSetFlags.argtypes = [CGEventRef, CGEventFlags]
core_graphics.CGEventSetFlags.restype = None

core_graphics.CGEventSetIntegerValueField.argtypes = [CGEventRef, CGEventField, c_int64]
core_graphics.CGEventSetIntegerValueField.restype = None


class DetailedListProbe(SimpleProbe):
    native_class = NSScrollView
    supports_actions = True
    supports_refresh = True

    def __init__(self, widget):
        super().__init__(widget)
        self.native_detailedlist = widget._impl.native_detailedlist
        assert isinstance(self.native_detailedlist, NSTableView)

    @property
    def row_count(self):
        return int(
            self.native_detailedlist.numberOfRowsInTableView(self.native_detailedlist)
        )

    def assert_cell_content(self, row, title, subtitle, icon=None):
        data = self.native_detailedlist.tableView(
            self.native_detailedlist,
            objectValueForTableColumn=self.native_detailedlist.tableColumns[0],
            row=row,
        )
        assert str(data.attrs["title"]) == title
        assert str(data.attrs["subtitle"]) == subtitle

        if icon:
            assert data.attrs["icon"] == icon._impl.native
        else:
            assert data.attrs["icon"] is None

    @property
    def max_scroll_position(self):
        return int(self.native.documentView.bounds.size.height) - int(
            self.native.contentView.bounds.size.height
        )

    @property
    def scroll_position(self):
        return int(self.native.contentView.bounds.origin.y)

    def scroll_to_top(self):
        self.native.contentView.scrollToPoint(
            NSPoint(self.native.contentView.documentView.frame.origin.x, 0)
        )
        self.native.reflectScrolledClipView(self.native.contentView)

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    def row_position(self, row):
        # Pick a point half way across horizontally, and half way down the row,
        # taking into account the size of the rows and the header
        row_height = self.native_detailedlist.tableView(
            self.native_detailedlist, heightOfRow=row
        )
        return self.native_detailedlist.convertPoint(
            NSPoint(
                self.width / 2,
                (row * row_height) + (row_height / 2),
            ),
            toView=None,
        )

    async def select_row(self, row, add=False):
        point = self.row_position(row)
        # Table maintains an inner mouse event loop, so we can't
        # use the "wait for another event" approach for the mouse events.
        # Use a short delay instead.
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            point,
            delay=0.1,
            modifierFlags=NSEventModifierFlagCommand if add else 0,
        )
        await self.mouse_event(
            NSEventType.LeftMouseUp,
            point,
            delay=0.1,
            modifierFlags=NSEventModifierFlagCommand if add else 0,
        )

    async def _refresh_action(self, offset):
        # Create a scroll event where event phase = Began, Momenum scroll phase = Begin,
        # and the pixel value is equal to the requested offset.
        cg_event = core_graphics.CGEventCreateScrollWheelEvent(
            None, kCGScrollEventUnitPixel, 2, offset, 0
        )
        core_graphics.CGEventSetLocation(
            cg_event,
            self.native_detailedlist.convertPoint(NSPoint(200, 200), toView=None),
        )
        core_graphics.CGEventSetFlags(cg_event, 0)

        core_graphics.CGEventSetIntegerValueField(
            cg_event,
            kCGScrollWheelEventScrollPhase,
            kCGScrollPhaseBegan,
        )
        core_graphics.CGEventSetIntegerValueField(
            cg_event,
            kCGScrollWheelEventMomentumPhase,
            kCGMomentumScrollPhaseBegin,
        )

        ns_event = NSEvent.eventWithCGEvent(cg_event)

        # Scroll the view to the position where
        self.native.contentView.scrollToPoint(NSPoint(0, -offset))
        self.native.reflectScrolledClipView(self.native.contentView)

        self.native_detailedlist.scrollWheel(ns_event)

        # Ensure the refresh indicator is hidden if there is no refresh handler.
        is_disabled = self.widget.on_refresh._raw is None
        assert self.native.refresh_indicator.isHidden() == is_disabled

    def refresh_available(self):
        return self.scroll_position <= 0

    async def non_refresh_action(self):
        # 20px is enough to be visible, but not enough
        await self._refresh_action(20)
        # Simulate a short delay before releasing the pull-to-refresh
        await asyncio.sleep(0.1)
        self.scroll_to_top()

    async def refresh_action(self, active=True):
        # 50px is enough to trigger a refresh
        await self._refresh_action(50)

        if not active:
            assert self.native.refresh_indicator.isHidden()
            # If refresh is disabled, simulate a short delay before releasing the
            # pull-to-refresh
            await asyncio.sleep(0.1)
            self.scroll_to_top()
        else:
            assert not self.native.refresh_indicator.isHidden()
            # Wait for the scroll to relax after reload completion
            while self.scroll_position < 0:
                await asyncio.sleep(0.01)

    async def _perform_action(self, row, index):
        point = self.row_position(row)

        # Click to show menu
        await self.mouse_event(
            NSEventType.RightMouseDown,
            point,
            delay=0.1,
        )
        await self.redraw("Action menu has been displayed")

        popup = self.impl._popup
        if popup:
            popup.performActionForItemAtIndex(index)
            popup.cancelTracking()

            # Wait until the popup menu is fully disposed.
            while self.impl._popup is not None:
                await self.redraw("Action has been selected", delay=0.1)

    async def perform_primary_action(self, row, active=True):
        await self._perform_action(row, 0)

    async def perform_secondary_action(self, row, active=True):
        await self._perform_action(row, 1 if self.impl.primary_action_enabled else 0)
