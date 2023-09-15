import clr

import toga

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

__version__ = toga._package_version(__file__, __name__)
