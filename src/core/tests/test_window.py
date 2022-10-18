from pathlib import Path
from unittest.mock import MagicMock, patch, Mock

import toga
import toga_dummy
from toga.command import CommandSet
from toga_dummy.utils import TestCase


class TestWindow(TestCase):
    def setUp(self):
        super().setUp()
        self.window = toga.Window(factory=toga_dummy.factory)
        self.app = toga.App("test_name", "id.app", factory=toga_dummy.factory)

    def test_show_is_not_called_in_constructor(self):
        self.assertActionNotPerformed(self.window, "show")

    def test_show_raises_error_when_app_not_set(self):
        self.app = None
        with self.assertRaisesRegex(
            AttributeError, "^Can't show a window that doesn't have an associated app$"
        ):
            self.window.show()

    def test_window_show_with_app_set(self):
        self.window.app = self.app
        self.window.show()
        self.assertActionPerformed(self.window, "show")
        self.assertTrue(self.window.visible)
        self.assertValueSet(self.window, "visible", True)

    def test_hide_raises_error_when_app_not_set(self):
        self.app = None
        with self.assertRaisesRegex(
            AttributeError, "^Can't hide a window that doesn't have an associated app$"
        ):
            self.window.hide()

    def test_window_hide_with_app_set(self):
        self.window.app = self.app
        self.window.hide()
        self.assertActionPerformed(self.window, "hide")
        self.assertFalse(self.window.visible)
        self.assertValueSet(self.window, "visible", False)

    def test_window_show_by_setting_visible_to_true(self):
        self.window.app = self.app
        self.window.visible = True
        self.assertActionPerformed(self.window, "show")
        self.assertTrue(self.window.visible)
        self.assertValueSet(self.window, "visible", True)

    def test_window_show_by_setting_visible_to_false(self):
        self.window.app = self.app
        self.window.visible = False
        self.assertActionPerformed(self.window, "hide")
        self.assertFalse(self.window.visible)
        self.assertValueSet(self.window, "visible", False)

    def test_widget_created(self):
        self.assertIsNotNone(self.window.id)
        new_app = toga.App("error_name", "id.error", factory=toga_dummy.factory)
        self.window.app = self.app
        with self.assertRaisesRegex(
            Exception, "^Window is already associated with an App$"
        ):
            self.window.app = new_app

    def test_window_title(self):
        # Assert default value
        title = self.window.title
        self.assertEqual(title, "Toga")
        self.assertValueGet(self.window, "title")

        # Set a new window title
        self.window.title = "New title"
        self.assertValueSet(self.window, "title", "New title")

        # New window title can be retrieved
        title = self.window.title
        self.assertValueGet(self.window, "title")
        self.assertEqual(title, "New title")

        # Set a default window title
        self.window.title = None
        self.assertValueSet(self.window, "title", "Toga")

        # New window title can be retrieved
        title = self.window.title
        self.assertValueGet(self.window, "title")
        self.assertEqual(title, "Toga")

    def test_toolbar(self):
        toolbar = self.window.toolbar
        self.assertIsInstance(toolbar, CommandSet)

    def test_size(self):
        # Add some content
        mock_content = MagicMock(toga.Box(factory=toga_dummy.factory))
        self.window.content = mock_content

        # Confirm defaults
        self.assertEqual(self.window.size, (640, 480))
        self.assertValueGet(self.window, "size")

        # A new size can be assigned
        mock_content.reset_mock()
        new_size = (1200, 40)
        self.window.size = new_size
        self.assertValueSet(self.window, "size", new_size)

        # Side effect of setting window size is a refresh on window content
        self.window.content.refresh.assert_called_once_with()

        # New size can be retrieved
        self.assertEqual(self.window.size, new_size)
        self.assertValueGet(self.window, "size")

    def test_position(self):
        # Confirm defaults
        self.assertEqual(self.window.position, (100, 100))

        # A new position can be assigned
        new_position = (40, 79)
        self.window.position = new_position
        self.assertValueSet(self.window, "position", new_position)

        # New position can be retrieved
        self.assertEqual(self.window.position, new_position)
        self.assertValueGet(self.window, "position")

    def test_full_screen_set(self):
        self.assertFalse(self.window.full_screen)
        with patch.object(self.window, "_impl"):
            self.window.full_screen = True
            self.assertTrue(self.window.full_screen)
            self.window._impl.set_full_screen.assert_called_once_with(True)

    def test_on_close(self):
        with patch.object(self.window, "_impl"):
            self.app.windows += self.window
            self.assertIsNone(self.window._on_close)

            # set a new callback
            def callback(window, **extra):
                return "called {} with {}".format(type(window), extra)

            self.window.on_close = callback
            self.assertEqual(self.window.on_close._raw, callback)
            self.assertEqual(
                self.window.on_close("widget", a=1),
                "called <class 'toga.window.Window'> with {'a': 1}",
            )

    def test_on_close_at_create(self):
        def callback(window, **extra):
            return "called {} with {}".format(type(window), extra)

        window = toga.Window(factory=toga_dummy.factory, on_close=callback)
        self.app.windows += window

        self.assertEqual(window.on_close._raw, callback)
        self.assertEqual(
            window.on_close("widget", a=1),
            "called <class 'toga.window.Window'> with {'a': 1}",
        )

        self.assertActionPerformed(window, "close")

    def test_close(self):
        # Ensure the window is associated with an app
        self.app.windows += self.window
        with patch.object(self.window, "_impl"):
            self.window.close()
            self.window._impl.close.assert_called_once_with()

    def test_question_dialog(self):
        title = "question_dialog_test"
        message = "sample_text"

        self.window.question_dialog(title, message)

        self.assertActionPerformedWith(
            self.window, "question_dialog", title=title, message=message
        )

    def test_confirm_dialog(self):
        title = "confirm_dialog_test"
        message = "sample_text"

        self.window.confirm_dialog(title, message)

        self.assertActionPerformedWith(
            self.window, "confirm_dialog", title=title, message=message
        )

    def test_error_dialog(self):
        title = "error_dialog_test"
        message = "sample_text"

        self.window.error_dialog(title, message)

        self.assertActionPerformedWith(
            self.window, "error_dialog", title=title, message=message
        )

    def test_info_dialog(self):
        title = "info_dialog_test"
        message = "sample_text"

        self.window.info_dialog(title, message)

        self.assertActionPerformedWith(
            self.window, "info_dialog", title=title, message=message
        )

    def test_stack_trace_dialog(self):
        title = "stack_trace_dialog_test"
        message = "sample_text"
        content = "sample_content"
        retry = True

        self.window.stack_trace_dialog(title, message, content, retry)

        self.assertActionPerformedWith(
            self.window,
            "stack_trace_dialog",
            title=title,
            message=message,
            content=content,
            retry=retry,
        )

    def test_save_file_dialog_with_initial_directory(self):
        title = "save_file_dialog_test"
        suggested_filename = "/path/to/initial_filename.doc"
        file_types = ["test"]

        self.window.save_file_dialog(title, suggested_filename, file_types)

        self.assertActionPerformedWith(
            self.window,
            "save_file_dialog",
            title=title,
            filename="initial_filename.doc",
            initial_directory=Path("/path/to"),
            file_types=file_types,
        )

    def test_save_file_dialog_with_self_as_initial_directory(self):
        title = "save_file_dialog_test"
        suggested_filename = "./initial_filename.doc"
        file_types = ["test"]

        self.window.save_file_dialog(title, suggested_filename, file_types)

        self.assertActionPerformedWith(
            self.window,
            "save_file_dialog",
            title=title,
            filename="initial_filename.doc",
            initial_directory=None,
            file_types=file_types,
        )

    def test_open_file_dialog(self):
        title = "title_test"
        initial_directory = "/path/to/initial_directory"
        file_types = ["test"]
        multiselect = True

        self.window.open_file_dialog(title, initial_directory, file_types, multiselect)

        self.assertActionPerformedWith(
            self.window,
            "open_file_dialog",
            title=title,
            initial_directory=Path(initial_directory),
            file_types=file_types,
            multiselect=multiselect,
        )

    def test_select_folder_dialog(self):
        title = ""
        initial_directory = "/path/to/initial_directory"
        multiselect = True

        self.window.select_folder_dialog(title, initial_directory, multiselect)

        self.assertActionPerformedWith(
            self.window,
            "select_folder_dialog",
            title=title,
            initial_directory=Path(initial_directory),
            multiselect=multiselect,
        )

    def test_window_set_content_once(self):
        content = Mock()
        self.window.content = content

        self.assertEqual(content.window, self.window)

        self.assertActionPerformed(self.window, "clear content")
        self.assertActionPerformed(self.window, "set content")

    def test_window_set_content_twice(self):
        content1, content2 = Mock(), Mock()
        self.window.content = content1
        self.window.content = content2

        self.assertEqual(content1.window, None)
        self.assertEqual(content2.window, self.window)

        self.assertActionPerformed(self.window, "clear content")
        self.assertActionPerformed(self.window, "set content")
