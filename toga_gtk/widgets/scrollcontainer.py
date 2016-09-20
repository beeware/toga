from gi.repository import Gtk

from toga.interface import ScrollContainer as ScrollContainerInterface

from .base import WidgetMixin
from ..container import Container


class ScrollContainer(ScrollContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, horizontal=True, vertical=True, content=None):
        super().__init__(id=id, style=style, horizontal=horizontal, vertical=vertical, content=content)
        self._create()

    def create(self):
        self._impl = Gtk.ScrolledWindow()

    def _set_content(self, container, widget):
        self._impl.add_with_viewport(container._impl)

    def _set_app(self, app):
        if self._content:
            self._content.app = app

    def _update_child_layout(self):
        if self._content is not None:
            self._inner_container._update_layout()

    def _set_vertical(self, value):
        self._impl.set_policy(
            Gtk.PolicyType.AUTOMATIC if getattr(self, 'horizontal', True) else Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC if getattr(self, 'vertical', True) else Gtk.PolicyType.NEVER,
        )

    def _set_horizontal(self, value):
        self._impl.set_policy(
            Gtk.PolicyType.AUTOMATIC if getattr(self, 'horizontal', True) else Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC if getattr(self, 'vertical', True) else Gtk.PolicyType.NEVER,
        )
