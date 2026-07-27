from ctypes import WinError
from importlib.metadata import version
from sys import getwindowsversion
from warnings import warn

from win32more.Windows.Win32.Foundation import ERROR_ACCESS_DENIED, GetLastError
from win32more.Windows.Win32.UI.HiDpi import (
    DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2,
    SetProcessDpiAwarenessContext,
)

if getwindowsversion().build < 17763:  # pragma: no cover
    # https://learn.microsoft.com/en-us/windows/apps/winui/winui3/
    raise WinError(
        descr="WinUI 3 only runs on Windows 10, version 1809 (build 17763) and later."
    )


# Set the application to be aware of per-monitor dpi values.
success = SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)


# According to the Microsoft documentation, if SetProcessDpiAwarenessContext fails with
# ERROR_ACCESS_DENIED, then the ProcessDpiAwarenessContext has already been set.
if not success:  # pragma: no cover
    dpi_error = GetLastError()
    if dpi_error == ERROR_ACCESS_DENIED:
        warn(
            "SetProcessDpiAwarenessContext has been set twice.",
            stacklevel=1,
        )
    else:
        warn(
            f"SetProcessDpiAwarenessContext failed with error code {dpi_error}.",
            stacklevel=1,
        )


__version__ = version("toga-winui3")
