from PySide6.QtGui import QGuiApplication

from .utils import create_qapplication

# Without a QApplication instance, determining the platform
# name does not work correctly.
create_qapplication()


# Must be defined as a function, else the expression
# gets evaluated too early and returns xcb on Wayland.
IS_WAYLAND = QGuiApplication.platformName() == "wayland"
print(IS_WAYLAND)
