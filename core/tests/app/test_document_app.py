import sys
from pathlib import Path
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
    default_extension = ".foobar"

    def create(self):
        self.main_window = toga.DocumentMainWindow(self)
        self._read = Mock(self.path)
        self._write = Mock(self.path)

    def read(self):
        # We don't actually care about the file or it's contents, but it needs to exist;
        # so we open it to verify that behavior.
        with self.path.open():
            self._read(self.path)

    def write(self):
        # We don't actually care about the file or it's contents, but it needs to be
        # writable, so we open it to verify that behavior.
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w"):
            self._write(self.path)


class OtherDocument(toga.Document):
    document_type = "Other Document"
    default_extension = ".other"

    def create(self):
        self.main_window = toga.DocumentMainWindow(self)

    def read(self):
        pass

    def write(self):
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
def doc_app(event_loop):
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

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )

    assert app._impl.interface == app
    assert_action_performed(app, "create App")

    assert app.document_types == {"foobar": ExampleDocument}

    # With no command line, a default empty document will be created
    assert len(app.documents) == 1
    assert app.documents[0].path is None

    # Document window has been created and shown
    assert len(app.windows) == 1
    assert list(app.windows)[0] == app.documents[0].main_window
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")


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
    app.documents[0]._read.assert_called_once_with(example_file)

    # Document window has been created and shown
    assert len(app.windows) == 1
    assert list(app.windows)[0] == app.documents[0].main_window
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")


def test_create_with_unknown_document_type(monkeypatch, capsys):
    """If the document specified at the command line is an unknown type, an exception is raised"""
    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/filename.unknown"])

    ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )

    stdout = capsys.readouterr().out
    assert "Don't know how to open documents of type .unknown" in stdout


def test_create_with_missing_file(monkeypatch, capsys):
    """If the document specified at the command line is a known type, but not present, an exception is raised"""
    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/filename.foobar"])

    ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )

    stdout = capsys.readouterr().out
    assert "Document /path/to/filename.foobar not found" in stdout


def test_close_last_document_non_persistent(monkeypatch, example_file, other_file):
    """Non-persistent apps exit when the last document is closed"""
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
    app.open(other_file)

    # There are 2 open documents
    assert len(app.documents) == 2
    assert len(app.windows) == 2

    # Close the first document window.
    list(app.windows)[0].on_close()

    # One document window closed.
    assert len(app.documents) == 1
    assert len(app.windows) == 1

    # App hasn't exited
    assert_action_not_performed(app, "exit")

    # Close the last remaining document window.
    list(app.windows)[0].on_close()

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
            # Register ExampleDocument with 2 extensions
            "foobar": ExampleDocument,
            "fbr": ExampleDocument,
            # Register a second document type
            "other": OtherDocument,
        },
    )
    app.open(other_file)

    # There are 2 open documents
    assert len(app.documents) == 2
    assert len(app.windows) == 2

    # Close the first document window.
    list(app.windows)[0].on_close()

    # One document window closed.
    assert len(app.documents) == 1
    assert len(app.windows) == 1

    # App hasn't exited
    assert_action_not_performed(app, "exit")

    # Close the last remaining document window.
    list(app.windows)[0].on_close()

    # No document windows.
    assert len(app.documents) == 0
    assert len(app.windows) == 0

    # App still hasn't exited
    assert_action_not_performed(app, "exit")


def test_new_menu(doc_app):
    """The new menu exists and can create new documents"""
    # Create a document of the default document type
    future = doc_app._impl.new_commands[ExampleDocument].action()
    doc_app.loop.run_until_complete(future)

    # There are now 2 documents, and 2 windows
    assert len(doc_app.documents) == 2
    assert len(doc_app.windows) == 2

    # The newest document is the one we just created
    new_doc = doc_app.documents[-1]
    assert isinstance(new_doc, ExampleDocument)
    assert new_doc.path is None
    assert new_doc.main_window.doc == new_doc
    assert new_doc.main_window in doc_app.windows

    # Create a document of a secondary document type
    future = doc_app._impl.new_commands[OtherDocument].action()
    doc_app.loop.run_until_complete(future)

    # There are now 2 documents, and 2 windows
    assert len(doc_app.documents) == 3
    assert len(doc_app.windows) == 3

    # The newest document is the one we just created
    new_doc = doc_app.documents[-1]
    assert isinstance(new_doc, OtherDocument)
    assert new_doc.path is None
    assert new_doc.main_window.doc == new_doc
    assert new_doc.main_window in doc_app.windows


def test_open_menu(doc_app, example_file):
    """The open method is activated by the open menu"""
    doc_app.current_window._impl.dialog_responses["OpenFileDialog"] = [example_file]

    future = doc_app._impl.open_command.action()
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
    doc_app.current_window._impl.dialog_responses["OpenFileDialog"] = [None]

    future = doc_app._impl.open_command.action()
    doc_app.loop.run_until_complete(future)

    # No second window was opened
    assert len(doc_app.documents) == 1
    assert len(doc_app.windows) == 1


def test_save_menu_existing_document(doc_app, tmp_path):
    """The save method can be triggered by menu on an existing document"""
    # There is one document available; but it doesn't have a filename.
    # Save it, then reset the mock
    assert len(doc_app.documents) == 1
    doc = doc_app.documents[0]
    doc_path = Path(tmp_path / "path/to/first.foobar")
    doc.save(doc_path)
    doc._write.reset_mock()

    # Save the document with the menu
    future = doc_app._impl.save_command.action()
    doc_app.loop.run_until_complete(future)

    # Write was invoked on the document
    doc._write.assert_called_once_with(doc_path)
    assert doc.path == doc_path


def test_save_menu_new_document(doc_app, tmp_path):
    """The save method can be triggered by menu on a new document"""
    # There is one document available; but it doesn't have a filename.
    assert len(doc_app.documents) == 1
    doc = doc_app.documents[0]
    assert doc.path is None

    # Prime the save file dialog with a response
    doc_path = Path(tmp_path / "path/to/first.foobar")
    doc_app.current_window._impl.dialog_responses["SaveFileDialog"] = [doc_path]

    # Save the document with the menu
    future = doc_app._impl.save_command.action()
    doc_app.loop.run_until_complete(future)

    # Write was invoked on the document
    doc._write.assert_called_once_with(doc_path)
    assert doc.path == doc_path


def test_save_menu_new_document_cancel(doc_app, tmp_path):
    """Save on a new file can be cancelled by not selecting a file"""
    # There is one document available; but it doesn't have a filename.
    assert len(doc_app.documents) == 1
    doc = doc_app.documents[0]
    assert doc.path is None

    # Prime the save file dialog with a cancel response
    doc_app.current_window._impl.dialog_responses["SaveFileDialog"] = [None]

    # Save the document with the menu
    future = doc_app._impl.save_command.action()
    doc_app.loop.run_until_complete(future)

    # Write was not invoked on the document
    doc._write.assert_not_called()
    assert doc.path is None


def test_save_non_document(doc_app):
    """If the current window isn't a document, save is a no-op"""
    # There is one document available
    assert len(doc_app.documents) == 1

    # Create a non-document window, and set it as the current window
    window = toga.Window()
    window.content = toga.Box()
    window.show()
    doc_app.current_window = window

    # Invoke save on the non-doc window. This should be a no-op,
    # but there's nothing we can do to verify that it is.
    doc_app.loop.run_until_complete(doc_app.save(window))

    # Mock Save so we can confirm it isn't invoked by the menu
    doc_app.save = Mock()

    # Call save on the non-document window
    future = doc_app._impl.save_command.action()
    doc_app.loop.run_until_complete(future)

    # Save wasn't invoked
    doc_app.save.assert_not_called()


def test_save_as_menu(doc_app, tmp_path):
    """The save as method can be triggered by menu"""
    # There is one document available, but it doesn't have a filename.
    assert len(doc_app.documents) == 1
    doc = doc_app.documents[0]
    assert doc.path is None

    # Prime the save file dialog with a response
    doc_path_1 = Path(tmp_path / "path/to/first.foobar")
    doc_path_2 = Path(tmp_path / "path/to/second.foobar")
    doc_app.current_window._impl.dialog_responses["SaveFileDialog"] = [
        doc_path_1,
        doc_path_2,
    ]

    # Save As the document with the menu
    future = doc_app._impl.save_as_command.action()
    doc_app.loop.run_until_complete(future)

    # Write was invoked on the document
    doc._write.assert_called_once_with(doc_path_1)
    assert doc.path == doc_path_1

    doc._write.reset_mock()

    # Save As the document a second time with a different name
    future = doc_app._impl.save_as_command.action()
    doc_app.loop.run_until_complete(future)

    # Write was invoked on the document
    doc._write.assert_called_once_with(doc_path_2)
    assert doc.path == doc_path_2


def test_save_as_menu_reject_name(doc_app, tmp_path):
    """Save As confirms overwrite of an existing name; if denied, a new filename is selected"""
    # There is one document available; but it doesn't have a filename.
    assert len(doc_app.documents) == 1
    doc = doc_app.documents[0]
    assert doc.path is None

    # Prime the save file dialog with 2 responses - one for an existing file
    doc_path_1 = Path(tmp_path / "path/to/first.foobar")
    doc_path_1.parent.mkdir(parents=True, exist_ok=True)
    doc_path_1.write_text("sample file")

    doc_path_2 = Path(tmp_path / "path/to/second.foobar")
    doc_app.current_window._impl.dialog_responses["SaveFileDialog"] = [
        doc_path_1,
        doc_path_2,
    ]
    # Prime the confirm dialog to reject the first candidate name.
    doc_app.current_window._impl.dialog_responses["ConfirmDialog"] = [False]

    # Save As the document with the menu
    future = doc_app._impl.save_as_command.action()
    doc_app.loop.run_until_complete(future)

    # Write was invoked on the document with
    doc._write.assert_called_once_with(doc_path_2)
    assert doc.path == doc_path_2


def test_save_as_menu_overwrite_name(doc_app, tmp_path):
    """Save As confirms overwrite of an existing name; if accepted, the filename is used"""
    # There is one document available; but it doesn't have a filename.
    assert len(doc_app.documents) == 1
    doc = doc_app.documents[0]
    assert doc.path is None

    # Prime the save file dialog with a response for an existing file
    doc_path = Path(tmp_path / "path/to/first.foobar")
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text("sample file")

    doc_app.current_window._impl.dialog_responses["SaveFileDialog"] = [doc_path]
    # Prime the confirm dialog to accept the existing name
    doc_app.current_window._impl.dialog_responses["ConfirmDialog"] = [True]

    # Save As the document with the menu
    future = doc_app._impl.save_as_command.action()
    doc_app.loop.run_until_complete(future)

    # Write was invoked on the document with
    doc._write.assert_called_once_with(doc_path)
    assert doc.path == doc_path


def test_save_as_non_document(doc_app):
    """If the current window isn't a document, save as is a no-op"""
    # There is one document available
    assert len(doc_app.documents) == 1

    # Create a non-document window, and set it as the current window
    window = toga.Window()
    window.content = toga.Box()
    window.show()
    doc_app.current_window = window

    # Invoke save-as on the non-doc window. This should be a no-op,
    # but there's nothing we can do to verify that it is.
    doc_app.loop.run_until_complete(doc_app.save_as(window))

    # Mock save as so we can check it isn't invoked by the menu
    doc_app.save_as = Mock()

    # Call save as on the non-document window
    future = doc_app._impl.save_as_command.action()
    doc_app.loop.run_until_complete(future)

    # Save As wasn't invoked
    doc_app.save_as.assert_not_called()


def test_save_as_menu_cancel(doc_app, tmp_path):
    """Save As can be cancelled by not selecting a file"""
    # There is one document available; but it doesn't have a filename.
    assert len(doc_app.documents) == 1
    doc = doc_app.documents[0]
    assert doc.path is None

    # Prime the save file dialog with a cancel response
    doc_app.current_window._impl.dialog_responses["SaveFileDialog"] = [None]

    # Save As the document with the menu
    future = doc_app._impl.save_as_command.action()
    doc_app.loop.run_until_complete(future)

    # Write was not invoked on the document
    doc._write.assert_not_called()
    assert doc.path is None


def test_save_all(doc_app, example_file, tmp_path):
    """Save All can be invoked"""
    # There is one pre-existing document available; but it doesn't have a filename.
    doc_0 = doc_app.documents[0]
    assert doc_0.path is None

    # Create a non-document window, and set it as the current window
    window = toga.Window()
    window.content = toga.Box()
    window.show()
    doc_app.current_window = window

    # Create a second document window that *does* have a filename
    doc_app.open(example_file)

    # There should be 3 windows, and 2 documents
    assert len(doc_app.documents) == 2
    assert len(doc_app.windows) == 3

    # Prime the save file dialog with a response for a new filename
    doc_0_path = Path(tmp_path / "path/to/first.foobar")
    doc_app.current_window._impl.dialog_responses["SaveFileDialog"] = [doc_0_path]

    # Save All with the menu
    future = doc_app._impl.save_all_command.action()
    doc_app.loop.run_until_complete(future)

    # Document 0 was saved with the new filename
    doc_app.documents[0]._write.assert_called_once_with(doc_0_path)
    doc_app.documents[0].path == doc_0_path

    # Save will have been invoked on the non-document window, but
    # it's a no-op with no side effects.

    # Document 1 was saved with the existing filename
    doc_app.documents[1]._write.assert_called_once_with(example_file)
    doc_app.documents[1].path == example_file


def test_save_all_disabled(doc_app, tmp_path):
    """If there are no document windows, Save All is a no-op"""
    # Create a non-document window, and set it as the current window
    window = toga.Window()
    window.content = toga.Box()
    window.show()
    doc_app.current_window = window

    # Close the document window
    doc = doc_app.documents[0]
    doc.main_window.close()

    # Mock save all so we can check it wasn't invoked
    doc_app.save_all = Mock()

    # Save All the document
    future = doc_app._impl.save_all_command.action()
    doc_app.loop.run_until_complete(future)

    # Save all wasn't called, because there are no current document windows
    doc_app.save_all.assert_not_called()


class DeprecatedDocumentApp(toga.DocumentApp):
    def startup(self):
        self.main_window = None


def test_deprecated_base_class(monkeypatch):
    """The DocumentApp base class has been deprecated"""
    monkeypatch.setattr(sys, "argv", ["app-exe"])

    with pytest.warns(
        DeprecationWarning,
        match=r"toga.DocumentApp is no longer required. Use toga.App instead",
    ):
        app = DeprecatedDocumentApp(
            "Test App",
            "org.beeware.document-app",
            document_types={"foobar": ExampleDocument},
        )

    assert app._impl.interface == app
    assert_action_performed(app, "create App")

    assert app.document_types == {"foobar": ExampleDocument}

    # With no command line, a default empty document will be created
    assert len(app.documents) == 1
    assert app.documents[0].path is None

    # Document window has been created and shown
    assert len(app.windows) == 1
    assert list(app.windows)[0] == app.documents[0].main_window
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")
