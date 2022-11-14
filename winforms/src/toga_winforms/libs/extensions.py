import os
import platform

import clr

#######################################################################
# WebView2
#######################################################################
WEBVIEW2_DIR = os.path.join(os.path.dirname(__file__), "WebView2")

# The architecture-specific extension dlls folder must be in the path
archpath = "x64" if platform.architecture()[0] == "64bit" else "x86"
os.environ["Path"] = os.path.join(WEBVIEW2_DIR, archpath) + ";" + os.environ["Path"]

clr.AddReference(os.path.join(WEBVIEW2_DIR, "Microsoft.Web.WebView2.Core.dll"))
clr.AddReference(os.path.join(WEBVIEW2_DIR, "Microsoft.Web.WebView2.WinForms.dll"))

from Microsoft.Web.WebView2.Core import (  # noqa: F401, E402
    WebView2RuntimeNotFoundException,
)
from Microsoft.Web.WebView2.WinForms import (  # noqa: F401, E402
    CoreWebView2CreationProperties,
    WebView2,
)
