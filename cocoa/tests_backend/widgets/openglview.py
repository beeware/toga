from toga_cocoa.libs import NSOpenGLView

from .base import SimpleProbe


class OpenGLViewProbe(SimpleProbe):
    native_class = NSOpenGLView
