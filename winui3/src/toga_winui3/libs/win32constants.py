# Win32 constants

# Integral Type Constants
# https://learn.microsoft.com/cpp/c-runtime-library/data-type-constants
SHRT_MAX = 32767

# NotifyIcon Flags
NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002

# NotifyIcon Messages
NIM_ADD = 0x00000000
NIM_MODIFY = 0x00000001
NIM_DELETE = 0x00000002
NIM_SETVERSION = 0x00000004

# NotifyIcon Notifications
NIN_SELECT = 0x00000400

# NotifyIcon Versions
NOTIFYICON_VERSION_4 = 4

# Set Window Position
SWP_NOACTIVATE = 0x0010
SWP_NOOWNERZORDER = 0x0200
SWP_NOZORDER = 0x0004
SWP_DPI = SWP_NOACTIVATE | SWP_NOOWNERZORDER | SWP_NOZORDER
