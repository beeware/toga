import os
from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import assert_action_performed_with


class MyDoc(toga.Document):
    description = "My Document"
    extensions = ["doc"]

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
    description = "Other Document"
    extensions = ["other"]

    def create(self):
        self.main_window = Mock(title="Mock Window")

    def read(self):
        pass


def test_create_document(app):
    doc = MyDoc(app)

    assert doc.path is None
    assert doc.app == app
    assert doc.description == "My Document"
    assert doc.title == "My Document: Untitled"

    # create() has been invoked
    assert doc.content is None
    assert doc.main_window.title == "Mock Window"

    # Document can be shown
    doc.show()
    doc.main_window.show.assert_called_once_with()

    # Document can be hidden
    doc.hide()
    doc.main_window.hide.assert_called_once_with()


def test_no_description(event_loop):
    """If a document class doesn't define a description, an error is raised."""

    class BadDoc(toga.Document):
        def create(self):
            self.main_window = Mock(title="Mock Window")

        def read(self):
            pass

    with pytest.raises(
        ValueError,
        match=r"Document type 'BadDoc' doesn't define a 'descriptions' attribute",
    ):
        toga.App(
            "Test App",
            "org.beeware.document-app",
            document_types=[MyDoc, BadDoc],
        )


def test_no_extensions(event_loop):
    """If a document class doesn't define extensions, an error is raised."""

    class BadDoc(toga.Document):
        description = "Bad Document"

        def create(self):
            self.main_window = Mock(title="Mock Window")

        def read(self):
            pass

    with pytest.raises(
        ValueError,
        match=r"Document type 'BadDoc' doesn't define an 'extensions' attribute",
    ):
        toga.App(
            "Test App",
            "org.beeware.document-app",
            document_types=[MyDoc, BadDoc],
        )


def test_empty_extensions(event_loop):
    """If a document class doesn't define extensions, an error is raised."""

    class BadDoc(toga.Document):
        description = "Bad Document"
        extensions = []

        def create(self):
            self.main_window = Mock(title="Mock Window")

        def read(self):
            pass

    with pytest.raises(
        ValueError,
        match=r"Document type 'BadDoc' doesn't define at least one extension",
    ):
        toga.App(
            "Test App",
            "org.beeware.document-app",
            document_types=[MyDoc, BadDoc],
        )


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
    assert not doc.modified


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
        assert not doc.modified
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

    # Touch the document to mark it as modified
    doc.touch()
    assert doc.modified

    # Read the file
    doc.save(converter(path))

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == path.absolute()
    assert doc.title == "My Document: doc"
    assert doc._mock_content.write(path.absolute())
    # Saving clears the modification flag
    assert not doc.modified


@pytest.mark.parametrize("converter", [str, lambda s: s])
def test_save_relative_document(app, converter, tmp_path):
    """A document can be saved with a relative path."""
    doc = MyDoc(app)

    path = Path("doc.mydoc")

    # Touch the document to mark it as modified
    doc.touch()
    assert doc.modified

    # Read the file
    doc.save(converter(path))

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == (Path.cwd() / path).absolute()
    assert doc.title == "My Document: doc"
    assert doc._mock_content.write(path.absolute())
    # Saving clears the modification flag
    assert not doc.modified


def test_save_existing_document(app, tmp_path):
    """A document can be saved at its existing path."""
    doc = MyDoc(app)
    path = tmp_path / "doc.mydoc"
    # Prime the document's path
    doc._path = path

    # Touch the document to mark it as modified
    doc.touch()
    assert doc.modified

    # Save the file
    doc.save()

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == path.absolute()
    assert doc.title == "My Document: doc"
    assert doc._mock_content.write(path.absolute())
    # Saving clears the modification flag
    assert not doc.modified


def test_save_readonly_document(app, tmp_path):
    """Save is a no-op on a readonly document."""
    doc = OtherDoc(app)
    path = tmp_path / "doc.other"
    # Prime the document's path
    doc._path = path

    # Touch the document to mark it as modified. This isn't a likely setup for a
    # readonly document, but it's possible.
    doc.touch()
    assert doc.modified

    # Save the file
    doc.save()

    # Calling absolute() ensures the expected value is correct on Windows
    assert doc.path == path.absolute()
    assert doc.title == "Other Document: doc"
    # There's no write method, so modifications can't be committed.
    assert doc.modified


def test_focus(app):
    """A document can be given focus."""
    doc1 = MyDoc(app)

    # Give the document focus.
    doc1.focus()

    # The app's current window has been set.
    assert_action_performed_with(app, "set_current_window", window=doc1.main_window)
