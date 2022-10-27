import ctypes

import clr

clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms  # noqa: F401, E402
from System import Action, ArgumentException, Convert  # noqa: F401, E402
from System import DateTime as WinDateTime  # noqa: F401, E402
from System import Environment, Single, String, Threading, Uri  # noqa: F401, E402
from System.Drawing import (  # noqa: F401, E402
    Bitmap,
    Color,
    ContentAlignment,
    Drawing2D,
)
from System.Drawing import Font as WinFont  # noqa: F401, E402
from System.Drawing import FontFamily, FontStyle, Graphics  # noqa: F401, E402
from System.Drawing import Icon as WinIcon  # noqa: F401, E402
from System.Drawing import Image as WinImage  # noqa: F401, E402
from System.Drawing import (  # noqa: F401, E402
    Pen,
    Point,
    PointF,
    Rectangle,
    RectangleF,
    Size,
    SolidBrush,
    StringFormat,
    SystemColors,
    SystemFonts,
    Text,
)
from System.Drawing.Drawing2D import FillMode  # noqa: F401, E402
from System.Drawing.Drawing2D import GraphicsPath, Matrix  # noqa: F401, E402
from System.Drawing.Text import PrivateFontCollection  # noqa: F401, E402
from System.IO import FileNotFoundException, MemoryStream  # noqa: F401, E402
from System.Net import SecurityProtocolType  # noqa: F401, E402
from System.Net import ServicePointManager  # noqa: F401, E402
from System.Runtime.InteropServices import ExternalException  # noqa: F401, E402
from System.Threading.Tasks import Task, TaskScheduler  # noqa: F401, E402

user32 = ctypes.windll.user32
# shcore dll not exist on some Windows versions
# win_version should be checked to ensure proper usage
try:
    shcore = ctypes.windll.shcore
except OSError:
    shcore = None
win_version = Environment.OSVersion.Version
