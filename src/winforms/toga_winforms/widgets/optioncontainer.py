from toga.interface import OptionContainer as OptionContainerInterface

from ..container import Container
from ..libs import WinForms
from .base import WidgetMixin
from System import Drawing


class OptionContainer(OptionContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, content=None):
        super(OptionContainer, self).__init__(id=id, style=style, content=content)
        self._create()

    def create(self):
        self._container = self  # TODO Why?
        self._impl = WinForms.TabControl()

    def _add_content(self, label, container, widget):
        item = WinForms.TabPage()
        item.Text = label
        item.Controls.Add(container._impl)

        self._impl.Controls.Add(item)

        # item.Size = Drawing.Size(700, 1000)
        # TODO Expansion??? https://stackoverflow.com/a/7380999

        # container._impl.Width = item.Width
        # container._impl.Height = item.Height
        # container._impl.Location = Drawing.Point(container._impl.Location.X, container._impl.Location.Y)
        container._impl.Anchor = WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
