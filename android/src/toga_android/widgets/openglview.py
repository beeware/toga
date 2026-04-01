import weakref

from android.opengl import GLSurfaceView
from android.view import MotionEvent
from java import dynamic_proxy

from toga.widgets.openglview import TOUCH

from .base import Widget, suppress_reference_error


class TogaGLRenderer(dynamic_proxy(GLSurfaceView.Renderer)):
    def __init__(self, impl):
        super().__init__()
        self.impl = weakref.proxy(impl)
        self.interface = weakref.proxy(impl.interface)

    def onSurfaceCreated(self, gl_api, config):
        self.interface.renderer.on_init(self.interface)

    def onDrawFrame(self, gl_api):
        self._redraw()

    def onSurfaceChanged(self, gl_api, width, height):
        self._redraw()

    def _redraw(self):
        width = self.impl.native.getWidth()
        height = self.impl.native.getHeight()
        self.interface.renderer.on_render(
            self.interface,
            size=(width, height),
            pointer=self.impl.pointer,
            buttons=self.impl.buttons,
        )


class TouchListener(dynamic_proxy(GLSurfaceView.OnTouchListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = weakref.proxy(impl)
        self.interface = weakref.proxy(impl.interface)

    def onTouch(self, canvas, event):
        with suppress_reference_error():
            x, y = map(self.impl.scale_out, (event.getX(), event.getY()))
            if (action := event.getAction()) == MotionEvent.ACTION_DOWN:
                self.interface.pointer = (x, y)
                self.interface.buttons = frozenset([TOUCH])
            elif action == MotionEvent.ACTION_MOVE:
                self.interface.pointer = (x, y)
                self.interface.buttons = frozenset([TOUCH])
            elif action == MotionEvent.ACTION_UP:
                self.interface.on_release(x, y)
                self.interface.buttons = frozenset()
            else:  # pragma: no cover
                self.interface.pointer = None
                self.interface.buttons = frozenset()
        return True


class OpenGLView(Widget):
    def create(self):
        self.pointer = None
        self.buttons = frozenset()
        self.native = GLSurfaceView(self._native_activity)
        self.renderer = TogaGLRenderer(self)
        self.listener = TouchListener(self)

        self.native.setEGLContextClientVersion(3)
        self.native.setRenderer(self.renderer)

    def redraw(self):
        self.native.invalidate()
