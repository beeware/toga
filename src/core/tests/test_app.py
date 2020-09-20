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

        self.app = self.create_app()

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

    def test_default_commands(self):
        self.assertValueSet(self.app, "about command", "about")
        self.assertValueSet(self.app, "preferences command", "preferences")
        self.assertValueSet(self.app, "homepage command", "homepage")
        self.assertValueSet(self.app, "quit command", "quit")

    def test_no_about_command(self):
        app = self.create_app(about_command=False)
        self.assertNoValueSet(app, "about command")

    def test_no_preferences_command(self):
        app = self.create_app(preferences_command=False)
        self.assertNoValueSet(app, "preferences command")

    def test_no_home_page_command(self):
        app = self.create_app(home_page_command=False)
        self.assertNoValueSet(app, "homepage command")

    def test_no_quit_command(self):
        app = self.create_app(quit_command=False)
        self.assertNoValueSet(app, "quit command")

    def create_app(self, **kwargs):
        def test_startup_function(app):
            self.started = True
            return self.content

        return toga.App(
            factory=toga_dummy.factory,
            formal_name=self.name,
            id=self.id,
            app_id=self.app_id,
            startup=test_startup_function,
            **kwargs,
        )


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
