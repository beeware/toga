# Enable the standard library compatibility shims before doing anything else.
#
# __future__ imports must be at the very top of the file, and MicroPython doesn't
# currently include a __future__ module, so this file can't contain any __future__
# imports. Other modules imported after `compat` can use __future__ as normal.
import sys

if sys.implementation.name != "cpython":  # pragma: no cover
    from . import compat  # noqa: F401

import warnings
from importlib import import_module

from travertino import _package_version

toga_core_imports = {
    # toga.app imports
    "App": "toga.app",
    "DocumentApp": "toga.app",
    # toga.colors imports
    "hsl": "toga.colors",
    "hsla": "toga.colors",
    "rgb": "toga.colors",
    "rgba": "toga.colors",
    # toga.command imports
    "Command": "toga.command",
    "Group": "toga.command",
    # toga.dialogs imports
    "ConfirmDialog": "toga.dialogs",
    "ErrorDialog": "toga.dialogs",
    "InfoDialog": "toga.dialogs",
    "OpenFileDialog": "toga.dialogs",
    "QuestionDialog": "toga.dialogs",
    "SaveFileDialog": "toga.dialogs",
    "SelectFolderDialog": "toga.dialogs",
    "StackTraceDialog": "toga.dialogs",
    # toga.documents imports
    "Document": "toga.documents",
    "DocumentWindow": "toga.documents",
    # toga.fonts imports
    "Font": "toga.fonts",
    # toga.icons imports
    "Icon": "toga.icons",
    # toga.images imports
    "Image": "toga.images",
    # toga.keys imports
    "Key": "toga.keys",
    # toga.statusicons imports
    "MenuStatusIcon": "toga.statusicons",
    "SimpleStatusIcon": "toga.statusicons",
    # toga.types imports
    "LatLng": "toga.types",
    "Position": "toga.types",
    "Size": "toga.types",
    # toga.widgets imports
    "ActivityIndicator": "toga.widgets.activityindicator",
    "Widget": "toga.widgets.base",
    "Box": "toga.widgets.box",
    "Button": "toga.widgets.button",
    "Canvas": "toga.widgets.canvas",
    "Column": "toga.widgets.box",
    "DateInput": "toga.widgets.dateinput",
    "DatePicker": "toga.widgets.dateinput",
    "DetailedList": "toga.widgets.detailedlist",
    "Divider": "toga.widgets.divider",
    "ImageView": "toga.widgets.imageview",
    "Label": "toga.widgets.label",
    "MapPin": "toga.widgets.mapview",
    "MapView": "toga.widgets.mapview",
    "MultilineTextInput": "toga.widgets.multilinetextinput",
    "NumberInput": "toga.widgets.numberinput",
    "OptionContainer": "toga.widgets.optioncontainer",
    "OptionItem": "toga.widgets.optioncontainer",
    "PasswordInput": "toga.widgets.passwordinput",
    "ProgressBar": "toga.widgets.progressbar",
    "Row": "toga.widgets.box",
    "ScrollContainer": "toga.widgets.scrollcontainer",
    "Selection": "toga.widgets.selection",
    "Slider": "toga.widgets.slider",
    "SplitContainer": "toga.widgets.splitcontainer",
    "Switch": "toga.widgets.switch",
    "Table": "toga.widgets.table",
    "TextInput": "toga.widgets.textinput",
    "TimeInput": "toga.widgets.timeinput",
    "TimePicker": "toga.widgets.timeinput",
    "Tree": "toga.widgets.tree",
    "WebView": "toga.widgets.webview",
    # toga.window imports
    "DocumentMainWindow": "toga.window",
    "MainWindow": "toga.window",
    "Window": "toga.window",
}
__all__ = list(toga_core_imports.keys())


def __getattr__(name):
    if module_name := toga_core_imports.get(name):
        module = import_module(module_name)
        value = getattr(module, name)
    else:
        # MicroPython apparently doesn't attempt a submodule import when __getattr__
        # raises AttributeError, so we need to do it manually.
        try:
            value = import_module(f"{__name__}.{name}")
        except ImportError:
            raise AttributeError(
                f"module '{__name__}' has no attribute '{name}'"
            ) from None

    globals()[name] = value
    return value


class NotImplementedWarning(RuntimeWarning):
    # pytest.warns() requires that Warning() subclasses are constructed by passing a
    # single argument (the warning message). Use a factory method to avoid reproducing
    # the message format and the warn invocation.
    @classmethod
    def warn(cls, platform: str, feature: str) -> None:
        """Raise a warning that a feature isn't implemented on a platform."""
        warnings.warn(NotImplementedWarning(f"[{platform}] Not implemented: {feature}"))


__version__ = _package_version(__file__, __name__)
