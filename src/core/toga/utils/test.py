import os
import ast
import unittest
from collections import namedtuple
import toga_dummy


class DefinitionExtractor:
    def __init__(self, file, emtpy=False):
        self.emtpy = emtpy
        self._classes = {}

        if not emtpy:
            # load the file and parse it with the ast module.
            with open(file, 'r') as f:
                lines = f.read()
            self.tree = ast.parse(lines)
            self.extract_classes()

    @property
    def class_names(self):
        return self._classes.keys()

    def extract_classes(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self._classes[node.name] = node

    def methods_of_class(self, class_name):
        methods = []
        if not self.emtpy:
            class_node = self._classes[class_name]
            for node in ast.walk(class_node):
                if isinstance(node, ast.FunctionDef):
                    methods.append(node.name)
        return methods


def create_impl_tests(root):
    """ Calling this function with a the path to a Toga backend will return
    the implementation tests for this backend.

    Args:
        root (str): The absolute path to a toga backend.

    Returns:
        A dictionary of test classes.
    """
    dummy_files = collect_dummy_files()
    tests = dict()
    for name, dummy_path in dummy_files:
        if 'widgets' in dummy_path:
            path = os.path.join(root, 'widgets/{}.py'.format(name))
        else:
            path = os.path.join(root, '{}.py'.format(name))

        tests['Test{}Impl'.format(name.capitalize())] = make_toga_impl_check_class(path, dummy_path)
    return tests


TestFile = namedtuple('TestFile', ['name', 'path'])


def collect_dummy_files(exclude_folder=None, exclude_files=None):
    dummy_files = []
    toga_dummy_base = os.path.dirname(toga_dummy.__file__)

    for root, dirs, files in os.walk(toga_dummy_base):
        # Exclude the 'test_utils' folder.
        if 'test_utils' in dirs:
            dirs.remove('test_utils')

        for file_ in files:
            # exclude non .py files or start with '__'
            if file_.startswith('__') or not file_.endswith('.py'):
                continue
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
        actual = DefinitionExtractor(path, emtpy=True)

    class TestClass(unittest.TestCase):
        pass

    if skip_test:
        @unittest.skip(skip_msg)
        def setup(self):
            pass

        setattr(TestClass, 'setUp', setup)

    def make_test_function(_foo, _bar):
        def fn(self):
            self.assertIn(_foo, _bar)

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

    return TestClass
