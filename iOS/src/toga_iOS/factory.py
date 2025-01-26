from toga import NotImplementedWarning

from . import dialogs
from .app import App
from .colors import native_color
from .command import Command
from .fonts import Font
from .hardware.camera import Camera
from .hardware.location import Location
from .icons import Icon
from .images import Image
from .paths import Paths
from .statusicons import MenuStatusIcon, SimpleStatusIcon, StatusIconSet

# Widgets
from .widgets.activityindicator import ActivityIndicator
from .widgets.box import Box
from .widgets.button import Button
from .widgets.canvas import Canvas
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

# from .widgets.splitcontainer import SplitContainer
from .widgets.switch import Switch

# from .widgets.table import Table
from .widgets.textinput import TextInput

# from .widgets.tree import Tree
from .widgets.webview import WebView
from .window import MainWindow, Window


def not_implemented(feature):
    NotImplementedWarning.warn("iOS", feature)


__all__ = [
    "not_implemented",
    "ActivityIndicator",
    "App",
    "Command",
    # Resources
    "native_color",  # colors
    "Font",
    "Icon",
    "Image",
    "Paths",
    "dialogs",
    # Hardware
    "Camera",
    "Location",
    # Status icons
    "MenuStatusIcon",
    "SimpleStatusIcon",
    "StatusIconSet",
    # Widgets
    "Box",
    "Button",
    "Canvas",
    "DetailedList",
    "Divider",
    "ImageView",
    "Label",
    "MapView",
    "MultilineTextInput",
    "NumberInput",
    "OptionContainer",
    "PasswordInput",
    "ProgressBar",
    "ScrollContainer",
    "Selection",
    "Slider",
    # 'SplitContainer',
    "Switch",
    # 'Table',
    "TextInput",
    # 'Tree',
    "WebView",
    # Windows
    "MainWindow",
    "Window",
]


def __getattr__(name):  # pragma: no cover
    raise NotImplementedError(f"Toga's iOS backend doesn't implement {name}")
