from android.opengl import GLSurfaceView
from java import dynamic_proxy

from .base import Widget


class TogaGLRenderer(dynamic_proxy(GLSurfaceView.Renderer)):
    def onSurfaceCreated(self, unused, config):
        self.interface.renderer.on_init(self.interface)

    def onDrawFrame(self, unused):
        self._redraw()

    def onSurfaceChanged(self, unused, width, height):
        self._redraw()

    def _redraw(self):
        width = self.impl.native.getWidth()
        height = self.impl.native.getHeight()
        self.interface.renderer.on_render(self.interface, size=(width, height))


class OpenGLView(Widget):
    def create(self):
        self.native = GLSurfaceView(self._native_activity)
        self.renderer = TogaGLRenderer()
        self.renderer.interface = self.interface
        self.renderer.impl = self

        self.native.setEGLContextClientVersion(3)
        self.native.setRenderer(self.renderer)

    def redraw(self):
        self.native.invalidate()
