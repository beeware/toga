from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .base import Widget


class ScrollContainer(Widget):
    def __init__(self, horizontal=True, vertical=True):
        super(ScrollContainer, self).__init__()
        self.horizontal = horizontal
        self.vertical = vertical

        self._content = None

        self.startup()

    def startup(self):
        self._impl = Gtk.ScrolledWindow()
        self._impl.set_policy(
            Gtk.PolicyType.AUTOMATIC if self.horizontal else Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC if self.vertical else Gtk.PolicyType.NEVER,
        )

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self.window
        self._content.app = self.app

        self._impl.add_with_viewport(self._content._impl)

    def _set_app(self, app):
        if self._content:
            self._content.app = app

    def _set_window(self, window):
        if self._content:
            self._content.window = window
            if window:
                self._impl.set_min_content_width(min(self.window._size[0], self._content._width_hint[0]))
                self._impl.set_min_content_height(min(self.window._size[1], self._content._height_hint[0]))
