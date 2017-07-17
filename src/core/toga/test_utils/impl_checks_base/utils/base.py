import unittest
from .ast_helper import DefinitionExtractor


class ImplCheckMixin:
    """
    This is the base class for all the implementation base classes.
    """
    PATH = None
    PATH_DUMMY = None

    def setUp(self):
        # the dummy backend defines everything expected
        self.expected = DefinitionExtractor(self.PATH_DUMMY)
        # the backend definition is the 'actual' implementation
        print(self.PATH)
        self.actual = DefinitionExtractor(self.PATH)

    def test_module_has_required_classes(self):
        # test if all expected classes are present
        actual_class_names = self.actual.class_names
        for cls in self.expected.class_names:
            with self.subTest(cls=cls):
                self.assertIn(cls, actual_class_names)

    def test_module_classes_have_required_methods(self):
        # Loop through the classes and check if all the expected methods are present.
        for cls in self.expected.class_names:
            actual_methods_names = self.actual.methods_of_class(cls)
            for method in self.expected.methods_of_class(cls):
                with self.subTest(method=method):
                    self.assertIn(method, actual_methods_names)