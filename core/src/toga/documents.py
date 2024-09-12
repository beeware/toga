from __future__ import annotations

import itertools
import sys
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Mapping, Sequence

import toga
from toga import dialogs
from toga.handlers import overridable, overridden
from toga.window import MainWindow, Window

if TYPE_CHECKING:
    from toga.app import App


class Document(ABC):
    #: A short description of the type of document (e.g., "Text document"). This is a
    #: class variable that subclasses should define.
    description: str

    #: A list of extensions that documents of this type might use, without leading dots (e.g.,
    #: ``["doc", "txt"]``). The list must have at least one extension; the first is the
    #: default extension for documents of this type. This is a class variable that
    #: subclasses should define.
    extensions: list[str]

    def __init__(self, app: App):
        """Create a new Document. Do not call this constructor directly - use
        :any:`DocumentSet.new`, :any:`DocumentSet.open` or
        :any:`DocumentSet.request_open` instead.

        :param app: The application the document is associated with.
        """
        self._path: Path | None = None
        self._app = app
        self._main_window: Window | None = None
        self.modified = False

        # Create the visual representation of the document.
        self.create()

        # Add the document to the list of managed documents.
        self.app._documents._add(self)

    ######################################################################
    # Document properties
    ######################################################################
    @property
    def path(self) -> Path:
        """The path where the document is stored (read-only)."""
        return self._path

    @property
    def app(self) -> App:
        """The app that this document is associated with (read-only)."""
        return self._app

    @property
    def main_window(self) -> Window | None:
        """The main window for the document."""
        return self._main_window

    @main_window.setter
    def main_window(self, window: Window) -> None:
        self._main_window = window

    @property
    def title(self) -> str:
        """The title of the document.

        This will be used as the default title of a :any:`toga.DocumentWindow` that
        contains the document.
        """
        return f"{self.description}: {self.path.stem if self.path else 'Untitled'}"

    @property
    def modified(self) -> bool:
        """Has the document been modified?"""
        return self._modified

    @modified.setter
    def modified(self, value: bool):
        self._modified = bool(value)

    ######################################################################
    # Document operations
    ######################################################################

    def focus(self):
        """Give the document focus in the app."""
        self.app.current_window = self.main_window

    def hide(self) -> None:
        """Hide the visual representation for this document."""
        self.main_window.hide()

    def open(self, path: str | Path):
        """Open a file as a document.

        :param path: The file to open.
        """
        self._path = Path(path).absolute()
        if self._path.exists():
            self.read()
        else:
            raise FileNotFoundError()

        # Set the title of the document window to match the path
        self._main_window.title = self._main_window._default_title
        # Document is initially unmodified
        self.modified = False

    def save(self, path: str | Path | None = None):
        """Save the document as a file.

        If a path is provided, and the :meth:`~toga.Document.write` method has been
        overwritten, the path for the document will be updated. Otherwise, the existing
        path will be used.

        :param path: If provided, the new file name for the document.
        """
        if overridden(self.write):
            if path:
                self._path = Path(path).absolute()
                # Re-set the title of the document with the new path
                self._main_window.title = self._main_window._default_title
            self.write()
            # Clear the modification flag.
            self.modified = False

    def show(self) -> None:
        """Show the visual representation for this document."""
        self.main_window.show()

    def touch(self, *args, **kwargs):
        """Mark the document as modified.

        This method accepts `*args` and `**kwargs` so that it can be used as an
        ``on_change`` handler; these arguments are not used.
        """
        self.modified = True

    ######################################################################
    # Abstract interface
    ######################################################################

    @abstractmethod
    def create(self) -> None:
        """Create the window (or windows) for the document.

        This method must, at a minimum, assign the :any:`main_window` property. It
        may also create additional windows or UI elements if desired.
        """

    @abstractmethod
    def read(self) -> None:
        """Load a representation of the document into memory from
        :attr:`~toga.Document.path`, and populate the document window.
        """

    @overridable
    def write(self) -> None:
        """Persist a representation of the current state of the document.

        This method is a no-op by default, to allow for read-only document types.
        """


class DocumentSet(Sequence[Document], Mapping[Path, Document]):
    def __init__(self, app: App, types: list[type[Document]]):
        """A collection of documents managed by an app.

        A document is automatically added to the app when it is created, and removed
        when it is closed. The document collection will be stored in the order that
        documents were created.

        :param app: The app that this instance is bound to.
        :param types: The document types managed by this app.
        """
        self.app = app
        for doc_type in types:
            if not hasattr(doc_type, "description"):
                raise ValueError(
                    f"Document type {doc_type.__name__!r} "
                    "doesn't define a 'descriptions' attribute"
                )
            if not hasattr(doc_type, "extensions"):
                raise ValueError(
                    f"Document type {doc_type.__name__!r} "
                    "doesn't define an 'extensions' attribute"
                )
            if len(doc_type.extensions) == 0:
                raise ValueError(
                    f"Document type {doc_type.__name__!r} "
                    "doesn't define at least one extension"
                )

        self._types = types

        self.elements: list[Document] = []

    @property
    def types(self) -> list[type[Document]]:
        """The list of document types the app can manage.

        The first document type in the list is the app's default document type.
        """
        return self._types

    def __iter__(self) -> Iterator[Document]:
        return iter(self.elements)

    def __contains__(self, value: object) -> bool:
        return value in self.elements

    def __len__(self) -> int:
        return len(self.elements)

    def __getitem__(self, path_or_index):
        # Look up by index
        if isinstance(path_or_index, int):
            return self.elements[path_or_index]

        # Look up by path
        if sys.version_info < (3, 9):  # pragma: no-cover-if-gte-py39
            # resolve() *should* turn the path into an absolute path;
            # but on Windows, with Python 3.8, it doesn't.
            path = Path(path_or_index).absolute().resolve()
        else:  # pragma: no-cover-if-lt-py39
            path = Path(path_or_index).resolve()
        for item in self.elements:
            if item.path == path:
                return item

        # No match found
        raise KeyError(path_or_index)

    def _add(self, document: Path):
        if document in self:
            raise ValueError("Document is already being managed.")

        self.elements.append(document)

    def _remove(self, document: Path):
        if document not in self:
            raise ValueError("Document is not being managed.")

        self.elements.remove(document)

    def new(self, document_type: type[Document]) -> Document:
        """Create a new document of the given type, and show the document window.

        :param document_type: The document type that has been requested.
        :returns: The newly created document.
        """
        document = document_type(app=self.app)
        document.show()
        return document

    async def request_open(self) -> Document:
        """Present a dialog asking the user for a document to open, and pass the
        selected path to :meth:`open`.

        :returns: The document that was opened.
        :raises ValueError: If the path describes a file that is of a type that doesn't
            match a registered document type.
        """
        # A safety catch: if app modal dialogs aren't actually modal (eg, macOS) prevent
        # a second open dialog from being opened when one is already active. Attach the
        # dialog instance as a private attribute; delete as soon as the future is
        # complete.
        if hasattr(self, "_open_dialog"):
            return

        # CLOSE_ON_LAST_WINDOW is a proxy for the GTK/Windows behavior of loading content
        # into the existing window. This is actually implemented by creating a new window
        # and disposing of the old one; mark the current window for cleanup
        current_window = self.app.current_window
        if self.app._impl.CLOSE_ON_LAST_WINDOW:
            if hasattr(self.app.current_window, "_commit"):
                if await self.app.current_window._commit():
                    current_window._replace = True
                else:
                    # The changes in the current document window couldn't be committed
                    # (e.g., a save was requested, but then cancelled), so we can't
                    # proceed with opening a new document.
                    return

        self._open_dialog = dialogs.OpenFileDialog(
            self.app.formal_name,
            file_types=(
                list(itertools.chain(*(doc_type.extensions for doc_type in self.types)))
                if self.types
                else None
            ),
        )
        path = await self.app.dialog(self._open_dialog)
        del self._open_dialog

        try:
            if path:
                return self.open(path)
        finally:
            # Remove the replacement marker
            if hasattr(current_window, "_replace"):
                del current_window._replace

    def open(self, path: Path | str) -> Document:
        """Open a document in the app, and show the document window.

        If the provided path is already an open document, the existing representation for
        the document will be given focus.

        :param path: The path to the document to be opened.
        :returns: The document that was opened.
        :raises ValueError: If the path describes a file that is of a type that doesn't
            match a registered document type.
        """
        try:
            if sys.version_info < (3, 9):  # pragma: no-cover-if-gte-py39
                # resolve() *should* turn the path into an absolute path;
                # but on Windows, with Python 3.8, it doesn't.
                path = Path(path).absolute().resolve()
            else:  # pragma: no-cover-if-lt-py39
                path = Path(path).resolve()
            document = self.app.documents[path]
            document.focus()
            return document
        except KeyError:
            # No existing representation for the document.
            try:
                DocType = {
                    extension: doc_type
                    for doc_type in self.types
                    for extension in doc_type.extensions
                }[path.suffix[1:]]
            except KeyError:
                raise ValueError(
                    f"Don't know how to open documents with extension {path.suffix}"
                )
            else:
                prev_window = self.app.current_window
                document = DocType(app=self.app)
                try:
                    document.open(path)

                    # If the previous window is marked for replacement, close it; but
                    # put the new document window in the same position as the previous
                    # one.
                    if getattr(prev_window, "_replace", False):
                        document.main_window.position = prev_window.position
                        prev_window.close()

                    document.show()
                    return document
                except Exception:
                    # Open failed; ensure any windows opened by the document are closed.
                    document.main_window.close()
                    raise

    async def save(self):
        """Save the current content of an app.

        If there isn't a current window, or current window doesn't define a ``save()``
        method, the save request will be ignored.
        """
        if hasattr(self.app.current_window, "save"):
            await self.app.current_window.save()

    async def save_as(self):
        """Save the current content of an app under a different filename.

        If there isn't a current window, or the current window hasn't defined a
        ``save_as()`` method, the save-as request will be ignored.
        """
        if hasattr(self.app.current_window, "save_as"):
            await self.app.current_window.save_as()

    async def save_all(self):
        """Save the state of all content in the app.

        This method will attempt to call ``save()`` on every window associated with the
        app. Any windows that do not provide a ``save()`` method will be ignored.
        """
        for window in self.app.windows:
            if hasattr(window, "save"):
                await window.save()


class DocumentWindow(MainWindow):
    def __init__(self, doc: Document, *args, **kwargs):
        """Create a new document Window.

        A document window is a MainWindow (so it will have a menu bar, and *can* have a
        toolbar), bound to a document instance.

        In addition to the required ``doc`` argument, accepts the same arguments as
        :class:`~toga.Window`.

        The default ``on_close`` handler will use the document's modification status to
        determine if the document has been modified. It will allow the window to close
        if the document is fully saved, or the user explicitly declines the opportunity
        to save.

        :param doc: The document being managed by this window
        """
        self._doc = doc
        if "on_close" not in kwargs:
            kwargs["on_close"] = self._confirm_close

        super().__init__(*args, **kwargs)

    @property
    def doc(self) -> Document:
        """The document displayed by this window."""
        return self._doc

    @property
    def _default_title(self) -> str:
        return self.doc.title

    async def _confirm_close(self, window, **kwargs):
        if self.doc.modified:
            if await self.dialog(
                toga.QuestionDialog(
                    "Save changes?",
                    "This document has unsaved changes. Do you want to save these changes?",
                )
            ):
                return await self.save()
        return True

    async def _commit(self):
        # Get the window into a state where new content could be opened.
        # Used by the open method on GTK/Linux to ensure the current document
        # has been saved before closing this window and opening a replacement.
        return await self._confirm_close(self)

    def _close(self):
        # When then window is closed, remove the document it is managing from the app's
        # list of managed documents.
        self._app._documents._remove(self.doc)
        super()._close()

    async def save(self):
        """Save the document associated with this window.

        If the document associated with a window hasn't been saved before, and the
        document type defines a :meth:`~toga.Document.write` method, the user will be
        prompted to provide a filename.

        :returns: True if the save was successful; False if the save was aborted.
        """
        if overridden(self.doc.write):
            if self.doc.path:
                # Document has been saved previously; save using that filename.
                self.doc.save()
                return True
            else:
                return await self.save_as()
        return False

    async def save_as(self):
        """Save the document associated with this window under a new filename.

        The default implementation will prompt the user for a new filename, then save
        the document with that new filename. If the document type doesn't define a
        :meth:`~toga.Document.write` method, the save-as request will be ignored.

        :returns: True if the save was successful; False if the save was aborted.
        """
        if overridden(self.doc.write):
            suggested_path = (
                self.doc.path if self.doc.path else f"Untitled.{self.doc.extensions[0]}"
            )
            new_path = await self.dialog(
                dialogs.SaveFileDialog("Save as...", suggested_path)
            )
            # If a filename has been returned, save using that filename.
            # If there isn't a filename, the save was cancelled.
            if new_path:
                self.doc.save(new_path)
                return True

        return False
