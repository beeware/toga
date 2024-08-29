from __future__ import annotations

import warnings
from pathlib import Path

from .app import App, DocumentApp
from .colors import hsl, hsla, rgb, rgba
from .command import Command, Group
from .dialogs import (
    ConfirmDialog,
    ErrorDialog,
    InfoDialog,
    OpenFileDialog,
    QuestionDialog,
    SaveFileDialog,
    SelectFolderDialog,
    StackTraceDialog,
)
from .documents import Document, DocumentWindow
from .fonts import Font
from .icons import Icon
from .images import Image
from .keys import Key
from .statusicons import MenuStatusIcon, SimpleStatusIcon
from .types import LatLng, Position, Size
from .widgets.activityindicator import ActivityIndicator
from .widgets.base import Widget
from .widgets.box import Box
from .widgets.button import Button
from .widgets.canvas import Canvas
from .widgets.dateinput import DateInput, DatePicker
from .widgets.detailedlist import DetailedList
from .widgets.divider import Divider
from .widgets.imageview import ImageView
from .widgets.label import Label
from .widgets.mapview import MapPin, MapView
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
from .window import MainWindow, Window


class NotImplementedWarning(RuntimeWarning):
    # pytest.warns() requires that Warning() subclasses are constructed by passing a
    # single argument (the warning message). Use a factory method to avoid reproducing
    # the message format and the warn invocation.
    @classmethod
    def warn(cls, platform: str, feature: str) -> None:
        """Raise a warning that a feature isn't implemented on a platform."""
        warnings.warn(NotImplementedWarning(f"[{platform}] Not implemented: {feature}"))


__all__ = [
    "NotImplementedWarning",
    # Applications
    "App",
    "DocumentApp",
    # Commands
    "Command",
    "Group",
    # Documents
    "Document",
    "DocumentWindow",
    # Dialogs
    "ConfirmDialog",
    "ErrorDialog",
    "InfoDialog",
    "OpenFileDialog",
    "QuestionDialog",
    "SaveFileDialog",
    "SelectFolderDialog",
    "StackTraceDialog",
    # Keys
    "Key",
    # Resources
    "hsl",
    "hsla",
    "rgb",
    "rgba",
    "Font",
    "Icon",
    "Image",
    # Status icons
    "MenuStatusIcon",
    "SimpleStatusIcon",
    # Types
    "LatLng",
    "Position",
    "Size",
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
    "MapPin",
    "MapView",
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
    # Windows
    "MainWindow",
    "Window",
    # Deprecated widget names
    "DatePicker",
    "TimePicker",
]


def _package_version(file: Path | str | None, name: str) -> str:
    try:
        # Read version from SCM metadata
        # This will only exist in a development environment
        from setuptools_scm import get_version

        # Excluded from coverage because a pure test environment (such as the one
        # used by tox in CI) won't have setuptools_scm
        return get_version(root="../../..", relative_to=file)  # pragma: no cover
    except (
        ModuleNotFoundError,
        LookupError,
    ):  # pragma: no-cover-if-missing-setuptools_scm
        # If setuptools_scm isn't in the environment, the call to import will fail.
        # If it *is* in the environment, but the code isn't a git checkout (e.g.,
        # it's been pip installed non-editable) the call to get_version() will fail.
        # If either of these occurs, read version from the installer metadata.
        import importlib.metadata

        # The Toga package names as defined in setup.cfg all use dashes.
        package = "toga-core" if name == "toga" else name.replace("_", "-")
        return importlib.metadata.version(package)


__version__ = _package_version(__file__, __name__)
