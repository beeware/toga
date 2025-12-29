import os

import gi

gtk_version = "4.0" if os.getenv("TOGA_GTK") == "4" else "3.0"
gi.require_version("Gdk", gtk_version)
gi.require_version("Gtk", gtk_version)

# no-covering because we cannot test all DE and TOGA_GTKLIB variables in CI
# Detect the GTK DE-specific library to be used.  The TOGA_GTKLIB value will
# be prioritized, or, if no GTK4 library is specified, falls back to detecting
# with desktop environment.
if gtk_version == "4.0":  # pragma: no cover
    if os.getenv("TOGA_GTKLIB") == "Adw":
        gtklib = "Adw"
    elif os.getenv("TOGA_GTKLIB") == "None":
        gtklib = None
    elif os.getenv("TOGA_GTKLIB", "") == "":
        # No TOGA_GTKLIB specified; autodetect from DE
        if "GNOME" in os.getenv("XDG_CURRENT_DESKTOP", "").split(":"):
            gtklib = "Adw"
        else:
            gtklib = None
    else:
        # Fallback -- a specified TOGA_GTKLIB that is unsupported; use no GTK lib
        # integration for now since libadwaita would look out of place on DEs with
        # other libs (that we currently don't support).
        print(
            f"WARNING: Unsupported TOGA_GTKLIB value {os.getenv('TOGA_GTKLIB', '')!r}. "
            f"Supported values are: 'Adw', 'None'.  Defaulting to 'None'."
        )
        gtklib = None
else:  # pragma: no-cover-if-gtk4
    gtklib = None

if gtklib == "Adw":  # pragma: no-cover-unless-libadwaita
    gi.require_version("Adw", "1")
    from gi.repository import Adw  # noqa: E402, F401
# elif is used here, because explicit is better than implicit as a defensive
# practice.
elif gtklib is None:  # pragma: no-cover-unless-plain-gtk  # pragma: no branch
    Adw = None

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

GLIB_VERSION: tuple[int, int, int] = (
    GLib.MAJOR_VERSION,
    GLib.MINOR_VERSION,
    GLib.MICRO_VERSION,
)

if Adw:  # pragma: no-cover-unless-libadwaita
    ADW_VERSION: tuple[int, int, int] = (
        Adw.get_major_version(),
        Adw.get_minor_version(),
        Adw.get_micro_version(),
    )
else:  # pragma: no-cover-unless-plain-gtk
    ADW_VERSION = None

if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
    default_display = Gdk.Screen.get_default()
else:  # pragma: no-cover-if-gtk3
    from importlib import metadata

    from packaging.version import Version

    if Version(metadata.version("PyGobject")) < Version("3.52.1"):  # pragma: no cover
        raise RuntimeError(
            "GTK4 backend requires a newer version of PyGObject. "
            "Did you install `toga-gtk[gtk4]`?"
        )

    from gi._gi import hook_up_vfunc_implementation  # noqa: E402, F401

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
