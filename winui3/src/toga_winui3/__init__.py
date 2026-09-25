import platform
from ctypes import WinError
from importlib.metadata import version
from sys import getwindowsversion
from warnings import warn

from win32more.Windows.Management.Deployment import PackageManager
from win32more.Windows.Win32.Foundation import ERROR_ACCESS_DENIED, GetLastError, hstr
from win32more.Windows.Win32.UI.HiDpi import (
    DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2,
    SetProcessDpiAwarenessContext,
)

if getwindowsversion().build < 17763:  # pragma: no cover
    # https://learn.microsoft.com/en-us/windows/apps/winui/winui3/
    raise WinError(
        descr="WinUI 3 only runs on Windows 10, version 1809 (build 17763) and later."
    )


# Get the architecture used by the python interpreter.
# Put no cover on all the branches since there are both ARM64 and x64 CI testbeds, and
# leaving any branch without no cover would lead to a reported a gap in coverage.
if platform.architecture()[0] == "64bit":  # pragma: no cover
    if "ARM64" in platform.python_compiler():
        arch = "arm64"
    else:
        arch = "x64"
else:  # pragma: no cover
    arch = "x86"


runtime_verison = "2.3.1.0"
runtime_desc = f"Microsoft Windows App Runtime DDLM 2 ({runtime_verison} {arch} )"


# Check that the Microsoft Windows App Runtime is installed.
for package in PackageManager().FindPackagesByUserSecurityId(hstr("")):
    if package.Description == runtime_desc:
        break
else:  # pragma: no cover
    raise RuntimeError(
        "\n\nFor use with the current python interpreter, Toga on WinUI 3 requires "
        + f"Microsoft Windows App Runtime version {runtime_verison} for {arch}. "
        + "This can be downloaded from:\n\n"
        + "https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads"
    ) from None


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
