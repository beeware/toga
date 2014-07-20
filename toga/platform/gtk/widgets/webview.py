from __future__ import print_function, absolute_import, division

from gi.repository import Gtk, WebKit

from .base import Widget


class WebView(Widget):
    def __init__(self, url=None):
        super(WebView, self).__init__()
        self._url = url

        self._webview = None

    def _startup(self):
        self._impl = Gtk.ScrolledWindow()
        self._impl.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self._webview = WebKit.WebView()

        if self._url:
            self._webview.load_uri(self._url)

        self._impl.add(self._webview)
        self._impl.set_min_content_width(200)
        self._impl.set_min_content_height(200)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        if self._impl:
            self._webview.load_uri(self._url)
