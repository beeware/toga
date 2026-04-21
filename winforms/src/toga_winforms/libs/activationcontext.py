import functools
from collections.abc import Callable
from ctypes import WinDLL, WinError, byref, get_last_error, sizeof
from pathlib import Path

from . import windowconstants as wc
from .kernel32 import ActivateActCtx, CreateActCtxW, DeactivateActCtx, ReleaseActCtx
from .kernel32classes import ACTCTXW
from .win32 import ULONG_PTR


def activation_context(input_function: Callable):
    """A wrapper to call functions within the Toga activation context.

    This is primarily used for Common Control version 6, and is based on the built-in
    wrapper that is used when the ISOLATION_AWARE_ENABLED macro is employed. This is
    described by Raymond Chen here:
    https://devblogs.microsoft.com/oldnewthing/20140508-00/?p=1043
    """

    @functools.wraps(input_function)
    def call_with_activation_context(*args, **kwargs):
        manifest_path = str(
            Path(__file__).parent.parent / "resources" / "win32.manifest"
        )

        cookie = ULONG_PTR()
        actctx = ACTCTXW()
        actctx.cbSize = sizeof(ACTCTXW)

        # It is implicit in the ACTCTXW documentation that when using a manifest only
        # lpSource and cbSize need to be set.
        actctx.lpSource = manifest_path

        # According to the ACTCTXW documentation, the manifest will be assumed to be
        # written in the current user's current UI language. So, specify that the
        # manifest is written in US English.
        actctx.wLangId = 1033

        # Create a handle and activation context from ../resources/win32.manifest.
        handle_actctx = CreateActCtxW(byref(actctx))
        if handle_actctx == wc.INVALID_HANDLE_VALUE:  # pragma: no cover
            # This is not expected to fail.
            raise WinError(
                descr="CreateActCtxW failed to create a handle from win32.manifest.",
                code=get_last_error(),
            )

        # Activate the activation context.
        if not ActivateActCtx(handle_actctx, byref(cookie)):  # pragma: no cover
            # This is not expected to fail.
            raise WinError(descr="ActivateActCtx failed for win32.manifest.")

        # Call the input function.
        function_output = input_function(*args, **kwargs)

        if not DeactivateActCtx(0, cookie):  # pragma: no cover
            # This is not expected to fail.
            raise WinError(
                descr="DeactivateActCtx failed for win32.manifest.",
                code=get_last_error(),
            )

        ReleaseActCtx(handle_actctx)

        return function_output

    return call_with_activation_context


@activation_context
def WinDLL_activation_context(library: str):
    return WinDLL(library)
