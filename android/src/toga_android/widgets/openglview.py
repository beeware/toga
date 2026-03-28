from android.opengl import GLSurfaceView
from java import dynamic_proxy

from .base import Widget


class TogaGLRenderer(dynamic_proxy(GLSurfaceView.Renderer)):
    def onSurfaceCreated(self, gl_api, config):
        self.interface.renderer.on_init(self.interface)

    def onDrawFrame(self, gl_api):
        self._redraw()

    def onSurfaceChanged(self, gl_api, width, height):
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
