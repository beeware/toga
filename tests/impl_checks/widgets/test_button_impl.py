import unittest
import ast

from ..utils import Visitor, get_class_methods

# This dictionary defines what attributes a platform
# specific implementation of a toga.Button needs to have.
BUTTON_DEF = {'classes': ['Button'],
              'functions': ['create', 'set_label', 'rehint']}


class TestButtonImpl(unittest.TestCase):
    PATH = None

    def setUp(self):
        # Skip this test when we are in the base class.
        if self.PATH is None:
            raise unittest.SkipTest('is a base class.')
        # load the file and parse it with the ast module.
        with open(self.PATH, 'r') as f:
            lines = f.read()
        self.tree = ast.parse(lines)
        self.visitor = Visitor()
        self.visitor.visit(self.tree)

    def test_required_classes_are_there(self):
        classes = self.visitor.class_names
        def_classes = BUTTON_DEF.get('classes')
        def_functions = BUTTON_DEF.get('functions')

        for cls in def_classes:
            with self.subTest(cls=cls):
                self.assertIn(cls, classes)

    def test_button_class_has_required_methods(self):
        def_classes = BUTTON_DEF.get('classes')
        def_functions = BUTTON_DEF.get('functions')

        for cls in def_classes:
            methods = get_class_methods(self.tree, cls)
            print('methods: ', methods)
            for func in def_functions:
                with self.subTest(cls=cls):
                    self.assertIn(func, methods)


class TestButtonImplCocoa(TestButtonImpl):
    PATH = '../src/cocoa/toga_cocoa/widgets/button.py'


@unittest.skip('Not ported to new Toga version.')
class TestButtonImpliOS(TestButtonImpl):
    PATH = '../src/iOS/toga_ios/widgets/button.py'


@unittest.skip('Not ported to new Toga version.')
class TestButtonImplAndroid(TestButtonImpl):
    PATH = '../src/android/toga_android/widgets/button.py'


@unittest.skip('Not ported to new Toga version.')
class TestButtonImplDjango(TestButtonImpl):
    PATH = '../src/django/toga_django/widgets/button.py'


@unittest.skip('Not implemented yet.')
class TestButtonImplFlask(TestButtonImpl):
    PATH = '../src/flask/toga_flask/widgets/button.py'


@unittest.skip('Not ported to new Toga version.')
class TestButtonImplGTK(TestButtonImpl):
    PATH = '../src/gtk/toga_gtk/widgets/button.py'


@unittest.skip('Not implemented yet.')
class TestButtonImplPyramid(TestButtonImpl):
    PATH = '../src/pyramid/toga_pyramid/widgets/button.py'


@unittest.skip('Not ported to new Toga version.')
class TestButtonImplWin32(TestButtonImpl):
    PATH = '../src/win32/toga_win32/widgets/button.py'


@unittest.skip('Not ported to new Toga version.')
class TestButtonImplWinforms(TestButtonImpl):
    PATH = '../src/winforms/toga_winforms/widgets/button.py'
    