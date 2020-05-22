from .gtk import *  # noqa: E401, F403
from .utils import *  # noqa: E401, F403

# GDK/GTK always renders at 96dpi. When HiDPI mode is enabled, it is
# managed at the compositor level. See
# https://wiki.archlinux.org/index.php/HiDPI#GDK_3_(GTK_3) for details
DISPLAY_DPI = 96
