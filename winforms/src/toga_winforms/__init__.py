import clr
import travertino

from .libs.user32 import (
    DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2,
    SetProcessDpiAwarenessContext,
)

# Add a reference to the Winforms assembly
clr.AddReference("System.Windows.Forms")

# Add a reference to the WindowsBase assembly. This is needed to access
# System.Windows.Threading.Dispatcher.
#
# This assembly isn't exposed as a simple dot-path name; we have to extract it from the
# Global Assembly Cache (GAC). The version number and public key doesn't appear to
# change with Windows version or the underlying .NET, and has been available since
# Windows 7.
clr.AddReference(
    "WindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
)


# Enable DPI awareness. This must be done before calling any other UI-related code
# (https://learn.microsoft.com/en-us/dotnet/desktop/winforms/high-dpi-support-in-windows-forms).
import System.Windows.Forms as WinForms  # noqa: E402

WinForms.Application.EnableVisualStyles()
WinForms.Application.SetCompatibleTextRenderingDefault(False)

if SetProcessDpiAwarenessContext is not None:
    if not SetProcessDpiAwarenessContext(
        DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
    ):  # pragma: no cover
        print("WARNING: Failed to set the DPI Awareness mode for the app.")

__version__ = travertino._package_version(__file__, __name__)
