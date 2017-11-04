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

    def test_app_name(self):
        self.assertEqual(self.app.name, self.name)

    def test_app_icon(self):
        # App icon will be the default icon if you don't specify one
        self.assertEqual(self.app.icon, self.app.default_icon)

        # Set the icon to a different resource
        self.app.icon = "other"
        self.assertEqual(self.app.icon.path, "other.icns")

    def test_app_app_id(self):
        self.assertEqual(self.app.app_id, self.app_id)

    def test_app_id(self):
        self.assertEqual(self.app.id, self.id)

    def test_app_documents(self):
        self.assertEqual(self.app.documents, [])
        doc = MagicMock()
        self.app.add_document(doc)
        self.assertEqual(self.app.documents, [doc])

    @patch('toga.app.get_platform_factory')
    def test_app_init_with_no_factory(self, mock_function):
        app = toga.App(self.name, self.app_id)
        mock_function.assert_called_once_with(None)

    def test_app_open_docuemnts_raise_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.app.open_document('file/url')

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
