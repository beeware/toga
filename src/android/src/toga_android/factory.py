from .app import App, MainWindow
from .command import Command
from .fonts import Font
from .icons import Icon
from .images import Image
from .paths import paths
from . import dialogs

from .widgets.box import Box
from .widgets.button import Button
from .widgets.canvas import Canvas
from .widgets.datepicker import DatePicker
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
from .widgets.timepicker import TimePicker
from .widgets.webview import WebView
from .window import Window


def not_implemented(feature):
    print("[Android] Not implemented: {}".format(feature))


__all__ = [
    "App",
    "Box",
    "Button",
    "Canvas",
    "Command",
    "DatePicker",
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
    "TimePicker",
    "WebView",
    "Window",
    "DetailedList",
    "not_implemented",
    "paths",
    "dialogs",
]
