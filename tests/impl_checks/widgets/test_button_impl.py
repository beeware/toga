import unittest
import ast
from ..utils import Visitor

from ..impl_definitions import BUTTON_DEF


class TestButtonImpl(unittest.TestCase):
    PATH = None

    def setUp(self):
        with open(self.PATH, 'r') as f:
            lines = f.read()
        self.tree = ast.parse(lines)
        self.visitor = Visitor()
        self.visitor.visit(self.tree)

    def test_required_functions_are_there(self):
        # check if all required functions are there
        functions = self.visitor.function_names
        def_functions = BUTTON_DEF.get('function')
        for func in def_functions:
            with self.subTest(func=func):
                self.assertIn(func, functions)


class TestButtonImplCocoa(TestButtonImpl):
    PATH = '../../../src/cocoa/toga_cocoa/widgets/button.py'


class TestButtonImpliOS(TestButtonImpl):
    PATH = '../../../src/iOS/toga_ios/widgets/button.py'


class TestButtonImplAndroid(TestButtonImpl):
    PATH = '../../../src/android/toga_android/widgets/button.py'
