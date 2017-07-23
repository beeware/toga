import os
import ast
import unittest
from collections import namedtuple, defaultdict
from itertools import zip_longest

import toga_dummy


class DefinitionExtractor:
    def __init__(self, path):
        """ The DefinitionExtractor consumes a .py file and extracts information,
        with the help of the 'ast' module from it.
        Non existing files result in a empty DefinitionExtractor, this means the all properties
        return empty lists or dicts.

        Args:
            path (str): The path to the .py file.
        """
        self.exists = os.path.isfile(path)
        self._classes = {}
        self._methods = defaultdict(dict)

        if self.exists:
            # open the file and parse it with the ast module.
            with open(path, 'r') as f:
                lines = f.read()
            self.tree = ast.parse(lines)
            self.extract_classes()
            self._extract_class_methods()

    @property
    def class_names(self):
        return self._classes.keys()

    @property
    def method_names(self):
        return self._methods.keys()

    def extract_classes(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self._classes[node.name] = node

    def _extract_class_methods(self):
        for class_name in self._classes:
            for node in ast.walk(self._classes[class_name]):
                if isinstance(node, ast.FunctionDef):
                    self._methods['{}.{}'.format(class_name, node.name)]['node'] = node

        updated_methods = defaultdict(dict)
        for method in self._methods:
            for node in ast.walk(self._methods[method]['node']):
                if isinstance(node, ast.arguments):
                    args = [arg.arg for arg in node.args]
                    defaults = []
                    for default in node.defaults:
                        if isinstance(default, ast.NameConstant):
                            print(default.value)
                            defaults.append(default.value)
                        elif isinstance(default, ast.Str):
                            print(default.s)
                            defaults.append(default.s)
                        elif isinstance(default, ast.Num):
                            print(default.n)
                            defaults.append(default.n)
                        elif isinstance(default, ast.Tuple) or isinstance(default, ast.List):
                            defaults.append(default.elts)
                        else:
                            raise RuntimeWarning('ast classes of type "{}" can not be handled at the moment. '
                                                 'Please implement to make this warning disappear.'.format(default))

                    args_defaults_combi = zip_longest(reversed(args), reversed(defaults), fillvalue='no_default')

                    vararg = node.vararg.arg if node.vararg is not None else None
                    kwarg = node.kwarg.arg if node.kwarg is not None else None

                    updated_methods[method]['arguments'] = {'args': [x for x in args_defaults_combi],
                                                            'vararg': vararg,
                                                            'kwarg': kwarg}
        else:
            self._methods = updated_methods

    def get_function_def(self, function_id):
        return self._methods[function_id]

    def methods_of_class(self, class_name):
        methods = []
        if self.exists:
            class_node = self._classes[class_name]
            for node in ast.walk(class_node):
                if isinstance(node, ast.FunctionDef):
                    methods.append(node.name)
        return methods


def get_required_files(path_to_backend):
    name = os.path.basename(path_to_backend)
    if name in ['toga_cocoa', 'toga_gtk', 'toga_gtk', 'toga_winforms', 'toga_win32']:
        return TOGA_BASE_FILES + TOGA_DESKTOP_FILES
    if name in ['toga_iOS', 'toga_android']:
        return TOGA_BASE_FILES + TOGA_MOBILE_FILES
    else:
        raise RuntimeError('Couldn\'t identify a supported host platform: "{}"'.format(name))


def create_impl_tests(root):
    """ Calling this function with a the path to a Toga backend will return
    the implementation tests for this backend.

    Args:
        root (str): The absolute path to a toga backend.

    Returns:
        A dictionary of test classes.
    """
    dummy_files = collect_dummy_files(get_required_files(root))
    tests = dict()
    for name, dummy_path in dummy_files:
        if 'widgets' in dummy_path:
            path = os.path.join(root, 'widgets/{}.py'.format(name))
        else:
            path = os.path.join(root, '{}.py'.format(name))

        tests['Test{}Impl'.format(name.capitalize())] = make_toga_impl_check_class(path, dummy_path)
    return tests


TestFile = namedtuple('TestFile', ['name', 'path'])


def collect_dummy_files(required_files):
    dummy_files = []
    toga_dummy_base = os.path.dirname(toga_dummy.__file__)

    for root, dirs, files in os.walk(toga_dummy_base):

        for file_ in files:
            # exclude non .py files or start with '__'
            if file_.startswith('__') or not file_.endswith('.py'):
                continue

            if file_ in required_files:
                f = TestFile(file_[:-3], os.path.join(root, file_))
                dummy_files.append(f)

    return dummy_files


def make_toga_impl_check_class(path, dummy_path):
    expected = DefinitionExtractor(dummy_path)
    if os.path.isfile(path):
        skip_test = False
        actual = DefinitionExtractor(path)
    else:
        skip_test = True
        skip_msg = 'File does not exist: {}'.format(path)
        actual = DefinitionExtractor(path)

    class TestClass(unittest.TestCase):
        pass

    if skip_test:
        @unittest.skip(skip_msg)
        def setup(self):
            pass

        setattr(TestClass, 'setUp', setup)

    def make_test_function(element, element_list, msg=None):
        def fn(self):
            self.assertIn(element, element_list, msg=msg)

        return fn

    for cls in expected.class_names:
        setattr(TestClass,
                'test_class_{}_exists_in_file_{}'.format(cls, os.path.basename(path)),
                make_test_function(cls, actual.class_names))

    for cls in expected.class_names:
        for method in expected.methods_of_class(cls):
            setattr(TestClass,
                    'test_method_{}_exists_in_class_{}'.format(method, cls),
                    make_test_function(method, actual.methods_of_class(cls)))

            method_id = '{}.{}'.format(cls, method)
            method_def = expected.get_function_def(method_id)
            try:
                actual_method_def = actual.get_function_def(method_id)['arguments']['args']
            except KeyError:
                actual_method_def = []
            for arg in method_def['arguments']['args']:
                setattr(TestClass,
                        'test_{}_takes_the_right_argument_{}_with_{}'.format(method, *arg),
                        make_test_function(arg, actual_method_def))

    return TestClass


# A list of files that must be present in every
# valid Toga backend implementation.
TOGA_BASE_FILES = [
    'app.py',
    'command.py',
    'container.py',
    'dialogs.py',
    'factory.py',
    'font.py',
    'window.py',
    # Widgets
    'base.py',
    'box.py',
    'button.py',
    'icon.py',
    'image.py',
    'imageview.py',
    'label.py',
    'multilinetextinput.py',
    'numberinput.py',
    'optioncontainer.py',
    'passwordinput.py',
    'progressbar.py',
    'scrollcontainer.py',
    'selection.py',
    'slider.py',
    'switch.py',
    'table.py',
    'textinput.py',
    'tree.py',
    'webview.py'
]

# Files that must only be present
# in mobile implementations of Toga.
TOGA_MOBILE_FILES = [
    'navigationview.py',
    'detailedlist.py',
]

# Files that must only be present
# in desktop implementations of Toga.
TOGA_DESKTOP_FILES = [
    'splitcontainer.py',
]
