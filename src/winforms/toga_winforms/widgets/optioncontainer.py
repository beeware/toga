from toga.interface import OptionContainer as OptionContainerInterface

from ..container import Container
from ..libs import WinForms
from .base import WidgetMixin
from System import Drawing


class TogaOptionContainer(WinForms.TabControl):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface


class OptionContainer(OptionContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, content=None):
        super(OptionContainer, self).__init__(id=id, style=style, content=content)
        self._create()

    def create(self):
        self._container = self  # TODO Why?
        self._impl = TogaOptionContainer(self)

    def _add_content(self, label, container, widget):
        item = WinForms.TabPage()
        item.Text = label
        item.Size = Drawing.Size(700, 1000)  # TODO test
        item.TabIndex = 0  # TODO remove?
        # TODO Expansion??

        item.Controls.Add(container._impl)
        self._impl.Controls.Add(item)
