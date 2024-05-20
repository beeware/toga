from __future__ import annotations

import warnings
import importlib
import importlib.util
from types import ModuleType

to_import = {
    "toga.app": ["App", "DocumentApp", "DocumentMainWindow", "MainWindow"],
    "toga.colors": ["hsl", "hsla", "rgb", "rgba"],
    "toga.command": ["Command", "Group"],
    "toga.commands": ["Command", "Group"],
    "toga.documents": ["Document"],
    "toga.fonts": ["Font"],
    "toga.icons": ["Icon"],
    "toga.images": ["Image"],
    "toga.keys": ["Key"],
    "toga.types": ["LatLng"],
    "toga.widgets.activityindicator": ["ActivityIndicator"],
    "toga.widgets.base": ["Widget"],
    "toga.widgets.box": ["Box"],
    "toga.widgets.button": ["Button"],
    "toga.widgets.canvas": ["Canvas"],
    "toga.widgets.dateinput": ["DateInput", "DatePicker"],
    "toga.widgets.detailedlist": ["DetailedList"],
    "toga.widgets.divider": ["Divider"],
    "toga.widgets.imageview": ["ImageView"],
    "toga.widgets.label": ["Label"],
    "toga.widgets.mapview": ["MapPin", "MapView"],
    "toga.widgets.multilinetextinput": ["MultilineTextInput"],
    "toga.widgets.numberinput": ["NumberInput"],
    "toga.widgets.optioncontainer": ["OptionContainer", "OptionItem"],
    "toga.widgets.passwordinput": ["PasswordInput"],
    "toga.widgets.progressbar": ["ProgressBar"],
    "toga.widgets.scrollcontainer": ["ScrollContainer"],
    "toga.widgets.selection": ["Selection"],
    "toga.widgets.slider": ["Slider"],
    "toga.widgets.splitcontainer": ["SplitContainer"],
    "toga.widgets.switch": ["Switch"],
    "toga.widgets.table": ["Table"],
    "toga.widgets.textinput": ["TextInput"],
    "toga.widgets.timeinput": ["TimeInput", "TimePicker"],
    "toga.widgets.tree": ["Tree"],
    "toga.widgets.webview": ["WebView"],
    "toga.window": ["Window"],
}


def __getattr__(name):

    for module, names in to_import.items():
        if name in names:
            module = importlib.import_module(module)
            globals()[name] = getattr(module, name)
            return getattr(module, name)


class NotImplementedWarning(RuntimeWarning):
    # pytest.warns() requires that Warning() subclasses are constructed by passing a
    # single argument (the warning message). Use a factory method to avoid reproducing
    # the message format and the warn invocation.
    @classmethod
    def warn(self, platform, feature):
        """Raise a warning that a feature isn't implemented on a platform."""
        warnings.warn(NotImplementedWarning(f"[{platform}] Not implemented: {feature}"))


__all__ = [
    "NotImplementedWarning",
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
    "rgba",
    "Font",
    "Icon",
    "Image",
    # Types
    "LatLng",
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
