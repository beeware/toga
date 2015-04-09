from __future__ import print_function, absolute_import, division

from colosseum import CSSNode

class Widget(CSSNode):
    def __init__(self, **style):
        super(Widget, self).__init__(**style)
        self._window = None
        self._app = None
        self._impl = None

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Widget %r is already associated with an App" % self)
        self._app = app
        self._set_app(app)

    def _set_app(self, app):
        pass

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        self._window = window
        self._set_window(window)

    def _set_window(self, window):
        pass

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, id(self))
