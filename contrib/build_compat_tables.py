"""
 This script builds a table to show the supported platforms for Toga and the components that are supported
 
 Requires: pytablewriter from PyPi
"""
import ast
import os

import pytablewriter

"""
A dictionary of components, index is the module name and value is the class name
"""
COMPONENT_LIST =  [
    ('App', 'toga.interface.app.App'),
    ('MainWindow', 'toga.interface.app.MainWindow'),
    ('Window', 'toga.interface.window.Window'),
    ('Command', None),
    ('SEPARATOR', None),
    ('SPACER', None),
    ('EXPANDING_SPACER', None),
    ('Box', 'toga.interface.widgets.box.Box'),
    ('Button', 'toga.interface.widgets.button.Button'),
    ('Canvas', 'toga.interface.widgets.canvas.Canvas'),
    ('Icon', 'toga.interface.widgets.icon.Icon'),
    ('TIBERIUS_ICON', None),
    ('Image', None),
    ('ImageView', 'toga.interface.widgets.imageview.ImageView'),
    ('Font', 'toga.interface.font.Font'),
    ('Label', 'toga.interface.widgets.label.Label'),
    ('MultilineTextInput', 'toga.interface.widgets.multilinetextinput.MultilineTextInput'),
    ('NumberInput','toga.interface.widgets.numberinput.NumberInput'),
    ('OptionContainer','toga.interface.widgets.optioncontainer.OptionContainer'),
    ('PasswordInput','toga.interface.widgets.passwordinput.PasswordInput'),
    ('ProgressBar','toga.interface.widgets.progressbar.ProgressBar'),
    ('ScrollContainer','toga.interface.widgets.scrollcontainer.ScrollContainer'),
    ('Selection','toga.interface.widgets.selection.Selection'),
    ('SplitContainer','toga.interface.widgets.splitcontainer.SplitContainer'),
    ('Table','toga.interface.widgets.table.Table'),
    ('TextInput','toga.interface.widgets.textinput.TextInput'),
    ('Tree','toga.interface.widgets.tree.Tree'),
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
.. |yes| image:: /_static/yes.png
    :width: 32
.. |no| image:: /_static/no.png
    :width: 32
"""

# Credit http://stackoverflow.com/questions/42195468/how-can-i-inspect-an-attribute-of-a-module-without-importing-it?noredirect=1#comment71553012_42195468
def get_declaration_from_source(text, name="__all__"):
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets)==1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                return ast.literal_eval(node.value)
    raise NameError("name %r was not found"%(name,))

_maps = dict.fromkeys(COMPONENT_LIST)

for module, label in PLATFORM_LIST.items():
    path = os.path.join('../src', module, 'toga_'+module, '__init__.py')
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
            if platform in v:
                i.append('|yes|')
            else:
                i.append('|no|')
        writer.value_matrix.append(i)
    
    writer.write_table()
    doc.write(_footer)

for component, value in _maps.items():
    with open('../docs/reference/supported_platforms/{0}.rst'.format(component[0]), 'w+') as doc:
        writer = pytablewriter.RstGridTableWriter()
        writer.stream = doc
        # writer.table_name = "Supported platforms"
        writer.header_list = ["Component"] + _platforms
        writer.value_matrix = []
        i = list([component[0]])
        for platform in _platforms:
            if platform in value:
                i.append('|yes|')
            else:
                i.append('|no|')
        writer.value_matrix.append(i)
        writer.write_table()
        
        doc.write(_footer)

print("Done.")