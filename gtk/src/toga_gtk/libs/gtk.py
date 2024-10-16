import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from gi.events import GLibEventLoopPolicy  # noqa: E402, F401
from gi.repository import (  # noqa: E402, F401
    Gdk,
    GdkPixbuf,
    GdkX11,
    Gio,
    GLib,
    GObject,
    Gtk,
)

if Gdk.Screen.get_default() is None:  # pragma: no cover
    raise RuntimeError(
        "Cannot identify an active display. Is the `DISPLAY` environment variable set correctly?"
    )

IS_WAYLAND = not isinstance(Gdk.Display.get_default(), GdkX11.X11Display)

# The following imports will fail if the underlying libraries or their API
# wrappers aren't installed; handle failure gracefully (see
# https://github.com/beeware/toga/issues/26)
try:
    try:
        gi.require_version("WebKit2", "4.1")
    except ValueError:  # pragma: no cover
        gi.require_version("WebKit2", "4.0")
    from gi.repository import WebKit2  # noqa: F401
except (ImportError, ValueError):  # pragma: no cover
    WebKit2 = None

try:
    gi.require_version("Pango", "1.0")
    from gi.repository import Pango  # noqa: F401
except (ImportError, ValueError):  # pragma: no cover
    Pango = None

try:
    import cairo  # noqa: F401

    gi.require_foreign("cairo")
except ImportError:  # pragma: no cover
    cairo = None

try:
    gi.require_version("PangoCairo", "1.0")
    from gi.repository import PangoCairo  # noqa: F401
except (ImportError, ValueError):  # pragma: no cover
    PangoCairo = None

try:
    gi.require_version("PangoFc", "1.0")
    from gi.repository import PangoFc  # noqa: F401
except (ImportError, ValueError):  # pragma: no cover
    PangoFc = None

try:
    gi.require_version("XApp", "1.0")
    from gi.repository import XApp  # noqa: F401
except (ImportError, ValueError):  # pragma: no cover
    XApp = None
