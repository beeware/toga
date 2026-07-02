from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from toga.platform import get_factory

if TYPE_CHECKING:
    from typing import Any

    from toga.app import App
    from toga.widgets.base import Widget
    from toga.window import Window


class BaseScaffold(ABC):
    @abstractmethod
    def __init__(self):
        self.factory = get_factory()
        self._impl = self._create()
        self._window = None
        self._app = None

    @abstractmethod
    def _create(self) -> Any: ...

    def refresh(self):
        self._impl.refresh()

    # The setters below are all abstract, as the child class must register
    # content with app/window and vice versa.
    @property
    def window(self) -> Window | None:
        return self._window

    @window.setter
    @abstractmethod
    def window(self, value: Window | None):
        self._window = value

    @property
    def app(self) -> App | None:
        return self._app

    @app.setter
    @abstractmethod
    def app(self, value):
        self._app = value


class Scaffold(BaseScaffold):
    def __init__(self, content: Widget = None):
        super().__init__()
        self._content = None
        self.content = content

    def _create(self):
        return get_factory().Scaffold(self)

    @property
    def content(self) -> Any | None:
        return self._content

    @content.setter
    def content(self, value: Widget | None):
        if self._content is not None:
            # Clear the old content's window, app, and scaffold
            self._content.window = None
            self._content.app = None
            self._content.scaffold = None
        if value is not None:
            value.scaffold = self
            value.window = self.window
            value.app = self.app

        self._content = value
        if value is not None:
            self._impl.set_content(self._content._impl)
        else:
            self._impl.set_content(None)
        self.refresh()

    @BaseScaffold.window.setter
    def window(self, value: Window | None):
        BaseScaffold.window.fset(self, value)
        if self.content is not None:
            # Track our content's window
            self.content.window = value

    @BaseScaffold.app.setter
    def app(self, value):
        BaseScaffold.app.fset(self, value)
        if self.content is not None:
            # Track our content's app
            self.content.app = value
