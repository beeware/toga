import sys
from pathlib import Path

import pytest

import toga
from toga_dummy.app import App as DummyApp
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
)


class ExampleDocument(toga.Document):
    def __init__(self, path, app):
        super().__init__(path=path, document_type="Example Document", app=app)

    def create(self):
        self.main_window = toga.DocumentMainWindow(self)

    def read(self):
        self.content = self.path


class ExampleDocumentApp(toga.DocumentApp):
    def startup(self):
        self.main_window = None


@pytest.fixture
def doc_app(event_loop):
    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={
            # Register ExampleDocument
            "foobar": ExampleDocument,
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
    app.main_loop()

    assert app._impl.interface == app
    assert_action_performed(app, "create DocumentApp")

    assert app.document_types == {"foobar": ExampleDocument}
    assert app.documents == []


def test_create_with_cmdline(monkeypatch):
    """If a document is specified at the command line, it is opened."""
    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/filename.foobar"])

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )
    app.main_loop()

    assert app._impl.interface == app
    assert_action_performed(app, "create DocumentApp")

    assert app.document_types == {"foobar": ExampleDocument}
    assert len(app.documents) == 1
    assert isinstance(app.documents[0], ExampleDocument)

    # Document content has been read
    assert app.documents[0].content == Path("/path/to/filename.foobar")

    # Document window has been created and shown
    assert_action_performed(app.documents[0].main_window, "create DocumentMainWindow")
    assert_action_performed(app.documents[0].main_window, "show")


def test_create_with_unknown_document_type(monkeypatch):
    """If the document specified at the command line is an unknown type, an exception is
    raised."""
    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/filename.unknown"])

    with pytest.raises(
        ValueError,
        match=r"Don't know how to open documents of type .unknown",
    ):
        ExampleDocumentApp(
            "Test App",
            "org.beeware.document-app",
            document_types={"foobar": ExampleDocument},
        )


def test_create_no_document_type():
    """A document app must manage at least one document type."""
    with pytest.raises(
        ValueError,
        match=r"A document must manage at least one document type.",
    ):
        toga.DocumentApp("Test App", "org.beeware.document-app")


def test_close_last_document_non_persistent(monkeypatch):
    """Non-persistent apps exit when the last document is closed"""
    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/example.foobar"])

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )
    # Create a second window
    # TODO: Use the document interface for this
    # app.open(other_file)
    _ = toga.Window()

    # There are 2 open documents
    # assert len(app.documents) == 2
    assert len(app.windows) == 2

    # Close the first document window
    list(app.windows)[0].close()

    # One document window closed.
    # assert len(app.documents) == 1
    assert len(app.windows) == 1

    # App hasn't exited
    assert_action_not_performed(app, "exit")

    # Close the last remaining document window
    list(app.windows)[0].close()

    # App has now exited
    assert_action_performed(app, "exit")


def test_close_last_document_persistent(monkeypatch):
    """Persistent apps don't exit when the last document is closed"""
    # Monkeypatch the property that makes the backend persistent
    monkeypatch.setattr(DummyApp, "CLOSE_ON_LAST_WINDOW", False)

    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/example.foobar"])

    app = ExampleDocumentApp(
        "Test App",
        "org.beeware.document-app",
        document_types={"foobar": ExampleDocument},
    )
    # Create a second window
    # TODO: Use the document interface for this
    # app.open(other_file)
    _ = toga.Window()

    # There are 2 open documents
    # assert len(app.documents) == 2
    assert len(app.windows) == 2

    # Close the first document window
    list(app.windows)[0].close()

    # One document window closed.
    # assert len(app.documents) == 1
    assert len(app.windows) == 1

    # App hasn't exited
    assert_action_not_performed(app, "exit")

    # Close the last remaining document window
    list(app.windows)[0].close()

    # No document windows.
    # assert len(app.documents) == 0
    assert len(app.windows) == 0

    # App still hasn't exited
    assert_action_not_performed(app, "exit")
