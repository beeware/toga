import sys
from unittest.mock import Mock

import pytest

import toga
from toga_dummy.app import App as DummyApp
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
)


class ExampleDocument(toga.Document):
    document_type = "Example Document"
    read_error = None

    def create(self):
        self.main_window = toga.DocumentMainWindow(self)
        self._mock_read = Mock(self.path)

    def read(self):
        if self.read_error:
            # If the object has a "read_error" attribute, raise that exception
            raise self.read_error
        else:
            # We don't actually care about the file or it's contents, but it needs to exist;
            # so we open it to verify that behavior.
            with self.path.open():
                self._mock_read(self.path)


class OtherDocument(toga.Document):
    document_type = "Other Document"

    def create(self):
        self.main_window = toga.DocumentMainWindow(self)

    def read(self):
        pass


@pytest.fixture
def example_file(tmp_path):
    """Create an actual file with the .foobar extension"""
    path = tmp_path / "path/to/filename.foobar"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        f.write("Dummy content")

    return path


@pytest.fixture
def other_file(tmp_path):
    """Create an actual file with the .other extension"""
    path = tmp_path / "path/to/other.other"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        f.write("Dummy content")

    return path


class ExampleDocumentApp(toga.App):
    def startup(self):
        self.main_window = None


@pytest.fixture
def doc_app(monkeypatch, event_loop, example_file):
    # Create an instance of an ExampleDocumentApp that has 1 file open.
    monkeypatch.setattr(sys, "argv", ["app-exe", str(example_file)])
    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={
            # Register ExampleDocument with 2 extensions
            "foobar": ExampleDocument,
            "fbr": ExampleDocument,
            # Register a second document type
            "other": OtherDocument,
        },
    )
    # The app will have a single window; set this window as the current window
    # so that dialogs have something to hang off.
    app.current_window = list(app.windows)[0]
    return app


def test_create_no_cmdline(monkeypatch):
    """A document app can be created with no command line."""
    monkeypatch.setattr(sys, "argv", ["app-exe"])

    with pytest.raises(
        ValueError,
        match=r"App doesn't define any initial windows.",
    ):
        ExampleDocumentApp(
            "Test App",
            "org.beeware.document-app",
            document_types={"foobar": ExampleDocument},
        )


def test_create_no_cmdline_default_handling(monkeypatch):
    """If the backend uses the app's command line handling, no error is raised for an
    empty command line."""
    monkeypatch.setattr(sys, "argv", ["app-exe"])

    # Monkeypatch the property that makes the backend handle command lines
    monkeypatch.setattr(DummyApp, "HANDLES_COMMAND_LINE", True)

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )

    assert app._impl.interface == app
    assert_action_performed(app, "create App")

    assert app.document_types == {"foobar": ExampleDocument}

    # No documents or windows exist
    assert len(app.documents) == 0
    assert len(app.windows) == 0


def test_create_with_cmdline(monkeypatch, example_file):
    """If a document is specified at the command line, it is opened."""
    monkeypatch.setattr(sys, "argv", ["app-exe", str(example_file)])

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )

    assert app._impl.interface == app
    assert_action_performed(app, "create App")

    assert app.document_types == {"foobar": ExampleDocument}

    # The document is registered
    assert len(app.documents) == 1
    assert isinstance(app.documents[0], ExampleDocument)

    # Document content has been read
    app.documents[0]._mock_read.assert_called_once_with(example_file)

    # Document window has been created and shown
    assert len(app.windows) == 1
    assert list(app.windows)[0] == app.documents[0].main_window
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")


def test_create_with_unknown_document_type(monkeypatch, capsys):
    """If the document specified at the command line is an unknown type, an exception is
    raised."""
    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/filename.unknown"])

    with pytest.raises(
        ValueError,
        match=r"App doesn't define any initial windows",
    ):
        ExampleDocumentApp(
            "Test App",
            "org.beeware.document-app",
            document_types={"foobar": ExampleDocument},
        )

    stdout = capsys.readouterr().out
    assert "Don't know how to open documents with extension .unknown" in stdout


def test_create_with_missing_file(monkeypatch, capsys):
    """If the document specified at the command line is a known type, but not present,
    an error is logged."""
    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/filename.foobar"])

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )

    stdout = capsys.readouterr().out
    assert "Document /path/to/filename.foobar not found" in stdout

    # No documents exist
    assert len(app.documents) == 0
    # There is 1 window... but it's not visible, and a request to exit has been issued
    # because it's would be the last (and only) window.
    assert len(app.windows) == 1
    assert not list(app.windows)[0].visible
    assert_action_performed(app, "exit")


def test_create_with_bad_file(monkeypatch, example_file, capsys):
    """If an error occurs reading the document, an error is logged is raised."""
    monkeypatch.setattr(sys, "argv", ["app-exe", str(example_file)])
    # Mock a reading error.
    monkeypatch.setattr(
        ExampleDocument, "read_error", ValueError("Bad file. No cookie.")
    )

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )

    stdout = capsys.readouterr().out
    assert "filename.foobar: Bad file. No cookie.\n" in stdout

    # No documents exist
    assert len(app.documents) == 0
    # There is 1 window... but it's not visible, and a request to exit has been issued
    # because it's would be the last (and only) window.
    assert len(app.windows) == 1
    assert not list(app.windows)[0].visible
    assert_action_performed(app, "exit")


def test_close_last_document_non_persistent(monkeypatch, example_file, other_file):
    """Non-persistent apps exit when the last document is closed"""
    monkeypatch.setattr(sys, "argv", ["app-exe", str(example_file)])

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={
            "foobar": ExampleDocument,
            "other": OtherDocument,
        },
    )

    # Create a second document window
    app.open(other_file)

    # There are 2 open documents
    assert len(app.documents) == 2
    assert len(app.windows) == 2

    # Close the first document window
    list(app.windows)[0].close()

    # One document window closed.
    assert len(app.documents) == 1
    assert len(app.windows) == 1

    # App hasn't exited
    assert_action_not_performed(app, "exit")

    # Close the last remaining document window
    list(app.windows)[0].close()

    # App has now exited
    assert_action_performed(app, "exit")


def test_close_last_document_persistent(monkeypatch, example_file, other_file):
    """Persistent apps don't exit when the last document is closed"""
    # Monkeypatch the property that makes the backend persistent
    monkeypatch.setattr(DummyApp, "CLOSE_ON_LAST_WINDOW", False)

    monkeypatch.setattr(sys, "argv", ["app-exe", str(example_file)])

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={
            "foobar": ExampleDocument,
            "other": OtherDocument,
        },
    )

    # Create a second document window
    app.open(other_file)

    # There are 2 open documents
    assert len(app.documents) == 2
    assert len(app.windows) == 2

    # Close the first document window
    list(app.windows)[0].close()

    # One document window closed.
    assert len(app.documents) == 1
    assert len(app.windows) == 1

    # App hasn't exited
    assert_action_not_performed(app, "exit")

    # Close the last remaining document window
    list(app.windows)[0].close()

    # No document windows.
    assert len(app.documents) == 0
    assert len(app.windows) == 0

    # App still hasn't exited
    assert_action_not_performed(app, "exit")


def test_open_missing_file(doc_app):
    """Attempting to read a missing file of a known type raises an error."""
    with pytest.raises(FileNotFoundError):
        doc_app.open("/does/not/exist.foobar")

    # Only the original document and window exists
    assert len(doc_app.documents) == 1
    assert len(doc_app.windows) == 1


def test_open_bad_file(monkeypatch, doc_app, example_file):
    """If an error occurs reading the document, an error is logged is raised."""
    # Mock a reading error.
    monkeypatch.setattr(
        ExampleDocument, "read_error", ValueError("Bad file. No cookie.")
    )

    with pytest.raises(ValueError, match=r"Bad file. No cookie."):
        doc_app.open(example_file)

    # Only the original document and window exists
    assert len(doc_app.documents) == 1
    assert len(doc_app.windows) == 1


def test_open_menu(doc_app, example_file):
    """The open method is activated by the open menu"""
    doc_app._impl.dialog_responses["OpenFileDialog"] = [example_file]

    future = doc_app.commands[toga.Command.OPEN].action()
    doc_app.loop.run_until_complete(future)

    # There are now 2 documents, and 2 windows
    assert len(doc_app.documents) == 2
    assert len(doc_app.windows) == 2

    # The second document is the one we just loaded
    new_doc = doc_app.documents[1]
    assert new_doc.path == example_file
    assert new_doc.main_window.doc == new_doc
    assert new_doc.main_window in doc_app.windows


def test_open_menu_cancel(doc_app):
    """The open menu action can be cancelled by not selecting a file."""
    doc_app._impl.dialog_responses["OpenFileDialog"] = [None]

    future = doc_app.commands[toga.Command.OPEN].action()
    doc_app.loop.run_until_complete(future)

    # No second window was opened
    assert len(doc_app.documents) == 1
    assert len(doc_app.windows) == 1


def test_open_menu_duplicate(doc_app, example_file):
    """If the open method is activated by the open menu"""
    # Mock a pre-existing open dialog
    doc_app._open_dialog = Mock()

    # Activate the open dialog a second time.
    future = doc_app.commands[toga.Command.OPEN].action()

    doc_app.loop.run_until_complete(future)

    # There is still only one document
    assert len(doc_app.documents) == 1
    assert len(doc_app.windows) == 1


def test_deprecated_document_app(monkeypatch, event_loop, example_file):
    """The deprecated API for creating Document-based apps still works."""

    class DeprecatedDocumentApp(toga.DocumentApp):
        def startup(self):
            self.main_window = None

    monkeypatch.setattr(sys, "argv", ["app-exe", str(example_file)])

    with pytest.warns(
        DeprecationWarning,
        match=r"toga.DocumentApp is no longer required. Use toga.App instead",
    ):
        app = DeprecatedDocumentApp(
            "Deprecated App",
            "org.beeware.deprecated-app",
            document_types={"foobar": ExampleDocument},
        )

    # The app has an open document
    assert len(app.documents) == 1
    assert isinstance(app.documents[0], ExampleDocument)
