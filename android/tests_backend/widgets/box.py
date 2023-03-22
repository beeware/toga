from java import jclass

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = jclass("android.widget.RelativeLayout")
