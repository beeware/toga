import os
from pathlib import Path
from unittest.mock import Mock

import pytest

import toga


class MyDoc(toga.Document):
    document_type = "My Document"

    def create(self):
        self.main_window = Mock(title="Mock Window")
        self.content = None
        self._mock_content = Mock()

    def read(self):
        self.content = "file content"
        self._mock_content.read(self.path)


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


@pytest.mark.parametrize("converter", [str, lambda s: s])
def test_open_absolute_document(app, converter, tmp_path):
    """A document can be opened with an absolute path."""
    doc = MyDoc(app)

    path = tmp_path / "doc.mydoc"
    path.write_text("sample file")

    # Read the file
    doc.open(converter(path))

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == path.absolute()
    assert doc.content == "file content"


@pytest.mark.parametrize("converter", [str, lambda s: s])
def test_open_relative_document(app, converter, tmp_path):
    """A document can be opened with a relative path."""
    doc = MyDoc(app)

    orig_cwd = Path.cwd()
    try:
        (tmp_path / "cwd").mkdir()
        os.chdir(tmp_path / "cwd")

        path = tmp_path / "cwd/doc.mydoc"
        path.write_text("sample file")

        # Read the file
        doc.open(converter(path))

        # Calling absolute() ensures the expected value is correct on Windows
        assert doc.path == path.absolute()
        assert doc.content == "file content"
    finally:
        os.chdir(orig_cwd)


def test_open_missing_document(app, tmp_path):
    """A missing document raises an error."""
    doc = MyDoc(app)

    # Read the file
    with pytest.raises(FileNotFoundError):
        doc.open(tmp_path / "doc.mydoc")
