from __future__ import annotations

import importlib
import importlib.util
import warnings

toga_core_imports = {
    "ActivityIndicator": "toga.widgets.activityindicator",
    "App": "toga.app",
    "DocumentApp": "toga.app",
    "DocumentMainWindow": "toga.app",
    "MainWindow": "toga.app",
    "Widget": "toga.widgets.base",
    "Box": "toga.widgets.box",
    "Button": "toga.widgets.button",
    "Canvas": "toga.widgets.canvas",
    "hsl": "toga.colors",
    "hsla": "toga.colors",
    "rgb": "toga.colors",
    "rgba": "toga.colors",
    "Command": "toga.command",
    "Group": "toga.command",
    "DateInput": "toga.widgets.dateinput",
    "DatePicker": "toga.widgets.dateinput",
    "DetailedList": "toga.widgets.detailedlist",
    "ConfirmDialog": "toga.dialogs",
    "ErrorDialog": "toga.dialogs",
    "InfoDialog": "toga.dialogs",
    "OpenFileDialog": "toga.dialogs",
    "QuestionDialog": "toga.dialogs",
    "SaveFileDialog": "toga.dialogs",
    "SelectFolderDialog": "toga.dialogs",
    "StackTraceDialog": "toga.dialogs",
    "Divider": "toga.widgets.divider",
    "Document": "toga.documents",
    "Font": "toga.fonts",
    "Icon": "toga.icons",
    "Image": "toga.images",
    "ImageView": "toga.widgets.imageview",
    "Key": "toga.keys",
    "Label": "toga.widgets.label",
    "MapPin": "toga.widgets.mapview",
    "MapView": "toga.widgets.mapview",
    "MultilineTextInput": "toga.widgets.multilinetextinput",
    "NumberInput": "toga.widgets.numberinput",
    "OptionContainer": "toga.widgets.optioncontainer",
    "OptionItem": "toga.widgets.optioncontainer",
    "PasswordInput": "toga.widgets.passwordinput",
    "ProgressBar": "toga.widgets.progressbar",
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
    "LatLng": "toga.types",
    "Position": "toga.types",
    "Size": "toga.types",
    "WebView": "toga.widgets.webview",
    "Window": "toga.window",
}
__all__ = list(toga_core_imports.keys())


def __getattr__(name):
    try:
        module_name = toga_core_imports[name]
    except KeyError:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name)
        globals()[name] = value
        return value


class NotImplementedWarning(RuntimeWarning):
    # pytest.warns() requires that Warning() subclasses are constructed by passing a
    # single argument (the warning message). Use a factory method to avoid reproducing
    # the message format and the warn invocation.
    @classmethod
    def warn(self, platform: str, feature: str):
        """Raise a warning that a feature isn't implemented on a platform."""
        warnings.warn(NotImplementedWarning(f"[{platform}] Not implemented: {feature}"))


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
