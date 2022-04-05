from unittest.mock import MagicMock, patch

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class AppTests(TestCase):
    def setUp(self):
        super().setUp()

        self.name = 'Test App'
        self.app_id = 'org.beeware.test-app'
        self.id = 'dom-id'

        self.content = MagicMock()

        self.started = False

        def test_startup_function(app):
            self.started = True
            return self.content

        self.app = toga.App(
            formal_name=self.name,
            app_id=self.app_id,
            startup=test_startup_function,
            factory=toga_dummy.factory,
            id=self.id
        )

    def test_app_name(self):
        self.assertEqual(self.app.name, self.name)

    def test_app_icon(self):
        # App icon will default to a name autodetected from the running module
        self.assertEqual(self.app.icon.path, 'resources/toga')

        # This icon will not be bound, since app icons are bound by the
        # platform layer.
        self.assertIsNone(self.app.icon._impl)

        # Bind it explicitly to validate binding can succeed.
        self.app.icon.bind(self.app.factory)
        self.assertIsNotNone(self.app.icon._impl)

        # Set the icon to a different resource
        self.app.icon = "other.icns"
        self.assertEqual(self.app.icon.path, "other.icns")
        self.app.icon.bind(self.app.factory)

        # This icon name will *not* exist. The Impl will be the DEFAULT_ICON's impl
        self.assertEqual(self.app.icon._impl, toga.Icon.DEFAULT_ICON._impl)

    def test_app_app_id(self):
        self.assertEqual(self.app.app_id, self.app_id)

    def test_app_id(self):
        self.assertEqual(self.app.id, self.id)

    @patch('toga.app.get_platform_factory')
    def test_app_init_with_no_factory(self, mock_function):
        toga.App(self.name, self.app_id)
        mock_function.assert_called_once_with(None)

    def test_app_main_loop_call_impl_main_loop(self):
        self.app.main_loop()
        self.assertActionPerformed(self.app, 'main loop')

    def test_app_startup(self):
        self.app.startup()

        self.assertTrue(self.started)
        self.assertEqual(self.app.main_window.content, self.content)
        self.assertEqual(self.app.main_window.app, self.app)
        self.assertActionPerformed(self.app.main_window, 'show')

    def test_is_full_screen(self):
        self.assertFalse(self.app.is_full_screen)

        self.app.set_full_screen(self.app.main_window)
        self.assertTrue(self.app.is_full_screen)

        self.app.set_full_screen(["window1", "window2", "window3"])
        self.assertTrue(self.app.is_full_screen)

        self.app.set_full_screen()
        self.assertFalse(self.app.is_full_screen)

    def test_app_exit(self):
        def exit_handler(widget):
            return True
        self.app.on_exit = exit_handler
        self.assertIs(self.app.on_exit._raw, exit_handler)
        self.app.exit()

        self.assertActionPerformed(self.app, 'exit')

    def test_full_screen(self):
        # set full screen and exit full screen
        self.app.set_full_screen(self.app.main_window)
        self.assertTrue(self.app.is_full_screen)
        self.app.exit_full_screen()
        self.assertFalse(self.app.is_full_screen)
        # set full screen and set full with no args
        self.app.set_full_screen(self.app.main_window)
        self.assertTrue(self.app.is_full_screen)
        self.app.set_full_screen()
        self.assertFalse(self.app.is_full_screen)

    def test_add_window(self):
        test_window = toga.Window(factory=toga_dummy.factory)

        self.assertEqual(len(self.app.windows), 0)
        self.app.windows += test_window
        self.assertEqual(len(self.app.windows), 1)
        self.app.windows += test_window
        self.assertEqual(len(self.app.windows), 1)
        self.assertIs(test_window.app, self.app)

        not_a_window = 'not_a_window'
        with self.assertRaises(TypeError):
            self.app.windows += not_a_window

    def test_remove_window(self):
        test_window = toga.Window(factory=toga_dummy.factory)
        self.app.windows += test_window
        self.assertEqual(len(self.app.windows), 1)
        self.app.windows -= test_window
        self.assertEqual(len(self.app.windows), 0)

        not_a_window = 'not_a_window'
        with self.assertRaises(TypeError):
            self.app.windows -= not_a_window

        test_window_not_in_app = toga.Window(factory=toga_dummy.factory)
        with self.assertRaises(AttributeError):
            self.app.windows -= test_window_not_in_app

    def test_app_contains_window(self):
        test_window = toga.Window(factory=toga_dummy.factory)
        self.assertFalse(test_window in self.app.windows)
        self.app.windows += test_window
        self.assertTrue(test_window in self.app.windows)

    def test_window_iteration(self):
        test_windows = [
            toga.Window(id=1, factory=toga_dummy.factory),
            toga.Window(id=2, factory=toga_dummy.factory),
            toga.Window(id=3, factory=toga_dummy.factory),
        ]
        for window in test_windows:
            self.app.windows += window
        self.assertEqual(len(self.app.windows), 3)

        for window in self.app.windows:
            self.assertIn(window, test_windows)

    def test_add_background_task(self):

        async def handler(sender):
            pass

        self.app.add_background_task(handler)
        self.assertActionPerformed(self.app, 'add_background_task')


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
