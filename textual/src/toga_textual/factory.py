import warnings

from toga import NotImplementedWarning

from . import dialogs
from .app import App
from .command import Command
from .fonts import Font
from .icons import Icon

# from .images import Image
from .statusicons import MenuStatusIcon, SimpleStatusIcon, StatusIconSet

# from .widgets.activityindicator import ActivityIndicator
# from .widgets.base import Widget
from .widgets.box import Box
from .widgets.button import Button

# from .widgets.canvas import Canvas
# from .widgets.dateinput import DateInput
# from .widgets.detailedlist import DetailedList
# from .widgets.divider import Divider
# from .widgets.imageview import ImageView
from .widgets.label import Label

# from .widgets.multilinetextinput import MultilineTextInput
# from .widgets.numberinput import NumberInput
# from .widgets.optioncontainer import OptionContainer
# from .widgets.passwordinput import PasswordInput
# from .widgets.progressbar import ProgressBar
# from .widgets.scrollcontainer import ScrollContainer
# from .widgets.selection import Selection
# from .widgets.slider import Slider
# from .widgets.splitcontainer import SplitContainer
# from .widgets.switch import Switch
# from .widgets.table import Table
from .widgets.textinput import TextInput

# from .widgets.timeinput import TimeInput
# from .widgets.tree import Tree
# from .widgets.webview import WebView
from .window import MainWindow, Window

warnings.warn(
    "Factory modules are deprecated. Use 'toga.platform.get_factory' instead.",
    DeprecationWarning,
    stacklevel=1,
)


def not_implemented(feature):  # pragma: no cover
    NotImplementedWarning.warn("Textual", feature)  # pragma: nocover


__all__ = [
    # "ActivityIndicator",
    "App",
    "Box",
    "Button",
    # "Canvas",
    "Command",
    # "DateInput",
    # "DetailedList",
    # "Divider",
    "Font",
    "Icon",
    # "Image",
    # "ImageView",
    "Label",
    "MainWindow",
    "MenuStatusIcon",
    # "MultilineTextInput",
    # "NumberInput",
    # "OptionContainer",
    # "PasswordInput",
    # "ProgressBar",
    # "ScrollContainer",
    # "Selection",
    "SimpleStatusIcon",
    # "Slider",
    # "SplitContainer",
    "StatusIconSet",
    # "Switch",
    # "Table",
    "TextInput",
    # "TimeInput",
    # "Tree",
    # "WebView",
    "Window",
    "dialogs",
    "not_implemented",
]


def __getattr__(name):
    raise NotImplementedError(f"Toga's Textual backend doesn't implement {name}")
