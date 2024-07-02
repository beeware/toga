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

    def write(self):
        self._mock_content.write(self.path)


class OtherDoc(toga.Document):
    document_type = "Other Document"

    def create(self):
        self.main_window = Mock(title="Mock Window")

    def read(self):
        pass


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


def test_default_extension(event_loop):
    """The default extension for a document type can be determined."""

    app = toga.App(
        "Test App",
        "org.beeware.document-app",
        document_types={
            "foobar": OtherDoc,
            "doc1": MyDoc,
            "doc2": MyDoc,
        },
    )

    doc = MyDoc(app)

    assert doc.default_extension == "doc1"


def test_default_extension_unregistered(app):
    """The default extension for a document type can be determined."""

    doc = MyDoc(app)

    with pytest.raises(
        RuntimeError,
        match=r"Document type isn't registered with the current app",
    ):
        doc.default_extension


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
    assert doc._mock_content.read(path.absolute())


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
        assert doc._mock_content.read(path.absolute())
    finally:
        os.chdir(orig_cwd)


def test_open_missing_document(app, tmp_path):
    """A missing document raises an error."""
    doc = MyDoc(app)

    # Read the file
    with pytest.raises(FileNotFoundError):
        doc.open(tmp_path / "doc.mydoc")


@pytest.mark.parametrize("converter", [str, lambda s: s])
def test_save_absolute_document(app, converter, tmp_path):
    """A document can be saved with an absolute path."""
    doc = MyDoc(app)

    path = tmp_path / "doc.mydoc"

    # Read the file
    doc.save(converter(path))

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == path.absolute()
    assert doc.title == "My Document: doc"
    assert doc._mock_content.write(path.absolute())


@pytest.mark.parametrize("converter", [str, lambda s: s])
def test_save_relative_document(app, converter, tmp_path):
    """A document can be saved with a relative path."""
    doc = MyDoc(app)

    path = Path("doc.mydoc")

    # Read the file
    doc.save(converter(path))

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == (Path.cwd() / path).absolute()
    assert doc.title == "My Document: doc"
    assert doc._mock_content.write(path.absolute())


def test_save_existing_document(app, tmp_path):
    """A document can be saved at its existing path."""
    doc = MyDoc(app)
    path = tmp_path / "doc.mydoc"
    # Prime the document's path
    doc._path = path

    # Save the file
    doc.save()

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == path.absolute()
    assert doc.title == "My Document: doc"
    assert doc._mock_content.write(path.absolute())


def test_save_readonly_document(app, tmp_path):
    """Save is a no-op on a readonly document."""
    doc = OtherDoc(app)
    path = tmp_path / "doc.other"
    # Prime the document's path
    doc._path = path

    # Save the file
    doc.save()

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == path.absolute()
    assert doc.title == "Other Document: doc"
