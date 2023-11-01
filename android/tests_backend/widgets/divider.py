from java import jclass

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = jclass("android.view.View")
