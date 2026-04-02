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
        native = self.impl.native
        width = native.getWidth()
        height = native.getHeight()
        # Pointer coordinates are in device-independent, top-left origin coords
        # We need drawing pixel, bottom-left origin coordinates
        scale = native.getContext().getResources().getDisplayMetrics().densityDpi / 160
        pointer = self.impl.pointer
        if pointer:
            x, y = pointer
            pointer = (scale * x, height - (scale * y))
        self.interface.renderer.on_render(
            self.interface,
            size=(width, height),
            pointer=pointer,
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
            self.impl.pointer = (x, y)
            if (action := event.getAction()) == MotionEvent.ACTION_DOWN:
                self.impl.buttons = frozenset([TOUCH])
            elif action == MotionEvent.ACTION_MOVE:
                self.impl.buttons = frozenset([TOUCH])
            elif action == MotionEvent.ACTION_UP:
                self.impl.buttons = frozenset()
            else:  # pragma: no cover
                self.impl.buttons = frozenset()
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
        self.native.setOnTouchListener(self.listener)

    def redraw(self):
        self.native.invalidate()
