import toga
import toga_dummy
from toga_dummy.utils import TestCase


class DocumentTests(TestCase):
    def setUp(self):
        super().setUp()

        self.filename = 'path/to/document.txt'
        self.document_type = 'path/to/document.txt'
        self.document = toga.Document(filename=self.filename,
                                      document_type=self.document_type,
                                      app=toga_dummy)

    def test_app(self):
        self.assertEqual(self.filename, self.document.filename)

    def test_read(self):
        with self.assertRaises(NotImplementedError):
            self.document.read()
