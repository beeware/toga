import importlib

from toga import NotImplementedWarning

toga_factory_imports = {
    "App": "toga.app",
    "DocumentApp": "toga.app",
    "DocumentMainWindow": "toga.app",
    "Command": "toga.command",
    "Document": "toga.documents",
    "dialogs": "toga_cocoa",
    "Font": "toga.fonts",
    "Camera": "toga.hardware.camera",
    "Location": "toga.hardware.location",
    "Icon": "toga.icons",
    "Image": "toga.images",
    "Paths": "toga.paths",
    "ActivityIndicator": "toga.widgets.activityindicator",
    "Box": "toga.widgets.box",
    "Button": "toga.widgets.button",
    "Canvas": "toga.widgets.canvas",
    "DetailedList": "toga.widgets.detailedlist",
    "Divider": "toga.widgets.divider",
    "ImageView": "toga.widgets.imageview",
    "Label": "toga.widgets.label",
    "MapView": "toga.widgets.mapview",
    "MultilineTextInput": "toga.widgets.multilinetextinput",
    "NumberInput": "toga.widgets.numberinput",
    "OptionContainer": "toga.widgets.optioncontainer",
    "PasswordInput": "toga.widgets.passwordinput",
    "ProgressBar": "toga.widgets.progressbar",
    "ScrollContainer": "toga.widgets.scrollcontainer",
    "Selection": "toga.widgets.selection",
    "Slider": "toga.widgets.slider",
    "SplitContainer": "toga.widgets.splitcontainer",
    "Switch": "toga.widgets.switch",
    "Table": "toga.widgets.table",
    "TextInput": "toga.widgets.textinput",
    "Tree": "toga.widgets.tree",
    "WebView": "toga.widgets.webview",
    "Window": "toga.window",
}


def __getattr__(name):
    try:
        module_name = toga_factory_imports[name]
    except KeyError:
        raise NotImplementedError(
            f"Toga's Cocoa backend doesn't implement '{name}'"
        ) from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name)
        globals()[name] = value
        return value


def not_implemented(feature):
    NotImplementedWarning.warn("Cocoa", feature)
