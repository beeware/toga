from ctypes import WinError, byref, c_wchar_p, get_last_error, sizeof
from pathlib import Path

from . import win32constants as wc
from .kernel32 import ActivateActCtx, CreateActCtxW, DeactivateActCtx, ReleaseActCtx
from .win32structures import ACTCTXW, ULONG_PTR


class ActivationContext:
    """A context manager to call code within the win32.manifest activation context.

    This is primarily used for Common Control version 6, and is based on the built-in
    wrapper that is used when the ISOLATION_AWARE_ENABLED macro is employed. This is
    described by Raymond Chen here:
    https://devblogs.microsoft.com/oldnewthing/20140508-00/?p=1043
    """

    def __init__(self):
        self._cookie = ULONG_PTR()
        self._manifest_path = c_wchar_p(
            str(Path(__file__).parent.parent / "resources" / "win32.manifest")
        )

        actctx = ACTCTXW()
        actctx.cbSize = sizeof(ACTCTXW)

        # It is implicit in the ACTCTXW documentation that when using a manifest only
        # lpSource and cbSize need to be set.
        actctx.lpSource = self._manifest_path

        # According to the ACTCTXW documentation, the manifest will be assumed to be
        # written in the current user's current UI language. So, specify that the
        # manifest is written in US English.
        actctx.wLangId = 1033

        # Create a handle and activation context from ../resources/win32.manifest.
        self._handle_actctx = CreateActCtxW(byref(actctx))
        if self._handle_actctx == wc.INVALID_HANDLE_VALUE:  # pragma: no cover
            # This is not expected to fail.
            raise WinError(
                descr="CreateActCtxW failed to create a handle from win32.manifest.",
                code=get_last_error(),
            )

    def __enter__(self):
        # Activate the activation context.
        return_code = ActivateActCtx(self._handle_actctx, byref(self._cookie))
        if not return_code:  # pragma: no cover
            # This is not expected to fail.
            raise WinError(descr="ActivateActCtx failed for win32.manifest.")

    def __exit__(self, exc_type, exc_value, traceback):
        # Deactivate the activation context.
        if not DeactivateActCtx(0, self._cookie):  # pragma: no cover
            # This is not expected to fail.
            raise WinError(
                descr="DeactivateActCtx failed for win32.manifest.",
                code=get_last_error(),
            )

    def __del__(self):  # pragma: no cover
        # This can't get coverage in CI because the only instance
        # is a module-level variable.
        ReleaseActCtx(self._handle_actctx)


# Create and instance of the ActivationContext context manager.
activation_context = ActivationContext()


# https://learn.microsoft.com/en-us/windows/win32/winmsg/loword
def loword(lparam: int) -> int:
    """Keeps the lower 16 bits of a value with at least 16 bits."""
    return lparam & 0b1111111111111111


# https://learn.microsoft.com/en-us/windows/win32/winmsg/hiword
def hiword(lparam: int) -> int:
    """Keeps the upper 16 bits of value with at least 32 bits."""
    return (lparam >> 16) & 0b1111111111111111


def is_submessage(message: int, submessage: int) -> bool:
    """Tests if a message is a bit-wise sub-message of a given message."""
    return (message & submessage) != 0
