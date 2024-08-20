from unittest.mock import Mock

import toga
from toga_dummy.utils import assert_action_not_performed, assert_action_performed


class ExampleDocument(toga.Document):
    description = "Example Document"
    extensions = "exampledoc"
    read_error = None
    write_error = None

    def create(self):
        self.main_window = toga.DocumentWindow(self)
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


def test_create(app):
    """A MainWindow can be created with minimal arguments."""
    doc = ExampleDocument(app)

    # The document has a main window.
    window = doc.main_window

    assert window.app == app
    assert window.content is None
    # Document reference is preserved
    assert window.doc == doc

    assert window._impl.interface == window
    assert_action_performed(window, "create MainWindow")

    # This is a secondary main window; app menus have not been created, but
    # window menus and toolbars have been.
    assert_action_not_performed(window, "create App menus")
    assert_action_performed(window, "create Window menus")
    assert_action_performed(window, "create toolbar")

    # We can't know what the ID is, but it must be a string.
    assert isinstance(window.id, str)
    # Window title is the document title.
    assert window.title == "Example Document: Untitled"
    # The app has created a main window, so this will be the second window.
    assert window.position == (150, 150)
    assert window.size == (640, 480)
    assert window.resizable
    assert window.closable
    assert window.minimizable
    # Default on-close handler is to confirm close.
    assert window.on_close._raw == window._confirm_close

    # The window has an empty toolbar; but it's also a secondary MainWindow created
    # *after* the app has finished initializing; check it has a change handler
    assert len(window.toolbar) == 0
    assert window.toolbar.on_change is not None


def test_create_explicit(app):
    """Explicit arguments at construction are stored."""
    on_close_handler = Mock()
    window_content = toga.Box()
    # Don't use a document, because we want to exercise the constructor
    doc = Mock()

    window = toga.DocumentWindow(
        doc=doc,
        id="my-window",
        title="My Window",
        position=toga.Position(10, 20),
        size=toga.Position(200, 300),
        resizable=False,
        minimizable=False,
        content=window_content,
        on_close=on_close_handler,
    )

    assert window.app == app
    assert window.content == window_content
    # Document reference is preserved
    assert window.doc == doc

    window_content.window == window
    window_content.app == app

    assert window._impl.interface == window
    assert_action_performed(window, "create MainWindow")

    # This is a secondary main window; app menus have not been created, but
    # window menus and toolbars have been.
    assert_action_not_performed(window, "create App menus")
    assert_action_performed(window, "create Window menus")
    assert_action_performed(window, "create toolbar")

    assert window.id == "my-window"
    assert window.title == "My Window"
    assert window.position == toga.Position(10, 20)
    assert window.size == toga.Size(200, 300)
    assert not window.resizable
    assert window.closable
    assert not window.minimizable
    assert window.on_close._raw == on_close_handler

    # The window has an empty toolbar; but it's also a secondary MainWindow created
    # *after* the app has finished initializing; check it has a change handler
    assert len(window.toolbar) == 0
    assert window.toolbar.on_change is not None


def test_close_unmodified(app):
    """An unmodified document doesn't need to be saved."""
    doc = ExampleDocument(app)
    assert not doc.modified

    window = doc.main_window

    # Trigger a window close
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert window.closed
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")

    # No save attempt was made.
    doc._mock_write.assert_not_called()


def test_close_modified(app):
    """If the save succeeds, the window will close."""
    mock_path = Mock()
    doc = ExampleDocument(app)
    doc._path = mock_path
    doc.touch()
    assert doc.modified

    window = doc.main_window
    # Prime the user's responses to the dialogs
    window._impl.dialog_responses["QuestionDialog"] = [True]

    # Trigger a window close
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert window.closed
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")

    # A save attempt was made.
    doc._mock_write.assert_called_once_with(mock_path)


def test_close_modified_cancel(app):
    """The user can choose to *not* save."""
    mock_path = Mock()
    doc = ExampleDocument(app)
    doc._path = mock_path
    doc.touch()
    assert doc.modified

    window = doc.main_window
    # Prime the user's responses to the dialogs
    window._impl.dialog_responses["QuestionDialog"] = [False]

    # Trigger a window close
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert window.closed
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")

    # No save attempt was made.
    doc._mock_write.assert_not_called()


def test_close_modified_unsaved(monkeypatch, app, tmp_path):
    """If a document is modified but unsaved, the save prompts for a filename."""
    monkeypatch.setattr(app.documents, "_types", ExampleDocument)
    doc = ExampleDocument(app)
    doc.touch()
    assert doc.modified

    window = doc.main_window
    # Prime the user's responses to the dialogs
    window._impl.dialog_responses["QuestionDialog"] = [True]
    new_path = tmp_path / "foo.exampledoc"
    window._impl.dialog_responses["SaveFileDialog"] = [new_path]

    # Trigger a window close
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert window.closed
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")

    # A save attempt was made.
    doc._mock_write.assert_called_once_with(new_path)


def test_close_modified_save_cancel(monkeypatch, app, tmp_path):
    """A close is aborted by canceling the save."""
    monkeypatch.setattr(app.documents, "_types", ExampleDocument)
    doc = ExampleDocument(app)
    doc.touch()
    assert doc.modified

    window = doc.main_window
    # Prime the user's responses to the dialogs
    window._impl.dialog_responses["QuestionDialog"] = [True]
    window._impl.dialog_responses["SaveFileDialog"] = [None]

    # Trigger a window close
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert not window.closed
    assert window.app == app
    assert window in app.windows
    assert_action_not_performed(window, "close")

    # No save attempt was made.
    doc._mock_write.assert_not_called()
