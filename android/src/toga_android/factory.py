from . import dialogs
from .app import App, MainWindow
from .command import Command
from .fonts import Font
from .hardware.camera import Camera
from .icons import Icon
from .images import Image
from .paths import Paths
from .widgets.box import Box
from .widgets.button import Button
from .widgets.canvas import Canvas
from .widgets.dateinput import DateInput
from .widgets.detailedlist import DetailedList
from .widgets.divider import Divider
from .widgets.imageview import ImageView
from .widgets.label import Label
from .widgets.multilinetextinput import MultilineTextInput
from .widgets.numberinput import NumberInput
from .widgets.optioncontainer import OptionContainer
from .widgets.passwordinput import PasswordInput
from .widgets.progressbar import ProgressBar
from .widgets.scrollcontainer import ScrollContainer
from .widgets.selection import Selection
from .widgets.slider import Slider
from .widgets.switch import Switch
from .widgets.table import Table
from .widgets.textinput import TextInput
from .widgets.timeinput import TimeInput
from .widgets.webview import WebView
from .window import Window


def not_implemented(feature):
    print(f"[Android] Not implemented: {feature}")  # pragma: nocover


__all__ = [
    "App",
    "Command",
    "MainWindow",
    "not_implemented",
    # Resources
    "dialogs",
    "Font",
    "Icon",
    "Image",
    "Paths",
    # Hardware
    "Camera",
    # Widgets
    # ActivityIndicator
    "Box",
    "Button",
    "Canvas",
    "DateInput",
    "DetailedList",
    "Divider",
    "ImageView",
    "Label",
    "MultilineTextInput",
    "NumberInput",
    "OptionContainer",
    "PasswordInput",
    "ProgressBar",
    "ScrollContainer",
    # "SplitContainer",
    "Selection",
    "Slider",
    "Switch",
    "Table",
    "TextInput",
    "TimeInput",
    # "Tree",
    "WebView",
    "Window",
]


def __getattr__(name):  # pragma: no cover
    raise NotImplementedError(f"Toga's Android backend doesn't implement {name}")
