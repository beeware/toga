from PySide6.QtGui import QGuiApplication

from .utils import create_qapplication


def __getattr__(name):
    if name == "IS_WAYLAND":
        create_qapplication()
        return QGuiApplication.platformName() == "wayland"
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
