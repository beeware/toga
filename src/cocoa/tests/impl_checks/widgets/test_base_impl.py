import os
from toga.test_utils import TestBaseImpl


class TestBaseImplCocoa(TestBaseImpl):
    PATH = os.path.join(os.path.dirname(__file__), '../../../toga_cocoa/widgets/base.py')