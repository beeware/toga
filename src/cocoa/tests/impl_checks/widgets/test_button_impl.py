import os
from toga.test_utils import TestButtonImpl


class TestButtonImplCocoa(TestButtonImpl):
    PATH = os.path.join(os.path.dirname(__file__), '../../../toga_cocoa/widgets/button.py')