import ctypes

import clr

clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms  # noqa: F401, E402
from System import (
    Action,
    ArgumentException,
    Convert,
)
from System import DateTime as WinDateTime  # noqa: F401, E402
from System import (
    Environment,
    Single,
    String,
    Threading,
    Uri,
)
from System.Drawing import (
    Bitmap,
    Color,
    ContentAlignment,
    Drawing2D,
)
from System.Drawing import Font as WinFont  # noqa: F401, E402
from System.Drawing import (
    FontFamily,
    FontStyle,
    Graphics,
)
from System.Drawing import Icon as WinIcon
from System.Drawing import Image as WinImage
from System.Drawing import (
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
from System.Drawing.Drawing2D import (  # noqa: F401, E402
    FillMode,
    GraphicsPath,
    Matrix,
)
from System.Drawing.Text import PrivateFontCollection  # noqa: F401, E402
from System.IO import FileNotFoundException, MemoryStream  # noqa: F401, E402
from System.Net import SecurityProtocolType, ServicePointManager  # noqa: F401, E402
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
