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

with open('../docs/supported_platforms.rst', 'w+') as doc:
    writer = pytablewriter.RstGridTableWriter()
    writer.stream = doc
    writer.table_name = "Supported platforms"
    writer.header_list = ["Component"] + list(PLATFORM_LIST.keys())
    writer.value_matrix = []
    for c, v in _maps.items():
        i = list([c])
        for platform in PLATFORM_LIST.keys():
            if platform in v:
                i.append('yes')
            else:
                i.append('no')
        writer.value_matrix.append(i)
    
    writer.write_table()

print("Done.")