import asyncio
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga.platform import get_platform_factory
from toga_dummy.documents import Document as DummyDocument
from toga_dummy.utils import assert_action_performed


class ExampleDocument(toga.Document):
    def __init__(self, path, app):
        super().__init__(path=path, document_type="Example Document", app=app)

    def create(self):
        self.main_window = toga.DocumentMainWindow(self)

    def read(self):
        self.content = self.path


def test_create_no_cmdline(monkeypatch):
    """A document app can be created with no command line."""
    monkeypatch.setattr(sys, "argv", ["app-exe"])

    app = toga.DocumentApp(
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

    app = toga.DocumentApp(
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
    assert_action_performed(app.documents[0].main_window, "create Window")
    assert_action_performed(app.documents[0].main_window, "show")


def test_create_with_unknown_document_type(monkeypatch):
    """If the document specified at the command line is an unknown type, an exception is raised"""
    monkeypatch.setattr(sys, "argv", ["app-exe", "/path/to/filename.unknown"])

    with pytest.raises(
        ValueError,
        match=r"Don't know how to open documents of type .unknown",
    ):
        toga.DocumentApp(
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


def test_close_single_document_app():
    """An app in single document mode closes the app when the window is closed"""
    # Monkeypatch the dummy impl to use single document mode
    DummyDocument.SINGLE_DOCUMENT_APP = True

    # Mock the app, but preserve the factory
    app = Mock()
    app.factory = get_platform_factory()

    doc = ExampleDocument(path=Path("/path/to/doc.txt"), app=app)

    # Window technically was prevented from closing, but the app has been exited.
    # This must be run as a co-routine.
    async def _do_close():
        return await doc.handle_close(Mock())

    assert not asyncio.get_event_loop().run_until_complete(_do_close())
    app.exit.assert_called_once_with()


def test_close_multiple_document_app():
    """An app in multiple document mode doesn't close when the window is closed"""
    # Monkeypatch the dummy impl to use single document mode
    DummyDocument.SINGLE_DOCUMENT_APP = False

    # Mock the app, but preserve the factory
    app = Mock()
    app.factory = get_platform_factory()

    doc = ExampleDocument(path=Path("/path/to/doc.txt"), app=app)

    # Window has closed, but app has not exited.
    # This must be run as a co-routine.
    async def _do_close():
        return await doc.handle_close(Mock())

    assert asyncio.get_event_loop().run_until_complete(_do_close())
    app.exit.assert_not_called()


@pytest.mark.parametrize("is_single_doc_app", [True, False])
def test_no_close(monkeypatch, is_single_doc_app):
    """A document can prevent itself from being closed."""
    # Monkeypatch the dummy impl to set the app mode
    DummyDocument.SINGLE_DOCUMENT_APP = is_single_doc_app

    # Monkeypatch the Example document to prevent closing.
    # Define this as a co-routine to simulate an implementation that called a dialog.
    async def can_close(self):
        return False

    ExampleDocument.can_close = can_close

    # Mock the app, but preserve the factory
    app = Mock()
    app.factory = get_platform_factory()

    doc = ExampleDocument(path=Path("/path/to/doc.txt"), app=app)

    # Window was prevented from closing.
    # This must be run as a co-routine.
    async def _do_close():
        await doc.handle_close(Mock())

    assert not asyncio.get_event_loop().run_until_complete(_do_close())
    app.exit.assert_not_called()
