from toga_iOS.widgets.openglview import TogaGLKView

from .base import SimpleProbe


class OpenGLViewProbe(SimpleProbe):
    native_class = TogaGLKView
