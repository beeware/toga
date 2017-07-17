import os
import unittest
from .ast_utils import DefinitionExtractor


def create_impl_tests(root):
    """ Calling this function with a the path to a Toga backend will return
    the implementation tests for this backend.

    Args:
        root (str): The absolute path to a toga backend.

    Returns:
        A dictionary of test classes.
    """
    path_to_widgets = os.path.join(root, 'widgets')
    widgets = collect_widgets(path_to_widgets)
    tests = dict()
    for widget in widgets:
        tests['Test{}Impl'.format(widget.capitalize())] = \
            make_toga_impl_check_class(os.path.join(root, 'widgets/{}.py'.format(widget)))
    return tests


def collect_widgets(path_to_widget_folder):
    """

    Args:
        path_to_widget_folder (str):

    Returns:
        A list of widget file names (str).
    """
    widgets = []
    if os.path.isdir(path_to_widget_folder) and os.path.basename(path_to_widget_folder) == 'widgets':
        filenames = os.listdir(path_to_widget_folder)
        for file in filenames:
            if not file.startswith('__'):
                widgets.append(os.path.splitext(file)[0])
    return widgets


def make_toga_impl_check_class(path):
    actual = DefinitionExtractor(path)

    expected = DefinitionExtractor(
        os.path.join(os.path.join(os.path.dirname(__file__), '../widgets/'), os.path.basename(path)))

    class TestClass(unittest.TestCase):
        pass

    for cls in expected.class_names:
        def _fn(self):
            # print('Expected: {}, Actual: {}'.format(cls, actual.class_names))
            self.assertIn(cls, actual.class_names)

        setattr(TestClass, 'test_class_{}_exists_in_file_{}'.format(cls, os.path.basename(path)), _fn)

    for cls in expected.class_names:
        for method in expected.methods_of_class(cls):
            def _fn(self):
                # print('Expected: {}, Actual: {}'.format(method, actual.methods_of_class(cls)))
                self.assertIn(method, actual.methods_of_class(cls))

            setattr(TestClass, 'test_method_{}_exists_in_class_{}'.format(method, cls), _fn)

    return TestClass
