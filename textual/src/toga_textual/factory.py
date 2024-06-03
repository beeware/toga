import importlib

from toga import NotImplementedWarning

toga_textual_factory_imports = {
    "App": "toga_textual.app",
    "DocumentApp": "toga_textual.app",
    "MainWindow": "toga_textual.app",
    "dialogs": "toga_textual",
    # "Command": "toga_textual.command",
    # "Document": "toga_textual.documents",
    # "Font": "toga_textual.fonts",
    "Icon": "toga_textual.icons",
    # "Image": "toga_textual.images",
    "Paths": "toga_textual.paths",
    # "ActivityIndicator": "toga_textual.widgets.activityindicator",
    # "widget": "toga_textual.widgets.base",
    "Box": "toga_textual.widgets.box",
    "Button": "toga_textual.widgets.button",
    # "Canvas": "toga_textual.widgets.canvas",
    # "DateInput": "toga_textual.widgets.dateinput",
    # "DetailedList": "toga_textual.widgets.detailedlist",
    # "Divider": "toga_textual.widgets.divider",
    # "ImageView": "toga_textual.widgets.imageview",
    "Label": "toga_textual.widgets.label",
    # "MultilineTextInput": "toga_textual.widgets.multilinetextinput",
    # "NumberInput": "toga_textual.widgets.numberinput",
    # "OptionContainer": "toga_textual.widgets.optioncontainer",
    # "PasswordInput": "toga_textual.widgets.passwordinput",
    # "ProgressBar": "toga_textual.widgets.progressbar",
    # "ScrollContainer": "toga_textual.widgets.scrollcontainer",
    # "Selection": "toga_textual.widgets.selection",
    # "Slider": "toga_textual.widgets.slider",
    # "SplitContainer": "toga_textual.widgets.splitcontainer",
    # "Switch": "toga_textual.widgets.switch",
    # "Table": "toga_textual.widgets.table",
    "TextInput": "toga_textual.widgets.textinput",
    # "TimeInput": "toga_textual.widgets.timeinput",
    # "Tree": "toga_textual.widgets.tree",
    # "WebView": "toga_textual.widgets.webview",
    "Window": "toga_textual.window",
}


__all__ = list(toga_textual_factory_imports.keys()) + ["not_implemented"]


def __getattr__(name):
    try:
        module_name = toga_textual_factory_imports[name]

        has_dot = module_name.find(".") != -1
        if not has_dot:
            module_name = f"toga_textual.{name}"
    except KeyError:
        raise NotImplementedError(
            f"Toga's Textual backend doesn't implement '{name}'"
        ) from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name) if has_dot else module
        globals()[name] = value
        return value


def not_implemented(feature):
    NotImplementedWarning.warn("Textual", feature)  # pragma: nocover
