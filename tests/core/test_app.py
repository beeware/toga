import unittest
from unittest.mock import MagicMock, patch
import toga
import toga_cocoa


class TestCoreApp(unittest.TestCase):
    def setUp(self):
        # mock factory to return a mock button
        self.factory = MagicMock()
        # Fixme | The MagicMock returns a MagicMock with the specs of a cocoa.Button.
        # This makes the test not platform independent. Solution could be a platform independent dummy backend.
        self.mock_app = MagicMock(spec=toga_cocoa.App)
        self.factory.App = MagicMock(return_value=self.mock_app)

        self.name = 'Test App'
        self.app_id = 'beeware.org'
        self.id = 'id'

        def test_startup_function(app):
            return 'return obj'

        self.app = toga.App(self.name,
                            self.app_id,
                            startup=test_startup_function,
                            factory=self.factory,
                            id=self.id)

    def test_app_name(self):
        self.assertEqual(self.app.name, self.name)

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
        self.factory.App.assert_called_once_with(creator=self.app)

    @patch('toga.app.get_platform_factory')
    def test_app_init_with_no_factory(self, mock_function):
        app = toga.App(self.name, self.app_id)
        mock_function.assert_called_once_with()

    def test_app_open_docuemnts_raise_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.app.open_document('file/url')

    def test_app_main_loop_call_impl_main_loop(self):
        self.app.main_loop()
        self.mock_app.main_loop.assert_called_once_with()
