from __future__ import print_function, absolute_import, division

from gi.repository import Gtk


class Window(object):
    _IMPL_CLASS = Gtk.Window

    def __init__(self, position=(100, 100), size=(640, 480)):
        self._app = None
        self._impl = None

    def _startup(self):
        self._impl = self._IMPL_CLASS()
        self._impl.connect("delete-event", self._on_close)
        self.on_startup()

        if self.content:
            # Assign the widget to the same app as the window.
            # This initiates startup logic.
            self.content.app = self.app

            self._impl.add(self.content._impl)

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app
        self._startup()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self
        if self._impl:
            # Assign the widget to the same app as the window.
            # This initiates startup logic.
            widget.app = self.app

            self._impl.add(self._content._impl)

    def show(self):
        self._impl.show_all()

    def on_startup(self):
        pass

    def _on_close(self, widget, data):
        self.on_close()

    def on_close(self):
        pass
