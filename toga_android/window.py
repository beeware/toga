

class Window(object):
    def __init__(self):
        self._app = None
        self._content = None

        self.startup()

    def startup(self):
        pass

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self
        self._content.app = self.app

    def show(self):
        pass
