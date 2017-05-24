import unittest
import inspect
import pyclbr
# from src.iOS.toga_iOS.widgets import button


class TestButtonImplementation(unittest.TestCase):
    def test_existence_of_button_class(self):
        print(inspect.getmoduleinfo('src/iOS/toga_iOS/widgets/button.py'))
        # print(pyclbr.readmodule('src.iOS.toga_iOS.widgets.button', path='src/iOS/toga_iOS/widgets/button.py'))
        print(pyclbr.readmodule('src.iOS.toga_iOS.widgets.button'))
        # self.assertTrue(inspect.isclass(button.Button))
