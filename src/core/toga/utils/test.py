import os
import ast
import unittest
from collections import namedtuple, defaultdict
from itertools import zip_longest

import toga_dummy


class NoDefault:
    """ This utility class to indicate that no default exists.
    The use of `None` is not possible because it itself could be a default value."""

    def __eq__(self, other):
        if isinstance(other, NoDefault):
            return True
        else:
            return False

    def __repr__(self):
        return 'no_default'


FunctionArguments = namedtuple('FunctionArguments', ['args', 'vararg', 'kwarg', 'kwonlyargs'])


class DefinitionExtractor:
    """ The DefinitionExtractor consumes a .py file and extracts information,
        with the help of the 'ast' module from it.
        Non existing files result in a empty DefinitionExtractor, this means the all properties
        return empty lists or dicts.

        Args:
            path (str): The path to the .py file.
    """

    def __init__(self, path):
        self.exists = os.path.isfile(path)
        self._classes = {}
        self._methods = defaultdict(dict)

        if self.exists:
            # open the file and parse it with the ast module.
            with open(path, 'r') as f:
                lines = f.read()
            self.tree = ast.parse(lines)
            self._extract_file()

    def _extract_file(self):
        self._extract_classes()
        self._extract_class_methods()

    @property
    def class_names(self):
        return self._classes.keys()

    @property
    def method_names(self):
        return self._methods.keys()

    def _extract_classes(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self._classes[node.name] = node

    @staticmethod
    def _get_function_defaults(node, kwonlyargs=False):
        if kwonlyargs:
            to_extract = node.kw_defaults
        else:
            to_extract = node.defaults

        defaults = []
        for default in to_extract:
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
        return defaults

    def _extract_class_methods(self):
        for class_name in self._classes:
            for node in ast.walk(self._classes[class_name]):
                if isinstance(node, ast.FunctionDef):
                    function_id = '{}.{}'.format(class_name, node.name)
                    self._methods[function_id]['node'] = node
                    self._methods[function_id]['arguments'] = self._extract_function_signature(node)

    def _extract_function_signature(self, node):
        for node in ast.walk(node):
            if isinstance(node, ast.arguments):
                # Extract positional arguments and possible default values.
                args = [arg.arg for arg in node.args]
                args_defaults = self._get_function_defaults(node)
                # Extract kwonlyargs and defaults.
                kwonlyargs = [arg.arg for arg in node.kwonlyargs]
                kwonlyargs_defaults = self._get_function_defaults(node, kwonlyargs=True)

                # Combine arguments and their corresponding default values,
                # if no default value exists fill it with a NoDefault object.
                args_plus_defaults = list(zip_longest(reversed(args),
                                                      reversed(args_defaults),
                                                      fillvalue=NoDefault()))
                kwonlyargs_plus_defaults = list(zip_longest(reversed(kwonlyargs),
                                                            reversed(kwonlyargs_defaults),
                                                            fillvalue=NoDefault()))

                vararg = node.vararg.arg if node.vararg is not None else None
                kwarg = node.kwarg.arg if node.kwarg is not None else None

                return FunctionArguments(
                    args=args_plus_defaults,
                    vararg=vararg,
                    kwarg=kwarg,
                    kwonlyargs=kwonlyargs_plus_defaults
                )

    def get_function_def(self, function_id):
        return self._methods[function_id]

    def methods_of_class(self, class_name):
        """ Get all methods names of a class.

        Args:
            class_name(str): Name of the class to extract the methodes

        Returns:
            Returns a `List` of (str) with all methods names of the class.

        Warnings:
            Does not return inherited methods. Only methods that are present in the class and the actual .py file.
        """
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

    def make_test_function(element, element_list, error_msg=None):
        def fn(self):
            self.assertIn(element, element_list, msg=error_msg)

        return fn

    for cls in expected.class_names:
        setattr(TestClass,
                'test_class_{}_exists_in_file_{}'.format(cls, os.path.basename(path)),
                make_test_function(cls, actual.class_names))

    for cls in expected.class_names:
        for method in expected.methods_of_class(cls):
            # create a test that checks if the method exists in the class.
            setattr(TestClass,
                    'test_method_{}_exists_in_class_{}'.format(method, cls),
                    make_test_function(method, actual.methods_of_class(cls)))

            # create tests that check for the right method arguments.
            method_id = '{}.{}'.format(cls, method)
            method_def = expected.get_function_def(method_id)['arguments']
            try:
                actual_method_def = actual.get_function_def(method_id)['arguments']
            except KeyError:
                actual_method_def = None

            if actual_method_def:
                # Create test whether the method takes the right arguments and if the arguments have the right name.
                # ARGS
                for arg in method_def.args:
                    setattr(TestClass,
                            'test_{}_takes_the_argument_{}_with_default_{}'.format(method, *arg),
                            make_test_function(arg, actual_method_def.args))
                # *varargs
                if method_def.vararg:
                    vararg = method_def.vararg
                    actual_vararg = actual_method_def.vararg if actual_method_def.vararg else []
                    setattr(TestClass,
                            'test_{}_takes_vararg_with_name_{}'.format(method, vararg),
                            make_test_function(vararg, actual_vararg))
                # **kwarg
                if method_def.kwarg:
                    kwarg = method_def.kwarg
                    actual_kwarg = actual_method_def.kwarg if actual_method_def.kwarg else []
                    setattr(TestClass,
                            'test_{}_takes_kwarg_with_name_{}'.format(method, kwarg),
                            make_test_function(kwarg, actual_kwarg,
                                               error_msg='The method does not take kwargs or the '
                                                         'variable is not named "{}".'.format(kwarg)))
                # kwonlyargs
                if method_def.kwonlyargs:
                    for kwonlyarg in method_def.kwonlyargs:
                        setattr(TestClass,
                                'test_{}_takes_kwonlyarg_{}_with_{}'.format(method, *kwonlyarg),
                                make_test_function(kwonlyarg, actual_method_def.kwonlyargs))

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
