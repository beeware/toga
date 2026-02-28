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
    from .widgets.canvas import Canvas
    from .widgets.dateinput import DateInput
    from .widgets.detailedlist import DetailedList
    from .widgets.divider import Divider
    from .widgets.imageview import ImageView
    from .widgets.label import Label
    from .widgets.mapview import MapView
    from .widgets.multilinetextinput import MultilineTextInput
    from .widgets.numberinput import NumberInput
    from .widgets.optioncontainer import OptionContainer
    from .widgets.passwordinput import PasswordInput
    from .widgets.progressbar import ProgressBar
    from .widgets.scrollcontainer import ScrollContainer
    from .widgets.selection import Selection
    from .widgets.slider import Slider
    from .widgets.splitcontainer import SplitContainer
    from .widgets.switch import Switch
    from .widgets.table import Table
    from .widgets.textinput import TextInput
    from .widgets.timeinput import TimeInput
    from .widgets.tree import Tree
    from .widgets.webview import WebView
    from .window import MainWindow, Window
except ModuleNotFoundError as exc:  # pragma: no cover
    if exc.name == "PySide6":
        raise ImportError(
            "Cannot import PySide6.  Did you install toga-qt with the extra [pyside6]?"
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
    "Canvas",
    "DateInput",
    "DetailedList",
    "Divider",
    "Font",
    "Container",
    "Box",
    "Label",
    "MapView",
    "MultilineTextInput",
    "NumberInput",
    "OptionContainer",
    "PasswordInput",
    "ProgressBar",
    "SplitContainer",
    "Selection",
    "ScrollContainer",
    "Switch",
    "Slider",
    "Table",
    "TextInput",
    "TimeInput",
    "Tree",
    "WebView",
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
