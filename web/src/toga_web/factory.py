import importlib

from toga import NotImplementedWarning

toga_web_factory_imports = {
    "App": "toga_web.app",
    "MainWindow": "toga_web.app",
    "Command": "toga_web.command",
    "dialogs": "toga_web",
    # "DocumentApp": "toga_web.app",
    # "Document": "toga_web.documents",
    # "Font": "toga_web.fonts",
    "Icon": "toga_web.icons",
    "Paths": "toga_web.paths",
    # "Image": "toga_web.images",
    "ActivityIndicator": "toga_web.widgets.activityindicator",
    "Box": "toga_web.widgets.box",
    "Button": "toga_web.widgets.button",
    "Divider": "toga_web.widgets.divider",
    # "Canvas": "toga_web.widgets.canvas",
    # "DetailedList": "toga_web.widgets.detailedlist",
    # "ImageView": "toga_web.widgets.imageview",
    "Label": "toga_web.widgets.label",
    # "MultilineTextInput": "toga_web.widgets.multilinetextinput",
    # "NumberInput": "toga_web.widgets.numberinput",
    # "OptionContainer": "toga_web.widgets.optioncontainer",
    "PasswordInput": "toga_web.widgets.passwordinput",
    "ProgressBar": "toga_web.widgets.progressbar",
    # "ScrollContainer": "toga_web.widgets.scrollcontainer",
    # "Selection": "toga_web.widgets.selection",
    # "Slider": "toga_web.widgets.slider",
    # "SplitContainer": "toga_web.widgets.splitcontainer",
    "Switch": "toga_web.widgets.switch",
    # "Table": "toga_web.widgets.table",
    "TextInput": "toga_web.widgets.textinput",
    # "Tree": "toga_web.widgets.tree",
    # "WebView": "toga_web.widgets.webview",
    # "Window": "toga_web.window",
}

__all__ = list(toga_web_factory_imports.keys()) + ["not_implemented"]


def __getattr__(name):
    try:
        module_name = toga_web_factory_imports[name]

        has_dot = module_name.find(".") != -1
        if not has_dot:
            module_name = f"toga_iOS.{name}"
    except KeyError:
        raise NotImplementedError(
            f"Toga's Web backend doesn't implement '{name}'"
        ) from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name) if has_dot else module
        globals()[name] = value
        return value


def not_implemented(feature):
    NotImplementedWarning.warn("Web", feature)
