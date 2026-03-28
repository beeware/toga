from android.opengl import GLSurfaceView

from .base import SimpleProbe


class OpenGLViewProbe(SimpleProbe):
    native_class = GLSurfaceView
