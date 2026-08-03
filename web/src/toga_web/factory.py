import warnings

from toga import NotImplementedWarning

from . import dialogs
from .app import App
from .command import Command
from .fonts import Font
from .icons import Icon

# from .images import Image
from .paths import Paths
from .statusicons import MenuStatusIcon, SimpleStatusIcon, StatusIconSet
from .widgets.activityindicator import ActivityIndicator
from .widgets.box import Box
from .widgets.button import Button
from .widgets.dateinput import DateInput
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
from .widgets.scrollcontainer import ScrollContainer
from .widgets.selection import Selection
from .widgets.slider import Slider

# from .widgets.splitcontainer import SplitContainer
from .widgets.switch import Switch

# from .widgets.table import Table
from .widgets.textinput import TextInput
from .widgets.timeinput import TimeInput

# from .widgets.tree import Tree
# from .widgets.webview import WebView
from .window import MainWindow, Window

warnings.warn(
    "Factory modules are deprecated. Use 'toga.platform.get_factory' instead.",
    DeprecationWarning,
    stacklevel=1,
)


def not_implemented(feature):  # pragma: no cover
    NotImplementedWarning.warn("Web", feature)  # pragma: nocover


__all__ = [
    "ActivityIndicator",
    "App",
    # # Widgets
    "Box",
    "Button",
    "Command",
    "DateInput",
    # 'Canvas',
    "Divider",
    # Resources
    "Font",
    "Icon",
    # 'DetailedList',
    # 'ImageView',
    "Label",
    # 'Tree',
    # 'WebView',
    # Windows
    "MainWindow",
    # Status Icons
    "MenuStatusIcon",
    # 'MultilineTextInput',
    # 'NumberInput',
    # 'OptionContainer',
    "PasswordInput",
    # 'Image',
    "Paths",
    "ProgressBar",
    "ScrollContainer",
    "Selection",
    "SimpleStatusIcon",
    "Slider",
    "StatusIconSet",
    # 'SplitContainer',
    "Switch",
    # 'Table',
    "TextInput",
    "TimeInput",
    "Window",
    "dialogs",
    "not_implemented",
]


def __getattr__(name):
    raise NotImplementedError(f"Toga's Web backend doesn't implement {name}")
