from win32more.Microsoft.UI.Xaml.Controls import Canvas

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = Canvas
