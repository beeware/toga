"""
 This script builds a table to show the supported platforms for Toga
 and the components that are supported per platform.

 Requires: pytablewriter from PyPi
"""
import ast
import os

import pytablewriter

"""
A dictionary of components, index is the module name and value is the class name
"""
COMPONENT_LIST = [
    ('EXPANDING_SPACER', None),
    ('SEPARATOR', None),
    ('SPACER', None),
    ('TIBERIUS_ICON', None),
    ('Command', None),
    ('Image', None),
    ('App', 'toga.interface.app.App'),
    ('Font', 'toga.interface.font.Font'),
    ('MainWindow', 'toga.interface.app.MainWindow'),
    ('Window', 'toga.interface.window.Window'),
    ('Box', 'toga.interface.widgets.box.Box'),
    ('Button', 'toga.interface.widgets.button.Button'),
    ('Canvas', 'toga.interface.widgets.canvas.Canvas'),
    ('Icon', 'toga.interface.widgets.icon.Icon'),
    ('ImageView', 'toga.interface.widgets.imageview.ImageView'),
    ('Label', 'toga.interface.widgets.label.Label'),
    ('MultilineTextInput', 'toga.interface.widgets.multilinetextinput.MultilineTextInput'),
    ('NumberInput', 'toga.interface.widgets.numberinput.NumberInput'),
    ('OptionContainer', 'toga.interface.widgets.optioncontainer.OptionContainer'),
    ('PasswordInput', 'toga.interface.widgets.passwordinput.PasswordInput'),
    ('ProgressBar', 'toga.interface.widgets.progressbar.ProgressBar'),
    ('ScrollContainer', 'toga.interface.widgets.scrollcontainer.ScrollContainer'),
    ('Selection', 'toga.interface.widgets.selection.Selection'),
    ('SplitContainer', 'toga.interface.widgets.splitcontainer.SplitContainer'),
    ('Table', 'toga.interface.widgets.table.Table'),
    ('TextInput', 'toga.interface.widgets.textinput.TextInput'),
    ('Tree', 'toga.interface.widgets.tree.Tree'),
    ('WebView', 'toga.interface.widgets.webview.WebView')]

"""
Static list of potential platforms, index is the directory and value is the friendly name
"""
PLATFORM_LIST = {
    'android': 'Android',
    'cocoa': 'Mac OS cocoa',
    'gtk': 'GTK +',
    'django': 'Django',
    'iOS': 'Apple iOS',
    'web': 'Web',
    'win32': 'Windows'
}

_footer = """
.. |yes| replace:: ✔

"""


def get_declaration_from_source(text, name="__all__"):
    # Credit: http://stackoverflow.com/q/42195468#comment71553012_42195468
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return ast.literal_eval(node.value)
    raise NameError("name {} was not found".format(name))


_maps = dict.fromkeys(COMPONENT_LIST)

for module, label in PLATFORM_LIST.items():
    factory_path = os.path.join(
        '../src', module, 'toga_' + module, 'factory.py')
    if os.path.exists(factory_path):
        path = factory_path
    else:
        path = os.path.join('../src', module, 'toga_' + module, '__init__.py')
    with open(path, 'r') as f:
        names = get_declaration_from_source(f.read())
        for key in _maps.keys():
            name, namespace = key
            if name in names:
                if _maps[key] is None:
                    _maps[key] = list()
                _maps[key].append(module)

_platforms = list(PLATFORM_LIST.keys())

# Write the overall component compatibility list
with open('../docs/supported_platforms.rst', 'w+') as doc:
    writer = pytablewriter.RstGridTableWriter()
    writer.stream = doc
    # writer.table_name = "Supported platforms"
    writer.header_list = ["Component"] + _platforms
    writer.value_matrix = []
    for c, v in _maps.items():
        label = ':mod:`{0}`'.format(c[1]) if c[1] is not None else c[0]
        i = list([label])
        for platform in _platforms:
            if v and platform in v:
                i.append('|yes|')
            else:
                # X and O symbols have opposite meanings depending on
                # the culture so we use blank spaces for "no"
                i.append(' ')
        writer.value_matrix.append(i)

    writer.write_table()
    doc.write(_footer)

print("Done.")
