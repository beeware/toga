from PySide6.QtGui import QGuiApplication

from .utils import create_qapplication


class LazyWaylandFlag:
    def __bool__(self):
        create_qapplication()
        return QGuiApplication.platformName() == "wayland"


IS_WAYLAND = LazyWaylandFlag()
