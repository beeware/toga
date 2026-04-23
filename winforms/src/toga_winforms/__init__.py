import os
import platform
from pathlib import Path

import clr_loader
from pythonnet import set_runtime

try:
    ####################################################################################
    # Toga Winforms requires the use of .NET; either .NET Framework 4.x, or .NET Core.
    #
    # .NET Framework 4.x is available by default on Windows 10 and 11. However, on
    # Windows on ARM64, it is an x86-64 binary, so it can't be used by a native ARM64
    # Python interpreter.
    #
    # However, it *can* be used on ARM64 if you have an x86-64 Python interpreter -
    # which is what you get if you run `py install -3.13` or `py install -3.14`. This
    # will apparently change in Python 3.15.
    #
    # Using .NET Core requires a separate install - but it will be present on a lot of
    # systems.
    #
    # So - try to load .NET Core; if it succeeds, use it. If the load fails, fall back
    # to .NET Framework. If we're on ARM64, check to see if the interpreter is running
    # in emulation mode. If it is, we're OK; if we're not, stop the interpreter; the
    # .NET gives instructions on how to install .NET.
    #
    # But: If TOGA_WINFORMS_USE_NETFX is defined in the environment, ignore .NET Core
    # and prefer .NET Framework 4.x
    ####################################################################################
    if os.environ.get("TOGA_WINFORMS_USE_NETFX", ""):  # pragma: no-cover-if-netcore
        raise RuntimeError("Explicitly requesting .NET Framework 4.x")
    else:  # pragma: no-cover-if-netfx
        # runtime.json defines the .NET version. .NET 10 is the current LTS release.
        set_runtime(
            clr_loader.get_coreclr(
                runtime_config=Path(__file__).parent / "resources/runtime.json"
            )
        )

        # .NET Core load succeeded
        _use_dotnet_core = True
except (clr_loader.util.clr_error.ClrError, RuntimeError):  # pragma: no cover
    # .NET Core load failed. This whole branch is no-cover because we can't
    # easily describe no-cover conditions for the failure modes.
    if platform.machine() == "ARM64" and "ARM64" in platform.python_compiler():
        # If you're on a native ARM64 machine running an ARM64 Python, .NET Framework
        # 4.x isn't an option. On Python 3.10 and 3.11, an x86-64 Python running on
        # ARM64 will return `platform.machine() == "AMD64"`, so it fails the first
        # part of the test.
        raise RuntimeError("""

On Windows, Toga requires .NET Core 10. Please visit:

    https://dotnet.microsoft.com/en-us/download/dotnet/10.0

and install the .NET Desktop Runtime.""") from None
    else:
        # Either a native x86_64 machine, or an ARM64 machine with and x86_64 Python
        # interpreter in emulation mode. We can use .NET Framework 4.x
        _use_dotnet_core = False


import clr
import travertino

from .libs.user32 import SetProcessDpiAwarenessContext
from .libs.win32constants import DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2

# Add a reference to the Winforms assembly
clr.AddReference("System.Windows.Forms")

# .NET Core requires some other explicit assemblies
if _use_dotnet_core:  # pragma: no-cover-if-netfx
    clr.AddReference("Microsoft.Win32.SystemEvents")
    clr.AddReference("System.Windows.Extensions")
else:  # pragma: no-cover-if-netcore
    # We can't do conditional branch coverage, so we need a no-op else
    pass

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
