from android.opengl import GLSurfaceView
from android.os import SystemClock
from android.view import MotionEvent

from toga.widgets.openglview import TOUCH

from .base import SimpleProbe


class OpenGLViewProbe(SimpleProbe):
    native_class = GLSurfaceView
    buttons = frozenset({TOUCH})

    async def button_state(self, buttons: frozenset, x=0, y=0):
        if TOUCH in buttons:
            await self.touch_down(x, y)

    async def reset_buttons(self, x=0, y=0):
        await self.touch_up(x, y)
        await self.redraw("Touch cleared")

    async def position_change(self, x=0, y=0):
        self.motion_event(MotionEvent.ACTION_MOVE, x, y)

    def motion_event(self, action, x, y):
        time = SystemClock.uptimeMillis()
        super().motion_event(
            time, time, action, x * self.scale_factor, y * self.scale_factor
        )

    async def touch_down(self, x, y):
        self.motion_event(MotionEvent.ACTION_DOWN, x, y)

    async def touch_up(self, x, y):
        self.motion_event(MotionEvent.ACTION_UP, x, y)
