from toga_qt.widgets.openglview import TogaOpenGLWidget

from .base import SimpleProbe


class OpenGLViewProbe(SimpleProbe):
    native_class = TogaOpenGLWidget
