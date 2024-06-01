import importlib

from toga import NotImplementedWarning

toga_gtk_factory_imports = {
    "App": "toga_gtk.app",
    "DocumentApp": "toga_gtk.app",
    "DocumentMainWindow": "toga_gtk.app",
    "Command": "toga_gtk.command",
    "Document": "toga_gtk.documents",
    "dialogs": "toga_gtk",
    "Font": "toga_gtk.fonts",
    "Camera": "toga_gtk.hardware.camera",
    "Location": "toga_gtk.hardware.location",
    "Icon": "toga_gtk.icons",
    "Image": "toga_gtk.images",
    "Paths": "toga_gtk.paths",
    "ActivityIndicator": "toga_gtk.widgets.activityindicator",
    "Box": "toga_gtk.widgets.box",
    "Button": "toga_gtk.widgets.button",
    "Canvas": "toga_gtk.widgets.canvas",
    "DetailedList": "toga_gtk.widgets.detailedlist",
    "Divider": "toga_gtk.widgets.divider",
    "ImageView": "toga_gtk.widgets.imageview",
    "Label": "toga_gtk.widgets.label",
    "MapView": "toga_gtk.widgets.mapview",
    "MainWindow": "toga_gtk.app",
    "MultilineTextInput": "toga_gtk.widgets.multilinetextinput",
    "NumberInput": "toga_gtk.widgets.numberinput",
    "OptionContainer": "toga_gtk.widgets.optioncontainer",
    "PasswordInput": "toga_gtk.widgets.passwordinput",
    "ProgressBar": "toga_gtk.widgets.progressbar",
    "ScrollContainer": "toga_gtk.widgets.scrollcontainer",
    "Selection": "toga_gtk.widgets.selection",
    "Slider": "toga_gtk.widgets.slider",
    "SplitContainer": "toga_gtk.widgets.splitcontainer",
    "Switch": "toga_gtk.widgets.switch",
    "Table": "toga_gtk.widgets.table",
    "TextInput": "toga_gtk.widgets.textinput",
    "Tree": "toga_gtk.widgets.tree",
    "WebView": "toga_gtk.widgets.webview",
    "Window": "toga_gtk.window",
}

__all__ = list(toga_gtk_factory_imports.keys()) + ["not_implemented"]


def __getattr__(name):
    try:
        module_name = toga_gtk_factory_imports[name]

        has_dot = module_name.find(".") != -1
        if not has_dot:
            module_name = f"toga_gtk.{name}"
    except KeyError:
        raise NotImplementedError(
            f"Toga's GTK backend doesn't implement '{name}'"
        ) from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name) if has_dot else module
        globals()[name] = value
        return value


def not_implemented(feature):
    NotImplementedWarning.warn("GTK", feature)
