import ast
import os
from os.path import join
import unittest
from collections import defaultdict, namedtuple
from itertools import zip_longest
from pathlib import Path

import toga_dummy


class NoDefault:
    """ This utility class to indicate that no argument default exists.
    The use of `None` is not possible because it itself could be a default argument value."""

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

    def __init__(self, path, platform_category=None):
        self.exists = os.path.isfile(path)
        self._classes = {}
        self._methods = defaultdict(dict)
        self.platform = platform_category if platform_category else None

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
                if self.is_required_for_platform(node):
                    self._classes[node.name] = node  # use the class name as the key
            elif isinstance(node, ast.Assign):
                # Allow a class with no new methods to be defined by assigning from an
                # existing class.
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self._classes[target.id] = node

    def is_required_for_platform(self, node):
        """ Checks if the class or function is required for the given platform.
        It looks for a decorator with the name `not_required_on`.

        Returns:
            `True` if the class/function is required for the platform.
            `False` if the class/function is not required and can be dropped for this platform.
        """
        if node.decorator_list:  # check if a decorator list exists
            for decorator in node.decorator_list:
                try:
                    # @not_required is a bare decorator, so the decorator node
                    # has an `id` attribute.
                    # @not_required_on is a decorator factory, so the decorator
                    # node contains a function that has an id.
                    if getattr(decorator, 'id', None) == 'not_required':
                        return False
                    elif decorator.func.id == 'not_required_on':
                        platforms_to_skip = [arg.s for arg in decorator.args]
                        if self.platform.intersection(set(platforms_to_skip)):
                            return False
                except Exception:
                    pass
        return True

    @staticmethod
    def _get_function_defaults(node, kwonlyargs=False):
        if kwonlyargs:
            to_extract = node.kw_defaults
        else:
            to_extract = node.defaults

        defaults = []
        for default in to_extract:
            if isinstance(default, ast.NameConstant):
                defaults.append(default.value)
            elif isinstance(default, ast.Str):
                defaults.append(default.s)
            elif isinstance(default, ast.Num):
                defaults.append(default.n)
            elif isinstance(default, ast.Tuple) or isinstance(default, ast.List):
                defaults.append(default.elts)
            elif isinstance(default, ast.Call):
                defaults.append(default.func)
            elif isinstance(default, ast.Attribute):
                defaults.append(default.value)
            elif isinstance(default, ast.Name):
                defaults.append(default.id)
            else:
                raise RuntimeWarning('ast classes of type "{}" can not be handled at the moment. '
                                     'Please implement to make this warning disappear.'.format(default))
        return defaults

    def _extract_class_methods(self):
        """ Extract all the methods from the classes and save them in `self.methods`.
        Use the combination of class and method name, like so: `<class_name>.<method_name>` as the key.
        """
        for class_name in self._classes:
            for node in ast.walk(self._classes[class_name]):
                if isinstance(node, ast.FunctionDef):
                    if self.is_required_for_platform(node):
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
            if class_name in self._classes.keys():
                class_node = self._classes[class_name]
                for node in ast.walk(class_node):
                    if isinstance(node, ast.FunctionDef):
                        if self.is_required_for_platform(node):
                            methods.append(node.name)
        return methods


def get_platform_category(path_to_backend):
    name = os.path.basename(path_to_backend)
    if name in ['toga_cocoa', 'toga_gtk', 'toga_winforms', 'toga_win32', 'toga_uwp']:
        return {'desktop', name.split('_')[-1]}
    elif name in ['toga_iOS', 'toga_android']:
        return {'mobile', name.split('_')[-1]}
    elif name in ['toga_django', 'toga_flask', 'toga_pyramid']:
        return {'web', name.split('_')[-1]}
    elif name in ['toga_curses', ]:
        return {'console', name.split('_')[-1]}
    elif name in ['toga_tvOS', ]:
        return {'settop', name.split('_')[-1]}
    elif name in ['toga_watchOS', ]:
        return {'watch', name.split('_')[-1]}
    else:
        raise RuntimeError('Couldn\'t identify a supported host platform: "{}"'.format(name))


def get_required_files(path_to_backend):
    # Find the list of files in the dummy backend
    # that aren't *this* file, or an __init__.py.
    files = [
        str(p.relative_to(Path(__file__).parent))
        for p in Path(__file__).parent.rglob('**/*.py')
        if str(p) != __file__ and p.name != '__init__.py'
    ]
    name = os.path.basename(path_to_backend)
    if name in ['toga_cocoa', 'toga_gtk', 'toga_winforms', 'toga_win32', 'toga_uwp']:
        for f in TOGA_DESKTOP_EXCLUDED_FILES:
            files.remove(f)
    elif name in ['toga_iOS', 'toga_android']:
        for f in TOGA_MOBILE_EXCLUDED_FILES:
            files.remove(f)
    elif name in ['toga_django', 'toga_flask', 'toga_pyramid']:
        for f in TOGA_WEB_EXCLUDED_FILES:
            files.remove(f)
    elif name in ['toga_curses', ]:
        for f in TOGA_CONSOLE_EXCLUDED_FILES:
            files.remove(f)
    elif name in ['toga_tvOS', ]:
        for f in TOGA_SETTOP_EXCLUDED_FILES:
            files.remove(f)
    elif name in ['toga_watchOS', ]:
        for f in TOGA_WATCH_EXCLUDED_FILES:
            files.remove(f)
    else:
        raise RuntimeError('Couldn\'t identify a supported host platform: "{}"'.format(name))
    return files


def create_impl_tests(root):
    """ Calling this function with a the path to a Toga backend will return
    the implementation tests for this backend.

    Args:
        root (str): The absolute path to a toga backend.

    Returns:
        A dictionary of test classes.
    """
    platform_category = get_platform_category(root)
    dummy_files = collect_dummy_files(get_required_files(root))
    tests = {}
    for name, dummy_path in dummy_files:
        if 'widgets' in dummy_path:
            path = os.path.join(root, 'widgets/{}.py'.format(name))
        else:
            path = os.path.join(root, '{}.py'.format(name))

        tests.update(make_toga_impl_check_class(path, dummy_path, platform_category))
    return tests


TestFile = namedtuple('TestFile', ['name', 'path'])


def collect_dummy_files(required_files):
    dummy_files = []
    toga_dummy_base = os.path.dirname(toga_dummy.__file__)

    for root, dirs, filenames in os.walk(toga_dummy_base):
        for filename in filenames:
            # exclude non .py filenames or start with '__'
            if filename.startswith('__') or not filename.endswith('.py'):
                continue

            full_filename = os.path.join(root, filename)[len(toga_dummy_base) + 1:]
            if full_filename in required_files:
                f = TestFile(filename[:-3], os.path.join(root, filename))
                dummy_files.append(f)

    return dummy_files


def make_test_function(element, element_list, error_msg=None):
    def fn(self):
        self.assertIn(element, element_list, msg=error_msg if error_msg else fn.__doc__)

    return fn


def make_test_class(path, cls, expected, actual, skip):
    class_name = '{}ImplTest'.format(cls)
    test_class = type(class_name, (unittest.TestCase,), {})

    if skip:
        test_class = unittest.skip(skip)(test_class)

    fn = make_test_function(cls, actual.class_names)
    fn.__doc__ = (
        "Expect class {} to be defined in {}, to be consistent with dummy implementation"
    ).format(cls, path)
    test_class.test_class_exists = fn

    for method in expected.methods_of_class(cls):
        # create a test that checks if the method exists in the class.
        fn = make_test_function(method, actual.methods_of_class(cls))
        fn.__doc__ = 'The method {}.{}(...) exists'.format(cls, method)
        setattr(test_class, 'test_{}_exists'.format(method), fn)

        # create tests that check for the right method arguments.
        method_id = '{}.{}'.format(cls, method)
        method_def = expected.get_function_def(method_id)['arguments']
        try:
            actual_method_def = actual.get_function_def(method_id)['arguments']
        except KeyError:
            actual_method_def = None

        if actual_method_def:
            # Create test whether the method takes the right arguments
            # and if the arguments have the right name.

            # ARGS
            for arg in method_def.args:
                fn = make_test_function(arg, actual_method_def.args)
                fn.__doc__ = "The argument {}.{}(..., {}={}, ...) exists".format(cls, method, *arg)
                setattr(
                    test_class,
                    'test_{}_arg_{}_default_{}'.format(method, *arg),
                    fn
                )

            # *varargs
            if method_def.vararg:
                vararg = method_def.vararg
                actual_vararg = actual_method_def.vararg if actual_method_def.vararg else []
                fn = make_test_function(vararg, actual_vararg)
                fn.__doc__ = "The vararg {}.{}(..., *{}, ...) exists".format(cls, method, vararg)
                setattr(
                    test_class,
                    'test_{}_vararg_{}'.format(method, vararg),
                    fn
                )

            # **kwarg
            if method_def.kwarg:
                kwarg = method_def.kwarg
                actual_kwarg = actual_method_def.kwarg if actual_method_def.kwarg else []
                fn = make_test_function(kwarg, actual_kwarg,
                                        error_msg='The method does not take kwargs or the '
                                                  'variable is not named "{}".'.format(kwarg))
                fn.__doc__ = "The kw argument {}.{}(..., **{}, ...) exists".format(cls, method, kwarg)
                setattr(
                    test_class,
                    'test_{}_kw_{}'.format(method, kwarg),
                    fn
                )

            # kwonlyargs
            if method_def.kwonlyargs:
                for kwonlyarg in method_def.kwonlyargs:
                    fn = make_test_function(kwonlyarg, actual_method_def.kwonlyargs)
                    fn.__doc__ = "The kwonly argument {}.{}(..., {}={}, ...) exists".format(cls, method, *kwonlyarg)
                    setattr(
                        test_class,
                        'test_{}_kwonly_{}_default_{}'.format(method, *kwonlyarg),
                        fn
                    )

    return class_name, test_class


def make_toga_impl_check_class(path, dummy_path, platform):
    prefix = os.path.commonprefix([path, dummy_path])
    expected = DefinitionExtractor(dummy_path, platform)
    if os.path.isfile(path):
        skip = None
        actual = DefinitionExtractor(path)
    else:
        skip = 'Implementation file {} does not exist'.format(path[len(prefix):])
        actual = DefinitionExtractor(path)

    test_classes = {}

    for cls in expected.class_names:
        class_name, test_class = make_test_class(path[len(prefix):], cls, expected, actual, skip)
        test_classes[class_name] = test_class

    return test_classes


# Files that do not need to be present in mobile implementations of Toga.
TOGA_MOBILE_EXCLUDED_FILES = [
    join('widgets', 'splitcontainer.py'),
]

# Files that do not need to be present in desktop implementations of Toga.
TOGA_DESKTOP_EXCLUDED_FILES = [
]

# Files do not need to be present in web implementations of Toga.
TOGA_WEB_EXCLUDED_FILES = [
    join('widgets', 'splitcontainer.py'),
]

# Files that do not need to be present in console implementations of Toga.
TOGA_CONSOLE_EXCLUDED_FILES = [
]

# Files that do not need to be present in set-top box implementations of Toga.
TOGA_SETTOP_EXCLUDED_FILES = [
]

# Files that do not need to be present in watch implementations of Toga.
TOGA_WATCH_EXCLUDED_FILES = [
]
