from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

import toga
from toga.command import CommandSet
from toga.widgets.base import WidgetRegistry
from toga_dummy.utils import TestCase


class TestWindow(TestCase):
    def setUp(self):
        super().setUp()
        self.window = toga.Window()
        self.app = toga.App("test_name", "id.app")

    def test_window_widgets_registry_on_constructor(self):
        self.assertTrue(isinstance(self.window.widgets, WidgetRegistry))
        self.assertEqual(len(self.window.widgets), 0)

    def test_show_is_not_called_in_constructor(self):
        self.assertActionNotPerformed(self.window, "show")

    def test_show_raises_error_when_app_not_set(self):
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

    def test_set_window_application_twice(self):
        self.assertIsNotNone(self.window.id)
        new_app = toga.App("error_name", "id.error")
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

    def test_set_content_without_app(self):
        content = MagicMock()

        self.window.content = content
        self.assertEqual(content.window, self.window)
        self.assertIsNone(content.app)

    def test_set_content_with_app(self):
        content = MagicMock()

        self.window.app = self.app
        self.window.content = content

        self.assertEqual(content.window, self.window)
        self.assertEqual(content.app, self.app)

    def test_set_app_after_content(self):
        content = MagicMock()

        self.window.content = content
        self.window.app = self.app

        self.assertEqual(content.window, self.window)
        self.assertEqual(content.app, self.app)

    def test_set_app_adds_window_widgets_to_app(self):

        id0, id1, id2, id3 = "id0", "id1", "id2", "id3"
        widget1, widget2, widget3 = (
            toga.Label(id=id1, text="label 1"),
            toga.Label(id=id2, text="label 1"),
            toga.Label(id=id3, text="label 1"),
        )
        content = toga.Box(id=id0, children=[widget1, widget2, widget3])

        self.window.content = content

        # The window has widgets in it's repository
        self.assertEqual(len(self.window.widgets), 4)
        self.assertEqual(self.window.widgets[id0], content)
        self.assertEqual(self.window.widgets[id1], widget1)
        self.assertEqual(self.window.widgets[id2], widget2)
        self.assertEqual(self.window.widgets[id3], widget3)

        # The app doesn't know about the widgets
        self.assertEqual(len(self.app.widgets), 0)

        # Assign the window to the app
        self.window.app = self.app

        # The window's content widgets are now known to the app.
        self.assertEqual(len(self.app.widgets), 4)
        self.assertEqual(self.app.widgets[id0], content)
        self.assertEqual(self.app.widgets[id1], widget1)
        self.assertEqual(self.app.widgets[id2], widget2)
        self.assertEqual(self.app.widgets[id3], widget3)

    def test_size(self):
        # Add some content
        content = MagicMock()
        self.window.content = content

        # Confirm defaults
        self.assertEqual(self.window.size, (640, 480))
        self.assertValueGet(self.window, "size")

        content.refresh.assert_called_once_with()

    def test_set_size(self):
        # Add some content
        content = MagicMock()
        self.window.content = content

        # A new size can be assigned
        new_size = (1200, 40)
        self.window.size = new_size
        self.assertValueSet(self.window, "size", new_size)

        # Side effect of setting window size is a refresh on window content
        self.assertEqual(content.refresh.call_args_list, [call(), call()])

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
                return f"called {type(window)} with {extra}"

            self.window.on_close = callback
            self.assertEqual(self.window.on_close._raw, callback)
            self.assertEqual(
                self.window.on_close("widget", a=1),
                "called <class 'toga.window.Window'> with {'a': 1}",
            )

    def test_on_close_at_create(self):
        def callback(window, **extra):
            return f"called {type(window)} with {extra}"

        window = toga.Window(on_close=callback)
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
