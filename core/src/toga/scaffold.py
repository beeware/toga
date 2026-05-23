from toga.platform import get_factory


class BaseScaffold:
    def refresh(self):
        self._impl.refresh()


class Scaffold(BaseScaffold):
    _SCAFFOLD_CLASS = "Scaffold"

    def __init__(self, content):
        self.factory = get_factory()
        self._impl = getattr(self.factory, self._SCAFFOLD_CLASS)(self)
        self._window = None
        self._app = None
        self.content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if self._content is not None:
            # Clear the old content's window and app
            self._content.window = None
            self._content.app = None
        self._content = value
        self._impl.set_content(value._impl)
        self._content.window = self._window
        self._content.app = self._app

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, value):
        self._window = value
        # Track our content's window
        self.content.window = value

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, value):
        self._app = value
        # Track our content's app
        self.content.app = value
