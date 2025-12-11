from toga import NotImplementedWarning

try:
    from . import dialogs
    from .app import App
    from .command import Command
    from .container import Container
    from .fonts import Font
    from .icons import Icon
    from .images import Image
    from .libs import get_testing
    from .paths import Paths
    from .statusicons import MenuStatusIcon, SimpleStatusIcon, StatusIconSet
    from .widgets.activityindicator import ActivityIndicator
    from .widgets.box import Box
    from .widgets.button import Button
    from .widgets.imageview import ImageView
    from .widgets.label import Label
    from .widgets.passwordinput import PasswordInput
    from .widgets.progressbar import ProgressBar
    from .widgets.switch import Switch
    from .widgets.textinput import TextInput
    from .window import MainWindow, Window
except ModuleNotFoundError as exc:  # pragma: no cover
    if exc.name == "PySide6":
        raise ImportError(
            "Cannot import PySide6.  Did you install toga-qt with the extra[pyside6]?"
        ) from exc
    else:
        raise

__all__ = [
    "not_implemented",
    "ActivityIndicator",
    "App",
    "Paths",
    "Icon",
    "Image",
    "MenuStatusIcon",
    "SimpleStatusIcon",
    "StatusIconSet",
    "Window",
    "MainWindow",
    "Command",
    "Button",
    "Font",
    "Container",
    "Box",
    "Label",
    "PasswordInput",
    "ProgressBar",
    "Switch",
    "TextInput",
    "ImageView",
    "dialogs",
]


def not_implemented(feature):
    NotImplementedWarning.warn("Qt", feature)


def __getattr__(name):
    if get_testing():
        import pytest

        pytest.skip("Widget not implemented on qt", allow_module_level=True)
    raise NotImplementedError(f"Toga's Qt backend doesn't implement {name}")
