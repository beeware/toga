import ctypes

import clr

clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms  # noqa: F401, E402

from System import (  # noqa: F401, E402
    Action,
    Convert,
    DateTime as WinDateTime,
    Environment,
    Single,
    Threading,
    Uri,
    ArgumentException,
)

from System.Drawing import (  # noqa: F401, E402
    Bitmap,
    Color,
    ContentAlignment,
    Drawing2D,
    Font as WinFont,
    FontFamily,
    FontStyle,
    Graphics,
    Icon as WinIcon,
    Image as WinImage,
    Pen,
    Point,
    PointF,
    Size,
    SolidBrush,
    StringFormat,
    SystemColors,
    SystemFonts,
    Text,
    Rectangle,
    RectangleF,
)

from System.Drawing.Drawing2D import (  # noqa: F401, E402
    FillMode,
    GraphicsPath,
    Matrix,
)

from System.Drawing.Text import PrivateFontCollection  # noqa: F401, E402

from System.IO import FileNotFoundException  # noqa: F401, E402
from System.Runtime.InteropServices import ExternalException  # noqa: F401, E402

from System.Threading.Tasks import Task  # noqa: F401, E402


user32 = ctypes.windll.user32
# shcore dll not exist on some Windows versions
# win_version should be checked to ensure proper usage
try:
    shcore = ctypes.windll.shcore
except OSError:
    shcore = None
win_version = Environment.OSVersion.Version
