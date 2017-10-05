import unittest
from unittest.mock import Mock, MagicMock, patch
import toga
import toga_dummy


class TestApp(unittest.TestCase):
    def setUp(self):
        # mock factory to return a mock app
        self.factory = MagicMock()

        self.mock_app = MagicMock(spec=toga_dummy.factory.App)
        self.mock_window = MagicMock(spec=toga_dummy.factory.App)
        self.mock_icon = MagicMock(spec=toga_dummy.factory.Icon)

        self.factory.App = MagicMock(return_value=self.mock_app)
        self.factory.Window = MagicMock(return_value=self.mock_window)
        self.factory.Icon = MagicMock(return_value=self.mock_icon)

        self.content = MagicMock()

        self.name = 'Test App'
        self.app_id = 'beeware.org'
        self.id = 'id'

        self.started = False
        def test_startup_function(app):
            self.started = True
            return self.content

        self.app = toga.App(self.name,
                            self.app_id,
                            startup=test_startup_function,
                            factory=self.factory,
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

    def test_app_factory_called(self):
        self.factory.App.assert_called_once_with(interface=self.app)

    @patch('toga.app.get_platform_factory')
    def test_app_init_with_no_factory(self, mock_function):
        app = toga.App(self.name, self.app_id)
        mock_function.assert_called_once_with(None)

    def test_app_open_docuemnts_raise_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.app.open_document('file/url')

    def test_app_main_loop_call_impl_main_loop(self):
        self.app.main_loop()
        self.mock_app.main_loop.assert_called_once_with()

    @patch('toga.window.Window.show')
    def test_app_startup(self, window_show):
        window_show = Mock()

        self.app.startup()

        self.assertTrue(self.started)
        self.assertEqual(self.app.main_window.content, self.content)
        self.assertEqual(self.app.main_window.app, self.app)
        self.app.main_window.show.assert_called_once_with()

    def test_app_exit(self):
        self.app.exit()

        self.app._impl.exit.assert_called_once_with()
