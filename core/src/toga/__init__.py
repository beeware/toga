from .app import App, DocumentApp, DocumentMainWindow, MainWindow

# Resources
from .colors import hsl, hsla, rgb, rgba
from .command import Command, Group
from .documents import Document
from .fonts import Font
from .icons import Icon
from .images import Image
from .keys import Key
from .widgets.activityindicator import ActivityIndicator

# Widgets
from .widgets.base import Widget
from .widgets.box import Box
from .widgets.button import Button
from .widgets.canvas import Canvas
from .widgets.dateinput import DateInput, DatePicker
from .widgets.detailedlist import DetailedList
from .widgets.divider import Divider
from .widgets.imageview import ImageView
from .widgets.label import Label
from .widgets.multilinetextinput import MultilineTextInput
from .widgets.numberinput import NumberInput
from .widgets.optioncontainer import OptionContainer, OptionItem
from .widgets.passwordinput import PasswordInput
from .widgets.progressbar import ProgressBar
from .widgets.scrollcontainer import ScrollContainer
from .widgets.selection import Selection
from .widgets.slider import Slider
from .widgets.splitcontainer import SplitContainer
from .widgets.switch import Switch
from .widgets.table import Table
from .widgets.textinput import TextInput
from .widgets.timeinput import TimeInput, TimePicker
from .widgets.tree import Tree
from .widgets.webview import WebView
from .window import Window

__all__ = [
    # Applications
    "App",
    "DocumentApp",
    "MainWindow",
    "DocumentMainWindow",
    # Commands
    "Command",
    "Group",
    # Documents
    "Document",
    # Keys
    "Key",
    # Resources
    "hsl",
    "hsla",
    "rgb",
    "rgba",  # Colors
    "Font",
    "Icon",
    "Image",
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
    "OptionItem",
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
    "Widget",
    "Window",
    # Deprecated widget names
    "DatePicker",
    "TimePicker",
]


def _package_version(file, name):
    try:
        # Read version from SCM metadata
        # This will only exist in a development environment
        from setuptools_scm import get_version

        # Excluded from coverage because a pure test environment (such as the one
        # used by tox in CI) won't have setuptools_scm
        return get_version(root="../../..", relative_to=file)  # pragma: no cover
    except (ModuleNotFoundError, LookupError):
        # If setuptools_scm isn't in the environment, the call to import will fail.
        # If it *is* in the environment, but the code isn't a git checkout (e.g.,
        # it's been pip installed non-editable) the call to get_version() will fail.
        # If either of these occurs, read version from the installer metadata.
        import importlib.metadata

        # The Toga package names as defined in setup.cfg all use dashes.
        package = "toga-core" if name == "toga" else name.replace("_", "-")
        return importlib.metadata.version(package)


__version__ = _package_version(__file__, __name__)
