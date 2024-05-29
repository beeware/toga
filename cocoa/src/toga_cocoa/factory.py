import importlib

from toga import NotImplementedWarning

toga_cocoa_factory_imports = {
    "App": "toga_cocoa.app",
    "DocumentApp": "toga_cocoa.app",
    "DocumentMainWindow": "toga_cocoa.app",
    "Command": "toga_cocoa.command",
    "Document": "toga_cocoa.documents",
    "dialogs": "toga_cocoa",
    "Font": "toga_cocoa.fonts",
    "Camera": "toga_cocoa.hardware.camera",
    "Location": "toga_cocoa.hardware.location",
    "Icon": "toga_cocoa.icons",
    "Image": "toga_cocoa.images",
    "Paths": "toga_cocoa.paths",
    "ActivityIndicator": "toga_cocoa.widgets.activityindicator",
    "Box": "toga_cocoa.widgets.box",
    "Button": "toga_cocoa.widgets.button",
    "Canvas": "toga_cocoa.widgets.canvas",
    "DetailedList": "toga_cocoa.widgets.detailedlist",
    "Divider": "toga_cocoa.widgets.divider",
    "ImageView": "toga_cocoa.widgets.imageview",
    "Label": "toga_cocoa.widgets.label",
    "MapView": "toga_cocoa.widgets.mapview",
    "MultilineTextInput": "toga_cocoa.widgets.multilinetextinput",
    "NumberInput": "toga_cocoa.widgets.numberinput",
    "OptionContainer": "toga_cocoa.widgets.optioncontainer",
    "PasswordInput": "toga_cocoa.widgets.passwordinput",
    "ProgressBar": "toga_cocoa.widgets.progressbar",
    "ScrollContainer": "toga_cocoa.widgets.scrollcontainer",
    "Selection": "toga_cocoa.widgets.selection",
    "Slider": "toga_cocoa.widgets.slider",
    "SplitContainer": "toga_cocoa.widgets.splitcontainer",
    "Switch": "toga_cocoa.widgets.switch",
    "Table": "toga_cocoa.widgets.table",
    "TextInput": "toga_cocoa.widgets.textinput",
    "Tree": "toga_cocoa.widgets.tree",
    "WebView": "toga_cocoa.widgets.webview",
    "Window": "toga_cocoa.window",
}


def __getattr__(name):
    try:
        module_name = toga_cocoa_factory_imports[name]
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
