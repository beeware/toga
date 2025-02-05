import os

import gi

gtk_version = "4.0" if os.getenv("TOGA_GTK") == "4" else "3.0"
gi.require_version("Gdk", gtk_version)
gi.require_version("Gtk", gtk_version)

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

GTK_VERSION: tuple[int, int, int] = (
    Gtk.get_major_version(),
    Gtk.get_minor_version(),
    Gtk.get_micro_version(),
)

if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
    default_display = Gdk.Screen.get_default()
else:  # pragma: no-cover-if-gtk3
    default_display = Gdk.Display.get_default()
if default_display is None:  # pragma: no cover
    raise RuntimeError(
        "Cannot identify an active display. Is the `DISPLAY` "
        "environment variable set correctly?"
    )

IS_WAYLAND = not isinstance(Gdk.Display.get_default(), GdkX11.X11Display)

# The following imports will fail if the underlying libraries or their API
# wrappers aren't installed; handle failure gracefully (see
# https://github.com/beeware/toga/issues/26)
if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
    try:
        try:
            gi.require_version("WebKit2", "4.1")
        except ValueError:  # pragma: no cover
            gi.require_version("WebKit2", "4.0")
        from gi.repository import WebKit2  # noqa: F401
    except (ImportError, ValueError):  # pragma: no cover
        WebKit2 = None
else:  # pragma: no-cover-if-gtk3
    try:
        gi.require_version("WebKit", "6.0")
        from gi.repository import WebKit as WebKit2  # noqa: F401
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

try:
    gi.require_version("Geoclue", "2.0")
    from gi.repository import Geoclue  # noqa: F401
except (ImportError, ValueError):  # pragma: no cover
    Geoclue = None

try:
    gi.require_version("Flatpak", "1.0")
    from gi.repository import Flatpak  # noqa: F401
except (ImportError, ValueError):  # pragma: no cover
    Flatpak = None
