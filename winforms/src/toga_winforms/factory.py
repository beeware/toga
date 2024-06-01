import importlib

from toga import NotImplementedWarning


def not_implemented(feature):
    NotImplementedWarning.warn("winforms", feature)


winforms_factory_imports = {
    "App": "toga_winforms.app",
    "MainWindow": "toga_winforms.app",
    "Command": "toga_winforms.command",
    "dialogs": "toga_winforms",
    "Font": "toga_winforms.fonts",
    "Icon": "toga_winforms.icons",
    "Image": "toga_winforms.images",
    "Paths": "toga_winforms.paths",
    "Box": "toga_winforms.widgets.box",
    "Button": "toga_winforms.widgets.button",
    "Canvas": "toga_winforms.widgets.canvas",
    "DetailedList": "toga_winforms.widgets.detailedlist",
    "Divider": "toga_winforms.widgets.divider",
    "DateInput": "toga_winforms.widgets.dateinput",
    "ImageView": "toga_winforms.widgets.imageview",
    "Label": "toga_winforms.widgets.label",
    "MapView": "toga_winforms.widgets.mapview",
    "MultilineTextInput": "toga_winforms.widgets.multilinetextinput",
    "NumberInput": "toga_winforms.widgets.numberinput",
    "OptionContainer": "toga_winforms.widgets.optioncontainer",
    "PasswordInput": "toga_winforms.widgets.passwordinput",
    "ProgressBar": "toga_winforms.widgets.progressbar",
    "ScrollContainer": "toga_winforms.widgets.scrollcontainer",
    "Selection": "toga_winforms.widgets.selection",
    "Slider": "toga_winforms.widgets.slider",
    "SplitContainer": "toga_winforms.widgets.splitcontainer",
    "Switch": "toga_winforms.widgets.switch",
    "Table": "toga_winforms.widgets.table",
    "TextInput": "toga_winforms.widgets.textinput",
    "TimeInput": "toga_winforms.widgets.timeinput",
    "WebView": "toga_winforms.widgets.webview",
    "Window": "toga_winforms.window",
}

__all__ = list(winforms_factory_imports.keys()) + ["not_implemented"]


def __getattr__(name):
    try:
        module_name = winforms_factory_imports[name]

        has_dot = module_name.find(".") != -1
        if not has_dot:
            module_name = f"toga_winforms.{name}"
    except KeyError:
        raise NotImplementedError(
            f"Toga's Winforms backend doesn't implement '{name}'"
        ) from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name) if has_dot else module
        globals()[name] = value
        return value
