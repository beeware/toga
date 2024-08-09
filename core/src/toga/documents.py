from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from toga.handlers import overridable, overridden

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
        self.modified = False

        # Create the visual representation of the document.
        self.create()

        # Add the document to the list of managed documents.
        self.app._documents._add(self)

    ######################################################################
    # Document properties
    ######################################################################
    @property
    def default_extension(self) -> str:
        """The default extension for documents of this type.

        Inspects the extensions against which this document type is registered
        with the app, and returns the first match.
        """
        try:
            return [
                extension
                for extension, document_type in self.app.document_types.items()
                if isinstance(self, document_type)
            ][0]
        except IndexError:
            raise RuntimeError("Document type isn't registered with the current app")

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
        return f"{self.document_type}: {self.path.stem if self.path else 'Untitled'}"

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

    def close(self):
        """Close all the windows for this document.

        This will immediately close any document windows, *without* invoking any
        ``on_close`` handlers.
        """
        self.main_window.close()

    def focus(self):
        """Give the document focus in the app."""
        self.app.current_window = self.main_window

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
