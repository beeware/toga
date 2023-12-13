from . import dialogs
from .app import App, DocumentApp, MainWindow
from .command import Command
from .documents import Document
from .fonts import Font
from .hardware.camera import Camera
from .icons import Icon
from .images import Image
from .paths import Paths
from .widgets.activityindicator import ActivityIndicator
from .widgets.base import Widget
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
from .widgets.splitcontainer import SplitContainer
from .widgets.switch import Switch
from .widgets.table import Table
from .widgets.textinput import TextInput
from .widgets.timeinput import TimeInput
from .widgets.tree import Tree
from .widgets.webview import WebView
from .window import Window


def not_implemented(feature):
    raise NotImplementedError()


__all__ = [
    "not_implemented",
    "App",
    "DocumentApp",
    "MainWindow",
    "Command",
    "Document",
    "Font",
    "Icon",
    "Image",
    "Paths",
    "dialogs",
    # Hardware
    "Camera",
    # Widgets
    "ActivityIndicator",
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
    "Selection",
    "Slider",
    "SplitContainer",
    "Switch",
    "Table",
    "TextInput",
    "TimeInput",
    "Tree",
    "WebView",
    "Window",
    # Widget is also required for testing purposes
    # Real backends shouldn't expose Widget.
    "Widget",
]


def __getattr__(name):  # pragma: no cover
    raise NotImplementedError(f"Toga's Dummy backend doesn't implement {name}")
