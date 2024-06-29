from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from toga.app import App
    from toga.window import Window


class Document(ABC):
    # Subclasses should override this definition

    #: A short description of the type of document
    document_type: str

    def __init__(self, app: App):
        """Create a new Document.

        :param app: The application the document is associated with.
        """
        self._path: Path | None = None
        self._app = app
        self._main_window: Window | None = None

        # Create the visual representation of the document
        self.create()

        # Create a platform specific implementation of the Document
        self._impl = app.factory.Document(interface=self)

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

        This will be used as the default title of a :any:`toga.DocumentMainWindow` that
        contains the document.
        """
        return f"{self.document_type}: {self.path.name if self.path else 'Untitled'}"

    ######################################################################
    # Document operations
    ######################################################################

    def close(self):
        """Close all the windows for this document.

        This will immediately close any document windows, *without* invoking any
        ``on_close`` handlers.
        """
        self.main_window.close()

    def open(self, path: str | Path):
        """Open a file as a document.

        :param path: The file to open.
        """
        self._path = Path(path).absolute()
        self._impl.open()

        # Set the title of the document window to match the path
        self._main_window.title = self._main_window._default_title

    def show(self) -> None:
        """Show the visual representation for this document."""
        self.main_window.show()

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
