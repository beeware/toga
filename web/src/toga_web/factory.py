from toga import NotImplementedWarning

from . import dialogs
from .app import App
from .command import Command

# from .fonts import Font
from .icons import Icon

# from .images import Image
from .paths import Paths
from .statusicons import MenuStatusIcon, SimpleStatusIcon, StatusIconSet
from .widgets.activityindicator import ActivityIndicator
from .widgets.box import Box
from .widgets.button import Button
from .widgets.divider import Divider

# from .widgets.canvas import Canvas
# from .widgets.detailedlist import DetailedList
# from .widgets.imageview import ImageView
from .widgets.label import Label

# from .widgets.multilinetextinput import MultilineTextInput
# from .widgets.numberinput import NumberInput
# from .widgets.optioncontainer import OptionContainer
from .widgets.passwordinput import PasswordInput
from .widgets.progressbar import ProgressBar

# from .widgets.scrollcontainer import ScrollContainer
# from .widgets.selection import Selection
# from .widgets.slider import Slider
# from .widgets.splitcontainer import SplitContainer
from .widgets.switch import Switch

# from .widgets.table import Table
from .widgets.textinput import TextInput

# from .widgets.tree import Tree
# from .widgets.webview import WebView
from .window import MainWindow, Window


def not_implemented(feature):
    NotImplementedWarning.warn("Web", feature)  # pragma: nocover


__all__ = [
    "not_implemented",
    "App",
    "Command",
    # Resources
    # 'Font',
    "Icon",
    # 'Image',
    "Paths",
    "dialogs",
    # Status Icons
    "MenuStatusIcon",
    "SimpleStatusIcon",
    "StatusIconSet",
    # # Widgets
    "Box",
    "Button",
    # 'Canvas',
    "Divider",
    # 'DetailedList',
    # 'ImageView',
    "Label",
    # 'MultilineTextInput',
    # 'NumberInput',
    # 'OptionContainer',
    "PasswordInput",
    "ProgressBar",
    "ActivityIndicator",
    # 'ScrollContainer',
    # 'Selection',
    # 'Slider',
    # 'SplitContainer',
    "Switch",
    # 'Table',
    "TextInput",
    # 'Tree',
    # 'WebView',
    # Windows
    "MainWindow",
    "Window",
]


def __getattr__(name):  # pragma: no cover
    raise NotImplementedError(f"Toga's Web backend doesn't implement {name}")
