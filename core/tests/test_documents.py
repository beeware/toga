from pathlib import Path
from unittest.mock import Mock

import pytest

import toga


class MyDoc(toga.Document):
    document_type = "My Document"

    def create(self):
        self.main_window = Mock(title="Mock Window")
        self.content = None

    def read(self):
        self.content = "file content"


def test_create_document(app):
    doc = MyDoc(app)

    assert doc.path is None
    assert doc.app == app
    assert doc.document_type == "My Document"
    assert doc.title == "My Document: Untitled"

    # create() has been invoked
    assert doc.content is None
    assert doc.main_window.title == "Mock Window"

    # Document can be shown
    doc.show()
    doc.main_window.show.assert_called_once_with()


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/path/to/doc.mydoc", Path("/path/to/doc.mydoc")),
        (Path("/path/to/doc.mydoc"), Path("/path/to/doc.mydoc")),
        ("doc.mydoc", Path.cwd() / "doc.mydoc"),
        (Path("doc.mydoc"), Path.cwd() / "doc.mydoc"),
    ],
)
def test_open_document(app, path, expected):
    """A document can be opened"""
    doc = MyDoc(app)

    doc.open(path)

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == expected.absolute()
    assert doc.content == "file content"
