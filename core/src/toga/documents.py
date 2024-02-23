from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from toga.app import App
    from toga.window import Window


class Document(ABC):
    # Subclasses should override these definitions
    document_type = "Unknown Document"
    default_extension = ".unknown"

    def __init__(self, app: App):
        """Create a new Document.

        :param app: The application the document is associated with.
        """
        self._app = app
        self._path = None
        self._main_window = None

        # Create the visual representation of the document
        self.create()

        # Create a platform specific implementation of the Document
        self._impl = app.factory.Document(interface=self)

    def can_close(self) -> bool:
        """Is the main document window allowed to close?

        The default implementation always returns ``True``; subclasses can override this
        to prevent a window closing with unsaved changes, etc.

        This default implementation is a function; however, subclasses can define it
        as an asynchronous co-routine if necessary to allow for dialog confirmations.
        """
        return True

    async def handle_close(self, window, **kwargs):
        """An ``on-close`` handler for the main window of this document that implements
        platform-specific document close behavior.

        It interrogates the :meth:`~toga.Document.can_close()` method to determine if
        the document is allowed to close.
        """
        if asyncio.iscoroutinefunction(self.can_close):
            can_close = await self.can_close()
        else:
            can_close = self.can_close()

        # If the document is allowed to close, remove it from the list of documents,
        # managed by the app.
        if can_close:
            self._app._documents.remove(self)

        return can_close

    @property
    def path(self) -> Path:
        """The path where the document is stored (read-only)."""
        return self._path

    @property
    def app(self) -> App:
        """The app that this document is associated with (read-only)."""
        return self._app

    @property
    def title(self) -> str:
        """The title of the document.

        This will be used as the default title of a :any:`toga.DocumentMainWindow` that
        contains the document.
        """
        return f"{self.document_type}: {self.path.name if self.path else 'Untitled'}"

    @property
    def main_window(self) -> Window:
        """The main window for the document."""
        return self._main_window

    @main_window.setter
    def main_window(self, window):
        self._main_window = window

    def show(self) -> None:
        """Show the :any:`main_window` for this document."""
        self.main_window.show()

    def open(self, path: str | Path):
        """Open a file as a document.

        :param path: The file to open.
        """
        self._path = Path(path)
        self._impl.open()

        # Set the title of the document window to match the path
        self._main_window.title = self._main_window._default_title

    def save(self, path: str | Path | None = None):
        """Save the document as a file.

        If a path is provided, the path for the document will be updated.
        Otherwise, the existing path will be used.
        :param path: If provided, the new file name for the document.
        """
        if path:
            self._path = Path(path)
            # Re-set the title of the document with the new path
            self._main_window.title = self._main_window._default_title
        self.write()

    @abstractmethod
    def create(self) -> None:
        """Create the window (or windows) for the document.

        This method must, at a minimum, assign the :any:`main_window` property. It
        may also create additional windows or UI elements if desired.
        """

    @abstractmethod
    def read(self) -> None:
        """Load a representation of the document into memory and populate the document
        window."""

    @abstractmethod
    def write(self) -> None:
        """Persist a representation of the current state of the document."""
