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
    write_error = None

    def create(self):
        self.main_window = toga.DocumentMainWindow(self)
        self._mock_read = Mock()
        self._mock_write = Mock()

    def read(self):
        if self.read_error:
            # If the object has a "read_error" attribute, raise that exception
            raise self.read_error
        else:
            # We don't actually care about the file or it's contents, but it needs to exist;
            # so we open it to verify that behavior.
            with self.path.open():
                self._mock_read(self.path)

    def write(self):
        # We don't actually care about the file or it's contents.
        self._mock_write(self.path)


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


def test_create_no_cmdline_no_document_types(monkeypatch):
    """A app without document types and no windows raises an error."""
    monkeypatch.setattr(sys, "argv", ["app-exe"])

    with pytest.raises(
        ValueError,
        match=(
            r"App doesn't define any initial windows, doesn't override new, "
            r"and doesn't have a default document type."
        ),
    ):
        ExampleDocumentApp(
            "Test App",
            "org.beeware.document-app",
        )


def test_create_no_cmdline(monkeypatch):
    """A document app can be created with no command line."""
    monkeypatch.setattr(sys, "argv", ["app-exe"])

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )

    # An untitled document has been created
    assert len(app.documents) == 1
    assert isinstance(app.documents[0], ExampleDocument)
    assert app.documents[0].title == "Example Document: Untitled"

    # Document window has been created and shown
    assert len(app.windows) == 1
    assert list(app.windows)[0] == app.documents[0].main_window
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")


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
    assert app.documents[0].title == "Example Document: filename"

    # Document content has been read
    app.documents[0]._mock_read.assert_called_once_with(example_file)

    # Document window has been created and shown
    assert len(app.windows) == 1
    assert list(app.windows)[0] == app.documents[0].main_window
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")


def test_create_with_unknown_document_type(monkeypatch, capsys):
    """If the document specified at the command line is an unknown type, it is ignored."""
    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/filename.unknown"])

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )

    stdout = capsys.readouterr().out
    assert "Don't know how to open documents with extension .unknown" in stdout

    # An untitled document has been created
    assert len(app.documents) == 1
    assert isinstance(app.documents[0], ExampleDocument)
    assert app.documents[0].title == "Example Document: Untitled"

    # Document window has been created and shown
    assert len(app.windows) == 1
    assert list(app.windows)[0] == app.documents[0].main_window
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")


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

    # An untitled document has been created
    assert len(app.documents) == 1
    assert isinstance(app.documents[0], ExampleDocument)
    assert app.documents[0].title == "Example Document: Untitled"

    # Document window has been created and shown
    assert len(app.windows) == 1
    assert list(app.windows)[0] == app.documents[0].main_window
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")


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

    # An untitled document has been created
    assert len(app.documents) == 1
    assert isinstance(app.documents[0], ExampleDocument)
    assert app.documents[0].title == "Example Document: Untitled"

    # Document window has been created and shown
    assert len(app.windows) == 1
    assert list(app.windows)[0] == app.documents[0].main_window
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")


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

    # Close the first document window (in a running app loop)
    async def close_window(app):
        list(app.windows)[0].close()

    app.loop.run_until_complete(close_window(app))

    # One document window closed.
    assert len(app.documents) == 1
    assert len(app.windows) == 1

    # App hasn't exited
    assert_action_not_performed(app, "exit")

    # Close the first document window (in a running app loop)
    app.loop.run_until_complete(close_window(app))

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

    # Close the first document window (in a running app loop)
    async def close_window(app):
        list(app.windows)[0].close()

    app.loop.run_until_complete(close_window(app))

    # One document window closed.
    assert len(app.documents) == 1
    assert len(app.windows) == 1

    # App hasn't exited
    assert_action_not_performed(app, "exit")

    # Close the last remaining document window
    app.loop.run_until_complete(close_window(app))

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


def test_new_menu(doc_app):
    """The new method is activated by the new menu."""
    doc_app.commands[toga.Command.NEW.format("foobar")].action()

    # There are now 2 documents, and 2 windows
    assert len(doc_app.documents) == 2
    assert len(doc_app.windows) == 2

    # The second document is the one we just loaded
    new_doc = doc_app.documents[1]
    assert new_doc.path is None
    assert new_doc.title == "Example Document: Untitled"
    assert new_doc.main_window.doc == new_doc
    assert new_doc.main_window in doc_app.windows


def test_open_menu(doc_app, example_file):
    """The open method is activated by the open menu."""
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
    """If the open method is activated by the open menu."""
    # Mock a pre-existing open dialog
    doc_app._open_dialog = Mock()

    # Activate the open dialog a second time.
    future = doc_app.commands[toga.Command.OPEN].action()

    doc_app.loop.run_until_complete(future)

    # There is still only one document
    assert len(doc_app.documents) == 1
    assert len(doc_app.windows) == 1


def test_save_menu(doc_app, example_file):
    """The save method is activated by the save menu."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document
    second_doc = doc_app.new(ExampleDocument)

    # Activate the save menu
    future = doc_app.commands[toga.Command.SAVE].action()
    doc_app.loop.run_until_complete(future)

    # The first document is the one we saved
    first_doc._mock_write.assert_called_once_with(example_file)
    second_doc._mock_write.assert_not_called()


def test_save_menu_readonly(doc_app, example_file, other_file, tmp_path):
    """The save method is a no-op on readonly files."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a readonly document, set to be current
    second_doc = doc_app.open(other_file)
    doc_app.current_window = second_doc.main_window

    # Activate the save menu
    future = doc_app.commands[toga.Command.SAVE].action()
    doc_app.loop.run_until_complete(future)

    # Second document hasn't changed properties updated
    assert second_doc.path == other_file
    assert second_doc.title == "Other Document: other"


def test_save_menu_untitled(doc_app, example_file, tmp_path):
    """The save method can can be activated on an untitled file."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document, set to be current
    second_doc = doc_app.new(ExampleDocument)
    doc_app.current_window = second_doc.main_window

    # Prime the save dialog on the second window
    path = tmp_path / "path/to/filename2.foobar"
    second_doc.main_window._impl.dialog_responses["SaveFileDialog"] = [path]

    # Activate the save menu
    future = doc_app.commands[toga.Command.SAVE].action()
    doc_app.loop.run_until_complete(future)

    # The second document is the one we saved
    first_doc._mock_write.assert_not_called()
    second_doc._mock_write.assert_called_once_with(path)

    # Second document has had properties updated
    assert second_doc.path == path
    assert second_doc.title == "Example Document: filename2"


def test_save_menu_untitled_cancel(doc_app, example_file, tmp_path):
    """Saving an untitled file can be cancelled."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document, set to be current
    second_doc = doc_app.new(ExampleDocument)
    doc_app.current_window = second_doc.main_window

    # Prime the save dialog on the second window
    second_doc.main_window._impl.dialog_responses["SaveFileDialog"] = [None]

    # Activate the save menu
    future = doc_app.commands[toga.Command.SAVE].action()
    doc_app.loop.run_until_complete(future)

    # Neither document is saved.
    first_doc._mock_write.assert_not_called()
    second_doc._mock_write.assert_not_called()


def test_save_menu_untitled_overwrite(doc_app, example_file, tmp_path):
    """An untitled file can overwrite an existing file."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document, set to be current
    second_doc = doc_app.new(ExampleDocument)
    doc_app.current_window = second_doc.main_window

    # Prime the save dialog on the second window to save using the existing filename,
    # and accept the overwrite.
    second_doc.main_window._impl.dialog_responses["SaveFileDialog"] = [example_file]
    second_doc.main_window._impl.dialog_responses["ConfirmDialog"] = [True]

    # Activate the save menu
    future = doc_app.commands[toga.Command.SAVE].action()
    doc_app.loop.run_until_complete(future)

    # Neither document is saved.
    first_doc._mock_write.assert_not_called()
    second_doc._mock_write.assert_called_once_with(example_file)

    # Second document has had properties updated
    assert second_doc.path == example_file
    assert second_doc.title == "Example Document: filename"


def test_save_menu_untitled_overwrite_reconsidered(doc_app, example_file, tmp_path):
    """An untitled file attempting to overwrite an existing file will be warned, but the
    decision can be walked back."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document, set to be current
    second_doc = doc_app.new(ExampleDocument)
    doc_app.current_window = second_doc.main_window

    # Prime the save dialog on the second window to save using the existing filename,
    # and reject the overwrite, then pick a unique filename
    path = tmp_path / "path/to/filename2.foobar"
    second_doc.main_window._impl.dialog_responses["SaveFileDialog"] = [
        example_file,
        path,
    ]
    second_doc.main_window._impl.dialog_responses["ConfirmDialog"] = [False]

    # Activate the save menu
    future = doc_app.commands[toga.Command.SAVE].action()
    doc_app.loop.run_until_complete(future)

    # Neither document is saved.
    first_doc._mock_write.assert_not_called()
    second_doc._mock_write.assert_called_once_with(path)

    # Second document has had properties updated
    assert second_doc.path == path
    assert second_doc.title == "Example Document: filename2"


def test_save_menu_non_document(doc_app, example_file):
    """On a non-document window, save is ignored."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document
    second_doc = doc_app.new(ExampleDocument)

    # Open a non-document window, and make it current
    third_window = toga.Window(title="Not a document")
    doc_app.current_window = third_window

    # Activate the save menu
    future = doc_app.commands[toga.Command.SAVE].action()
    doc_app.loop.run_until_complete(future)

    # No document is saved; the current window isn't a document.
    first_doc._mock_write.assert_not_called()
    second_doc._mock_write.assert_not_called()


def test_save_as_menu(doc_app, example_file, tmp_path):
    """The save as method is activated by the save as menu."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document
    second_doc = doc_app.new(ExampleDocument)

    # Prime the save dialog on the first window
    path = tmp_path / "path/to/filename2.foobar"
    first_doc.main_window._impl.dialog_responses["SaveFileDialog"] = [path]

    # Activate the Save As menu
    future = doc_app.commands[toga.Command.SAVE_AS].action()
    doc_app.loop.run_until_complete(future)

    # The first document is the one we saved
    first_doc._mock_write.assert_called_once_with(path)
    second_doc._mock_write.assert_not_called()

    # First document has had properties updated
    assert first_doc.path == path
    assert first_doc.title == "Example Document: filename2"


def test_save_as_menu_readonly(doc_app, example_file, other_file, tmp_path):
    """The save-as method is a no-op on readonly files."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a readonly document, set to be current
    second_doc = doc_app.open(other_file)
    doc_app.current_window = second_doc.main_window

    # Activate the Save As menu
    future = doc_app.commands[toga.Command.SAVE_AS].action()
    doc_app.loop.run_until_complete(future)

    # Second document hasn't changed properties updated
    assert second_doc.path == other_file
    assert second_doc.title == "Other Document: other"


def test_save_as_menu_untitled(doc_app, example_file, tmp_path):
    """The save as method can can be activated on an untitled file."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document, set to be current
    second_doc = doc_app.new(ExampleDocument)
    doc_app.current_window = second_doc.main_window

    # Prime the save dialog on the second window
    path = tmp_path / "path/to/filename2.foobar"
    second_doc.main_window._impl.dialog_responses["SaveFileDialog"] = [path]

    # Activate the Save As menu
    future = doc_app.commands[toga.Command.SAVE_AS].action()
    doc_app.loop.run_until_complete(future)

    # The second document is the one we saved
    first_doc._mock_write.assert_not_called()
    second_doc._mock_write.assert_called_once_with(path)

    # Second document has had properties updated
    assert second_doc.path == path
    assert second_doc.title == "Example Document: filename2"


def test_save_as_menu_cancel(doc_app, example_file, tmp_path):
    """A save as request can be cancelled by the user."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document
    second_doc = doc_app.new(ExampleDocument)

    # Cancel the request to save
    first_doc.main_window._impl.dialog_responses["SaveFileDialog"] = [None]

    # Activate the Save As menu
    future = doc_app.commands[toga.Command.SAVE_AS].action()
    doc_app.loop.run_until_complete(future)

    # Neither document is saved.
    first_doc._mock_write.assert_not_called()
    second_doc._mock_write.assert_not_called()


def test_save_as_menu_non_document(doc_app, example_file):
    """On a non-document window, save as is ignored."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document
    second_doc = doc_app.new(ExampleDocument)

    # Open a non-document window, and make it current
    third_window = toga.Window(title="Not a document")
    doc_app.current_window = third_window

    # Activate the Save As menu
    future = doc_app.commands[toga.Command.SAVE_AS].action()
    doc_app.loop.run_until_complete(future)

    # No document is saved; the current window isn't a document.
    first_doc._mock_write.assert_not_called()
    second_doc._mock_write.assert_not_called()


def test_save_all_menu(doc_app, example_file, tmp_path):
    """The save all method is activated by the save all menu."""
    current_window = doc_app.current_window
    first_doc = current_window.doc
    assert first_doc.path == example_file

    # Open a second new document
    second_doc = doc_app.new(ExampleDocument)

    # Open a third window, with no document attached
    third_window = toga.Window(title="Not a document")
    third_window.show()

    # Prime the save dialog on the second window
    path = tmp_path / "path/to/filename2.foobar"
    second_doc.main_window._impl.dialog_responses["SaveFileDialog"] = [path]

    # Activate the Save All menu
    future = doc_app.commands[toga.Command.SAVE_ALL].action()
    doc_app.loop.run_until_complete(future)

    # Both documents have been saved
    first_doc._mock_write.assert_called_once_with(example_file)
    second_doc._mock_write.assert_called_once_with(path)

    # Second document has had properties updated
    assert second_doc.path == path
    assert second_doc.title == "Example Document: filename2"


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
