"""
 This script builds a table to show the supported platforms for Toga and the components that are supported
 
 Requires: pytablewriter from PyPi
"""
import ast
import os
import sys
import pytablewriter

"""
A dictionary of components, index is the module name and value is the class name
"""
COMPONENT_LIST =  ['App', 'MainWindow', 'Window',
                   'Command', 'SEPARATOR', 'SPACER',
                   'EXPANDING_SPACER', 'Box', 'Button',
                   'Icon', 'TIBERIUS_ICON', 'Image',
                   'ImageView', 'Font', 'Label', 'MultilineTextInput',
                   'NumberInput', 'OptionContainer', 'PasswordInput',
                   'ProgressBar', 'ScrollContainer', 'Selection',
                   'SplitContainer', 'Table', 'TextInput',
                   'Tree', 'WebView']

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
        for name in names:
            if name in _maps.keys():
                if _maps[name] is None:
                    _maps[name] = list()
                _maps[name].append(module)

_platforms = list(PLATFORM_LIST.keys())

# Write the overall component compatibility list
with open('../docs/supported_platforms.rst', 'w+') as doc:
    writer = pytablewriter.RstGridTableWriter()
    writer.stream = doc
    # writer.table_name = "Supported platforms"
    writer.header_list = ["Component"] + _platforms
    writer.value_matrix = []
    for c, v in _maps.items():
        i = list([c])
        for platform in _platforms:
            if platform in v:
                i.append('|yes|')
            else:
                i.append('|no|')
        writer.value_matrix.append(i)
    
    writer.write_table()
    doc.write(_footer)

for component, value in _maps.items():
    with open('../docs/reference/supported_platforms/{0}.rst'.format(component), 'w+') as doc:
        writer = pytablewriter.RstGridTableWriter()
        writer.stream = doc
        # writer.table_name = "Supported platforms"
        writer.header_list = ["Component"] + _platforms
        writer.value_matrix = []
        i = list([component])
        for platform in _platforms:
            if platform in value:
                i.append('|yes|')
            else:
                i.append('|no|')
        writer.value_matrix.append(i)
        writer.write_table()
        
        doc.write(_footer)

print("Done.")