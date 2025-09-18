from PySide6.QtGui import QGuiApplication


# Must be defined as a function, else the expression
# gets evaluated too early and returns xcb on Wayland.
def get_is_wayland():
    return "wayland" == QGuiApplication.platformName()
