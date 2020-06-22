import os

from toga_dummy import test_implementation

globals().update(
    test_implementation.create_impl_tests(
        os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'toga_winforms')
        )
    )
)

from unittest.mock import patch, MagicMock
import toga
import toga_winforms
import toga_dummy
from toga.command import CommandSet
from toga_dummy.utils import TestCase

class TestWindow(TestCase):
    def setUp(self):
        super().setUp()
        self.window = toga.MainWindow(title="title")

    def test_open_file_dialog_with_custom_file_types_no_multiselect(self):
        title = "Open RTF file"
        init_dir = None
        multiselect = False
        file_types = ['rtf']
        #TODO: Mock the waiting function of winforms?
        #mock.patch('tenacity.BaseRetrying.wait', side_effect=lambda *args, **kwargs: 0)
        self.window.open_file_dialog(title, init_dir, file_types, multiselect)