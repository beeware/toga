import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GLib, GObject  # noqa: F401, E402

# The following import will fail if WebKit or its API wrappers aren't
# installed; handle failure gracefully
# (see https://github.com/beeware/toga/issues/26)
# Accept any API version greater than 3.0
WebKit2 = None
for version in ['4.0', '3.0']:
    try:
        gi.require_version('WebKit2', version)
        from gi.repository import WebKit2  # noqa: F401, E402
        break
    except (ImportError, ValueError):
        pass

try:
    gi.require_version("Pango", "1.0")
    from gi.repository import Pango  # noqa: F401, E402
except ImportError:
    Pango = None

try:
    import cairo  # noqa: F401, E402
except ImportError:
    cairo = None
