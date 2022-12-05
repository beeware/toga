import ctypes

import clr

clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms  # noqa: F401, E402
from System import (  # noqa: F401, E402
    Action,
    ArgumentException,
    Convert,
    DateTime as WinDateTime,
    Environment,
    Single,
    String,
    Threading,
    Uri,
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
from System.Drawing.Imaging import ImageFormat  # noqa: F401, E402
from System.Drawing.Text import PrivateFontCollection  # noqa: F401, E402
from System.Globalization import CultureInfo  # noqa: F401, E402
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
