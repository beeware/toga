import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk  # noqa: E402, F401

try:
    gi.require_version("WebKit2", "4.0")
    from gi.repository import WebKit2  # noqa: F401

except ImportError:  # pragma: no cover
    WebKit2 = None

try:
    gi.require_version("Pango", "1.0")
    from gi.repository import Pango
except ImportError:  # pragma: no cover
    Pango = None

try:
    import cairo
except ImportError:  # pragma: no cover
    cairo = None
