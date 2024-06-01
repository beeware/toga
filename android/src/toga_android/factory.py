import importlib

from toga import NotImplementedWarning

toga_android_factory_imports = {
    "App": "toga_android.app",
    "MainWindow": "toga_android.app",
    "Command": "toga_android.command",
    "Camera": "toga_android.hardware.camera",
    "Font": "toga_android.fonts",
    "Icon": "toga_android.icons",
    "Image": "toga_android.images",
    "Paths": "toga_android.paths",
    "Box": "toga_android.widgets.box",
    "Button": "toga_android.widgets.button",
    "Canvas": "toga_android.widgets.canvas",
    "DateInput": "toga_android.widgets.dateinput",
    "DetailedList": "toga_android.widgets.detailedlist",
    "Divider": "toga_android.widgets.divider",
    "dialogs": "toga_android",
    "ImageView": "toga_android.widgets.imageview",
    "Label": "toga_android.widgets.label",
    "Location": "toga_android.hardware.location",
    "MapView": "toga_android.widgets.mapview",
    "MultilineTextInput": "toga_android.widgets.multilinetextinput",
    "NumberInput": "toga_android.widgets.numberinput",
    "OptionContainer": "toga_android.widgets.optioncontainer",
    "PasswordInput": "toga_android.widgets.passwordinput",
    "ProgressBar": "toga_android.widgets.progressbar",
    "ScrollContainer": "toga_android.widgets.scrollcontainer",
    "Selection": "toga_android.widgets.selection",
    "Slider": "toga_android.widgets.slider",
    "Switch": "toga_android.widgets.switch",
    "Table": "toga_android.widgets.table",
    "TextInput": "toga_android.widgets.textinput",
    "TimeInput": "toga_android.widgets.timeinput",
    "WebView": "toga_android.widgets.webview",
    "Window": "toga_android.window",
}
__all__ = list(toga_android_factory_imports.keys()) + ["not_implemented"]


def __getattr__(name):
    try:
        module_name = toga_android_factory_imports[name]

        has_dot = module_name.find(".") != -1
        if not has_dot:
            module_name = f"toga_android.{name}"
    except KeyError:
        raise NotImplementedError(
            f"Toga's Android backend doesn't implement '{name}'"
        ) from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name) if has_dot else module
        globals()[name] = value
        return value


def not_implemented(feature):
    NotImplementedWarning.warn("Android", feature)
