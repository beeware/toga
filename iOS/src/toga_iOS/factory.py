import importlib

from toga import NotImplementedWarning

toga_ios_factory_imports = {
    "App": "toga_iOS.app",
    "MainWindow": "toga_iOS.app",
    "Command": "toga_iOS.command",
    "Camera": "toga_iOS.hardware.camera",
    "native_color": "toga_iOS.colors",
    "Font": "toga_iOS.fonts",
    "Icon": "toga_iOS.icons",
    "Image": "toga_iOS.images",
    "Paths": "toga_iOS.paths",
    "dialogs": "toga_iOS",
    "Box": "toga_iOS.widgets.box",
    "Button": "toga_iOS.widgets.button",
    "Canvas": "toga_iOS.widgets.canvas",
    "DetailedList": "toga_iOS.widgets.detailedlist",
    "ImageView": "toga_iOS.widgets.imageview",
    "Label": "toga_iOS.widgets.label",
    "Location": "toga_iOS.hardware.location",
    "MapView": "toga_iOS.widgets.mapview",
    "MultilineTextInput": "toga_iOS.widgets.multilinetextinput",
    "NumberInput": "toga_iOS.widgets.numberinput",
    "OptionContainer": "toga_iOS.widgets.optioncontainer",
    "PasswordInput": "toga_iOS.widgets.passwordinput",
    "ProgressBar": "toga_iOS.widgets.progressbar",
    "ScrollContainer": "toga_iOS.widgets.scrollcontainer",
    "Selection": "toga_iOS.widgets.selection",
    "Slider": "toga_iOS.widgets.slider",
    "Switch": "toga_iOS.widgets.switch",
    "TextInput": "toga_iOS.widgets.textinput",
    "WebView": "toga_iOS.widgets.webview",
    "Window": "toga_iOS.window",
}


__all__ = list(toga_ios_factory_imports.keys()) + ["not_implemented"]


def __getattr__(name):
    try:
        module_name = toga_ios_factory_imports[name]

        has_dot = module_name.find(".") != -1
        if not has_dot:
            module_name = f"toga_iOS.{name}"
    except KeyError:
        raise NotImplementedError(
            f"Toga's iOS backend doesn't implement '{name}'"
        ) from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name) if has_dot else module
        globals()[name] = value
        return value


def not_implemented(feature):
    NotImplementedWarning.warn("iOS", feature)
