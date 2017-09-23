from toga.interface import OptionContainer as OptionContainerInterface

from .base import WidgetMixin
from ..container import Container
from ..libs import WinForms


class OptionContainer(OptionContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, content=None):
        super(OptionContainer, self).__init__(id=id, style=style, content=content)
        self._create()

    def create(self):
        self._container = self
        self._impl = WinForms.TabControl()

    def _add_content(self, label, container, widget):
        item = WinForms.TabPage()
        item.Text = label

        # Enable AutoSize on the container to fill
        # the available space in the OptionContainer.
        container._impl.AutoSize = True

        item.Controls.Add(container._impl)

        self._impl.Controls.Add(item)
