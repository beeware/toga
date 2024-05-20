import importlib

from toga import NotImplementedWarning

toga_factory_imports = {
    "Window": "toga.window",
    "WebView": "toga.widgets.webview",
    "Tree": "toga.widgets.tree",
    "TextInput": "toga.widgets.textinput",
    "Table": "toga.widgets.table",
    "Switch": "toga.widgets.switch",
    "SplitContainer": "toga.widgets.splitcontainer",
    "Slider": "toga.widgets.slider",
    "Selection": "toga.widgets.selection",
    "ScrollContainer": "toga.widgets.scrollcontainer",
    "ProgressBar": "toga.widgets.progressbar",
    "PasswordInput": "toga.widgets.passwordinput",
    "OptionContainer": "toga.widgets.optioncontainer",
    "NumberInput": "toga.widgets.numberinput",
    "MultilineTextInput": "toga.widgets.multilinetextinput",
    "MapView": "toga.widgets.mapview",
    "Label": "toga.widgets.label",
    "ImageView": "toga.widgets.imageview",
    "Divider": "toga.widgets.divider",
    "DetailedList": "toga.widgets.detailedlist",
    "Canvas": "toga.widgets.canvas",
    "Button": "toga.widgets.button",
    "Box": "toga.widgets.box",
    "ActivityIndicator": "toga.widgets.activityindicator",
    "Path": "toga.paths",
    "Image": "toga.images",
    "Icon": "toga.icons",
    "Location": "toga.hardware.location",
    "Camera": "toga.hardware.camera",
    "Font": "toga.fonts",
    "Document": "toga.documents",
    "Command": "toga.command",
    "dialogs": "toga_cocoa",
    "App": "toga.app",
    "DocumentApp": "toga.app",
    "DocumentMainWindow": "toga.app",
}


def __getattr__(name):
    if name in toga_factory_imports:
        module = importlib.import_module(f"{toga_factory_imports[name]}")
        globals()[name] = getattr(module, name)
        return getattr(module, name)
    else:
        raise NotImplementedError(f"Toga's Cocoa backend doesn't implement {name}")


def not_implemented(feature):
    NotImplementedWarning.warn("Cocoa", feature)
