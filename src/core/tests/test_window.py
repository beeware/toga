from unittest.mock import MagicMock, patch

import toga
import toga_dummy
from toga.command import CommandSet
from toga_dummy.utils import TestCase


class TestWindow(TestCase):
    def setUp(self):
        super().setUp()
        self.window = toga.Window(factory=toga_dummy.factory)
        self.app = toga.App('test_name', 'id.app', factory=toga_dummy.factory)

    def test_raises_error_when_app_not_set(self):
        self.app = None
        with self.assertRaises(AttributeError):
            self.window.show()

    def test_widget_created(self):
        self.assertIsNotNone(self.window.id)
        new_app = toga.App('error_name', 'id.error', factory=toga_dummy.factory)
        self.window.app = self.app
        with self.assertRaises(Exception):
            self.window.app = new_app

    def test_window_title(self):
        title = self.window.title
        self.assertEqual(title, 'Toga')

    def test_toolbar(self):
        toolbar = self.window.toolbar
        self.assertIsInstance(toolbar, CommandSet)

    def test_size_getter_and_setter(self):
        # Add some content
        mock_content = MagicMock(toga.Box(factory=toga_dummy.factory))
        self.window.content = mock_content

        # Confirm defaults
        self.assertEqual((640, 480), self.window.size)

        # Test setter
        new_size = (1200, 40)
        mock_content.reset_mock()
        with patch.object(self.window, '_impl'):
            self.window.size = new_size
            self.window._impl.set_size.assert_called_once_with(new_size)
            self.window.content.refresh.assert_called_once_with()

    def test_position_getter_and_setter(self):
        # Confirm defaults
        self.assertEqual((100, 100), self.window.position)

        # Test setter
        new_position = (40, 79)
        with patch.object(self.window, '_impl'):
            self.window.position = new_position
            self.window._impl.set_position.assert_called_once_with(new_position)

    def test_full_screen_set(self):
        self.assertFalse(self.window.full_screen)
        with patch.object(self.window, '_impl'):
            self.window.full_screen = True
            self.assertTrue(self.window.full_screen)
            self.window._impl.set_full_screen.assert_called_once_with(True)

    def test_on_close(self):
        with patch.object(self.window, '_impl'):
            self.app.windows += self.window
            self.assertIsNone(self.window._on_close)

            # set a new callback
            def callback(window, **extra):
                return 'called {} with {}'.format(type(window), extra)

            self.window.on_close = callback
            self.assertEqual(self.window.on_close._raw, callback)
            self.assertEqual(
                self.window.on_close('widget', a=1),
                "called <class 'toga.window.Window'> with {'a': 1}"
            )

    def test_close(self):
        with patch.object(self.window, "_impl"):
            self.window.close()
            self.window._impl.close.assert_called_once_with()

    def test_question_dialog(self):
        title = "question_dialog_test"
        message = "sample_text"
        with patch.object(self.window, "_impl"):
            self.window.question_dialog(title, message)
            self.window._impl.question_dialog.assert_called_once_with(
                title, message)

    def test_confirm_dialog(self):
        title = "confirm_dialog_test"
        message = "sample_text"
        with patch.object(self.window, "_impl"):
            self.window.confirm_dialog(title, message)
            self.window._impl.confirm_dialog.assert_called_once_with(
                title, message)

    def test_error_dialog(self):
        title = "error_dialog_test"
        message = "sample_text"
        with patch.object(self.window, "_impl"):
            self.window.error_dialog(title, message)
            self.window._impl.error_dialog.assert_called_once_with(
                title, message)

    def test_info_dialog(self):
        title = "info_dialog_test"
        message = "sample_text"
        with patch.object(self.window, "_impl"):
            self.window.info_dialog(title, message)
            self.window._impl.info_dialog.assert_called_once_with(
                title, message)

    def test_stack_trace_dialog(self):
        title = "stack_trace_dialog_test"
        message = "sample_text"
        content = "sample_content"
        retry = True
        with patch.object(self.window, "_impl"):
            self.window.stack_trace_dialog(title, message, content, retry)
            self.window._impl.stack_trace_dialog.assert_called_once_with(
                title, message, content, retry)

    def test_save_file_dialog(self):
        title = "save_file_dialog_test"
        suggested_filename = "sample_filename_test"
        file_types = ['test']
        with patch.object(self.window, "_impl"):
            self.window.save_file_dialog(title, suggested_filename, file_types)
            self.window._impl.save_file_dialog.assert_called_once_with(
                title, suggested_filename, file_types)

    def test_open_file_dialog(self):
        title = "title_test"
        initial_directory = "initial_directory_test"
        file_types = ["test"]
        multiselect = True
        with patch.object(self.window, "_impl"):
            self.window.open_file_dialog(title, initial_directory, file_types, multiselect)
            self.window._impl.open_file_dialog.assert_called_once_with(
                title, initial_directory, file_types, multiselect)

    def test_select_folder_dialog(self):
        title = ""
        initial_directory = ""
        multiselect = True
        with patch.object(self.window, "_impl"):
            self.window.select_folder_dialog(title, initial_directory, multiselect)
            self.window._impl.select_folder_dialog.assert_called_once_with(
                title, initial_directory, multiselect)
