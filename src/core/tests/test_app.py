from unittest.mock import patch, MagicMock

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

        # This icon name *will* exist (since it overlaps with the default
        # icon name)
        self.assertIsNotNone(self.app.icon._impl)

        # Set the icon to a different resource
        self.app.icon = "other.icns"
        self.assertEqual(self.app.icon.path, "other.icns")

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
