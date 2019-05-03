from unittest.mock import patch, MagicMock

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class AppTests(TestCase):
    def setUp(self):
        super().setUp()

        self.name = 'Test App'
        self.app_id = 'beeware.org'
        self.id = 'id'

        self.content = MagicMock()

        self.started = False
        def test_startup_function(app):
            self.started = True
            return self.content

        self.app = toga.App(self.name,
                            self.app_id,
                            startup=test_startup_function,
                            factory=toga_dummy.factory,
                            id=self.id)

    @patch('toga.app.get_platform_factory')
    def test_app_init_with_no_factory(self, mock_function):
        toga.App(self.name, self.app_id)
        mock_function.assert_called_once_with(None)

    def test_app_name(self):
        self.assertEqual(self.app.name, self.name)

    def test_app_app_id(self):
        self.assertEqual(self.app.app_id, self.app_id)

    def test_app_id(self):
        self.assertEqual(self.app.id, self.id)

    def test_app_icon(self):
        # App icon will be the default icon if you don't specify one
        self.assertEqual(self.app.icon, self.app.default_icon)

        # Set the icon to a different resource
        self.app.icon = "other.icns"
        self.assertEqual(self.app.icon.path, "other.icns")

    def test_current_window(self):
        impl = MagicMock()
        self.app._impl = impl

        self.assertEqual(
            self.app.current_window, impl.current_window().interface
        )

    def test_is_full_screen_false(self):
        self.assertFalse(self.app.is_full_screen)

    def test_is_full_screen_true(self):
        self.app._full_screen_windows = "not None"

        self.assertTrue(self.app.is_full_screen)

    @patch("toga.app.App.exit_full_screen")
    def test_app_set_full_screen_if_not(self, mock_function):
        self.app.set_full_screen()

        mock_function.assert_called_once_with()
        self.assertActionNotPerformed(self.app, "enter_full_screen")

    @patch("toga.app.App.exit_full_screen")
    def test_app_set_full_screen_if(self, mock_function):
        windows = MagicMock()
        self.app.set_full_screen(windows)

        mock_function.asser_not_called()
        self.assertActionPerformed(self.app, "enter_full_screen")
        self.assertEqual(self.app._full_screen_windows, (windows,))

    def test_app_exit_full_screen_if(self):
        self.app._full_screen_windows = "not None"
        self.app.exit_full_screen()

        self.assertActionPerformed(self.app, "exit_full_screen")
        self.assertIsNone(self.app._full_screen_windows)

    def test_app_exit_full_screen_if_not(self):
        self.app.exit_full_screen()

        self.assertActionNotPerformed(self.app, "exit_full_screen")
        self.assertIsNone(self.app._full_screen_windows)

    def test_app_show_cursor(self):
        self.app.show_cursor()

        self.assertActionPerformed(self.app, 'show_cursor')

    def test_app_hide_cursor(self):
        self.app.hide_cursor()

        self.assertActionPerformed(self.app, 'hide_cursor')

    def test_app_startup(self):
        self.app.startup()

        self.assertTrue(self.started)
        self.assertEqual(self.app.main_window.content, self.content)
        self.assertEqual(self.app.main_window.app, self.app)
        self.assertActionPerformed(self.app.main_window, 'show')

    def test_app_main_loop_call_impl_main_loop(self):
        self.app.main_loop()
        self.assertActionPerformed(self.app, 'main loop')

    def test_app_exit(self):
        self.app.exit()

        self.assertActionPerformed(self.app, 'exit')

    def test_on_exit(self):
        self.assertIsNone(self.app.on_exit)


class DocumentAppTests(TestCase):
    def setUp(self):
        super().setUp()

        self.name = 'Test Document App'
        self.app_id = 'beeware.org'
        self.id = 'id'

        self.content = MagicMock()

        self.app = toga.DocumentApp(
            self.name,
            self.app_id,
            factory=toga_dummy.factory,
            id=self.id
        )

    def test_app_documents(self):
        self.assertEqual(self.app.documents, [])

        doc = MagicMock()
        self.app._documents.append(doc)
        self.assertEqual(self.app.documents, [doc])
