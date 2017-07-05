import unittest
from ..utils.ast_helper import DefinitionExtractor
from toga_dummy.widgets import button


class TestButtonImpl(unittest.TestCase):
    PATH = None

    def setUp(self):
        if self.PATH is None:
            raise unittest.SkipTest('is a base class.')

        # the dummy backend defines everything expected
        self.expected = DefinitionExtractor(button.__file__)
        # the backend definition is the 'actual' implementation
        self.actual = DefinitionExtractor(self.PATH)

    def test_button_has_required_classes(self):
        # test if all expected classes are present
        actual_class_names = self.actual.class_names
        for cls in self.expected.class_names:
            with self.subTest(cls=cls):
                self.assertIn(cls, actual_class_names)

    def test_button_classes_have_required_methods(self):
        # Loop through the classes and check if all the expected methods are present.
        for cls in self.expected.class_names:
            actual_methods_names = self.actual.methods_of_class(cls)
            for method in self.expected.methods_of_class(cls):
                with self.subTest(method=method):
                    self.assertIn(method, actual_methods_names)
