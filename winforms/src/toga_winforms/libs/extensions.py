import os
import platform
from pathlib import Path

import clr

#######################################################################
# WebView2
#######################################################################
WEBVIEW2_DIR = Path(__file__).parent / "WebView2"

# Derive the runtime's arch from the current machine's arch
arch_path = {
    "AMD64": "win-x64",
    "x86": "win-x86",
    "ARM64": "win-arm64",
}[platform.machine()]

# This specific filesystem layout is required for Windows Store Python.
# While python.org Python will respect $PATH when searching for DLLs to load,
# the Windows Store Python does not. Therefore, this filesystem layout is what
# the WebView2 loader will search by default to find the runtime.
# ref: https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution?tabs=dotnetcsharp#files-to-ship-with-the-app  # noqa: E501
webview_runtime_dir = WEBVIEW2_DIR / f"runtimes/{arch_path}/native"
os.environ["Path"] = f"{webview_runtime_dir}{os.pathsep}{os.environ['Path']}"

clr.AddReference(str(WEBVIEW2_DIR / "Microsoft.Web.WebView2.Core.dll"))
clr.AddReference(str(WEBVIEW2_DIR / "Microsoft.Web.WebView2.WinForms.dll"))

from Microsoft.Web.WebView2.Core import (  # noqa: F401, E402
    WebView2RuntimeNotFoundException,
)
from Microsoft.Web.WebView2.WinForms import (  # noqa: F401, E402
    CoreWebView2CreationProperties,
    WebView2,
)
