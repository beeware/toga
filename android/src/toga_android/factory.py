from . import dialogs
from .app import App, MainWindow
from .command import Command
from .fonts import Font
from .icons import Icon
from .images import Image
from .paths import Paths
from .widgets.box import Box
from .widgets.button import Button
from .widgets.canvas import Canvas
from .widgets.dateinput import DateInput
from .widgets.detailedlist import DetailedList
from .widgets.imageview import ImageView
from .widgets.label import Label
from .widgets.multilinetextinput import MultilineTextInput
from .widgets.numberinput import NumberInput
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
    "Box",
    "Button",
    "Canvas",
    "Command",
    "DateInput",
    "Font",
    "Icon",
    "Image",
    "ImageView",
    "Label",
    "MainWindow",
    "MultilineTextInput",
    "NumberInput",
    "PasswordInput",
    "ProgressBar",
    "Selection",
    "Slider",
    "ScrollContainer",
    "Switch",
    "Table",
    "TextInput",
    "TimeInput",
    "WebView",
    "Window",
    "DetailedList",
    "not_implemented",
    "Paths",
    "dialogs",
]


def __getattr__(name):  # pragma: no cover
    raise NotImplementedError(f"Toga's Android backend doesn't implement {name}")
