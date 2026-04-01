from rubicon.objc import NSObject, NSPoint, ObjCClass, objc_method

from toga.widgets.openglview import TOUCH
from toga_iOS.widgets.openglview import TogaGLKView

from .base import SimpleProbe

# Touch events generate a Set of 1 event.
NSSet = ObjCClass("NSSet")


# UITouch objects can't be instantiated; but we only care about 1 method, so
# create a mock that satisfies our needs.
class MockTouch(NSObject):
    @objc_method
    def locationInView(self, view) -> NSPoint:
        return self.position


class OpenGLViewProbe(SimpleProbe):
    native_class = TogaGLKView
    buttons = frozenset({TOUCH})

    async def button_state(self, buttons: frozenset, x=0, y=0):
        if TOUCH in buttons:
            await self.touch_down(x, y)

    async def reset_buttons(self, buttons: frozenset, x=0, y=0):
        await self.touch_up(x, y)
        await self.redraw("Touch cleared")

    async def touch_down(self, x, y):
        touch = MockTouch.alloc().init()
        touches = NSSet.setWithObject(touch)

        touch.position = NSPoint(x, y)
        self.native.touchesBegan(touches, withEvent=None)

    async def touch_move(self, x, y):
        touch = MockTouch.alloc().init()
        touches = NSSet.setWithObject(touch)

        touch.position = NSPoint(x, y)
        self.native.touchesMoved(touches, withEvent=None)

    async def touch_up(self, x, y):
        touch = MockTouch.alloc().init()
        touches = NSSet.setWithObject(touch)

        touch.position = NSPoint(x, y)
        self.native.touchesEnded(touches, withEvent=None)
