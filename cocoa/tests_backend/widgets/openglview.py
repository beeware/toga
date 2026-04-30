from toga.widgets.openglview import LEFT, MIDDLE, RIGHT
from toga_cocoa.libs import NSEvent, NSEventType, NSOpenGLView, NSPoint

from .base import SimpleProbe


class OpenGLViewProbe(SimpleProbe):
    native_class = NSOpenGLView
    buttons = frozenset({LEFT, MIDDLE, RIGHT})

    async def button_state(self, buttons: frozenset, x=0, y=0):
        methods = [
            self.left_mouse_down,
            self.middle_mouse_down,
            self.right_mouse_down,
        ]
        for button in buttons:
            method = methods[button]
            await method(x, y)

    async def reset_buttons(self, x=0, y=0):
        methods = [
            self.left_mouse_up,
            self.middle_mouse_up,
            self.right_mouse_up,
        ]
        for button in frozenset(self.native.buttons):
            method = methods[button]
            await method(x, y)
        await self.redraw("Buttons cleared")

    async def position_change(self, x=0, y=0):
        await self.mouse_event(
            NSEventType.LeftMouseDragged,
            self.native.convertPoint(NSPoint((x, y)), toView=None),
        )

    async def left_mouse_down(self, x=0, y=0):
        event = self._button_event(NSEventType.LeftMouseDown)
        self.native.mouseDown_(event)
        await self.redraw("Left mouse is down")

    async def left_mouse_up(self, x=0, y=0):
        event = self._button_event(NSEventType.LeftMouseUp)
        self.native.mouseUp_(event)
        await self.redraw("Left mouse is up")

    async def middle_mouse_down(self, x=0, y=0):
        event = self._button_event(NSEventType.OtherMouseDown)
        self.native.otherMouseDown_(event)
        await self.redraw("Left mouse is down")

    async def middle_mouse_up(self, x=0, y=0):
        event = self._button_event(NSEventType.OtherMouseUp)
        self.native.otherMouseUp_(event)
        await self.redraw("Left mouse is up")

    async def right_mouse_down(self, x=0, y=0):
        event = self._button_event(NSEventType.RightMouseDown)
        self.native.rightMouseDown_(event)
        await self.redraw("Left mouse is down")

    async def right_mouse_up(self, x=0, y=0):
        event = self._button_event(NSEventType.RightMouseUp)
        self.native.rightMouseUp_(event)
        await self.redraw("Left mouse is up")

    def _button_event(self, event_type, x=0, y=0):
        return NSEvent.mouseEventWithType(
            event_type,
            location=self.native.convertPoint(NSPoint(x, y), toView=None),
            modifierFlags=0,
            timestamp=0,
            windowNumber=self.native.window.windowNumber,
            context=None,
            eventNumber=0,
            clickCount=1,
            pressure=1.0 if event_type == NSEventType.LeftMouseDown else 0.0,
        )
