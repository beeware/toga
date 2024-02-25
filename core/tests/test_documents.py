from pathlib import Path
from unittest.mock import Mock

import pytest

import toga


class MyDoc(toga.Document):
    document_type = "My Document"
    default_extension = ".mydoc"

    def create(self):
        self.main_window = Mock(title="Mock Window")
        self.content = None
        self.written = None

    def read(self):
        self.content = "file content"

    def write(self):
        self.written = self.content


def test_create_document(app):
    doc = MyDoc(app)

    assert doc.path is None
    assert doc.app == app
    assert doc.document_type == "My Document"
    assert doc.default_extension == ".mydoc"
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


@pytest.mark.parametrize(
    "path,expected",
    [
        (None, Path("/path/to/doc.mydoc")),
        ("/path/to/newdoc.mydoc", Path("/path/to/newdoc.mydoc")),
        (Path("/path/to/newdoc.mydoc"), Path("/path/to/newdoc.mydoc")),
        ("newdoc.mydoc", Path.cwd() / "newdoc.mydoc"),
        (Path("newdoc.mydoc"), Path.cwd() / "newdoc.mydoc"),
    ],
)
def test_save_document(app, path, expected):
    """A document can be saved"""
    doc = MyDoc(app)
    doc.open("/path/to/doc.mydoc")

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == Path("/path/to/doc.mydoc").absolute()

    doc.save(path)
    assert doc.path == expected.absolute()
    assert doc.written == "file content"
