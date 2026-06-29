from __future__ import annotations

from typing import TYPE_CHECKING

from toga.platform import get_factory

if TYPE_CHECKING:
    from typing import Any

    from .app import App
    from .widget import Widget
    from .window import Window
from abc import ABC, abstractmethod


class BaseScaffold(ABC):
    @abstractmethod
    def __init__(self, content: Any = None):
        self.factory = get_factory()
        self._impl = self._create()
        self._window = None
        self._app = None

    @abstractmethod
    def _create(self) -> Any: ...

    def refresh(self):
        self._impl.refresh()

    @property
    def window(self) -> Window | None:
        return self._window

    @window.setter
    def window(self, value: Window | None):
        self._window = value

    @property
    def app(self) -> App | None:
        return self._app

    @app.setter
    def app(self, value):
        self._app = value


class Scaffold(BaseScaffold):
    def __init__(self, content: Widget | None = None):
        super().__init__()
        self._content = None
        self.content = content

    def _create(self):
        return get_factory().Scaffold(self)

    @property
    def content(self) -> Widget | None:
        return self._content

    @content.setter
    def content(self, value: Widget | None):
        if self._content is not None:
            # Clear the old content's window, app, and scaffold
            self._content.window = None
            self._content.app = None
            self._content.scaffold = None
        self._content = value
        if value is not None:
            self._content.scaffold = self
        self._impl.set_content(value._impl if value is not None else None)
        if value is not None:
            self._content.window = self.window
            self._content.app = self.app
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
