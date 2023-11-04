from __future__ import annotations

import asyncio
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from toga.app import App
    from toga.window import Window


class Document(ABC):
    def __init__(
        self,
        path: str | Path,
        document_type: str,
        app: App = None,
    ):
        """Create a new Document.

        :param path: The path where the document is stored.
        :param document_type: A human-readable description of the document type.
        :param app: The application the document is associated with.
        """
        self._path = Path(path)
        self._document_type = document_type
        self._app = app
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

        if can_close:
            if self._impl.SINGLE_DOCUMENT_APP:
                self.app.exit()
                return False
            else:
                return True
        else:
            return False

    @property
    def path(self) -> Path:
        """The path where the document is stored (read-only)."""
        return self._path

    @property
    def filename(self) -> Path:
        """**DEPRECATED** - Use :attr:`path`."""
        warnings.warn(
            "Document.filename has been renamed Document.path.",
            DeprecationWarning,
        )
        return self._path

    @property
    def document_type(self) -> Path:
        """A human-readable description of the document type (read-only)."""
        return self._document_type

    @property
    def app(self) -> App:
        """The app that this document is associated with (read-only)."""
        return self._app

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
