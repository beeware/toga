from toga import NotImplementedWarning
import importlib

toga_factory_imports = {
    "toga.app": ["App", "DocumentApp", "MainWindow"],
    "toga_cocoa": ["dialogs"],
    "toga.command": ["Command"],
    "toga.documents": ["Document"],
    "toga.fonts": ["Font"],
    "toga.hardware.camera": ["Camera"],
    "toga.hardware.location": ["Location"],
    "toga.icons": ["Icon"],
    "toga.images": ["Image"],
    "toga.paths": ["Paths"],
    "toga.widgets.activityindicator": ["ActivityIndicator"],
    "toga.widgets.box": ["Box"],
    "toga.widgets.button": ["Button"],
    "toga.widgets.canvas": ["Canvas"],
    "toga.widgets.detailedlist": ["DetailedList"],
    "toga.widgets.divider": ["Divider"],
    "toga.widgets.imageview": ["ImageView"],
    "toga.widgets.label": ["Label"],
    "toga.widgets.mapview": ["MapView"],
    "toga.widgets.multilinetextinput": ["MultilineTextInput"],
    "toga.widgets.numberinput": ["NumberInput"],
    "toga.widgets.optioncontainer": ["OptionContainer"],
    "toga.widgets.passwordinput": ["PasswordInput"],
    "toga.widgets.progressbar": ["ProgressBar"],
    "toga.widgets.scrollcontainer": ["ScrollContainer"],
    "toga.widgets.selection": ["Selection"],
    "toga.widgets.slider": ["Slider"],
    "toga.widgets.splitcontainer": ["SplitContainer"],
    "toga.widgets.switch": ["Switch"],
    "toga.widgets.table": ["Table"],
    "toga.widgets.textinput": ["TextInput"],
    "toga.widgets.tree": ["Tree"],
    "toga.widgets.webview": ["WebView"],
    "toga.window": ["Window"],
}


def __getattr__(name):

    for module, names in toga_factory_imports.items():
        if name in names:
            module = importlib.import_module(module)
            globals()[name] = getattr(module, name)
            return getattr(module, name)
    else:
        raise NotImplementedError(f"Toga's Cocoa backend doesn't implement {name}")


def not_implemented(feature):
    NotImplementedWarning.warn("Cocoa", feature)


__all__ = [
    "not_implemented",
    "App",
    "DocumentApp",
    "MainWindow",
    "Command",
    "Document",
    # Resources
    "Font",
    "Icon",
    "Image",
    "Paths",
    "dialogs",
    # Hardware
    "Camera",
    "Location",
    # Widgets
    "ActivityIndicator",
    "Box",
    "Button",
    "Canvas",
    "DetailedList",
    "Divider",
    "ImageView",
    "Label",
    "MapView",
    "MultilineTextInput",
    "NumberInput",
    "OptionContainer",
    "PasswordInput",
    "ProgressBar",
    "ScrollContainer",
    "Selection",
    "Slider",
    "SplitContainer",
    "Switch",
    "Table",
    "TextInput",
    "Tree",
    "WebView",
    "Window",
]
