from toga.interface import OptionContainer as OptionContainerInterface

from src.android.toga_android.widgets.base import WidgetMixin
from ..libs import WinForms
from System import Drawing


class TogaOptionContainer(WinForms.TabControl):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface


class OptionContainer(OptionContainerInterface, WidgetMixin):
    def __init__(self, id=None, style=None, content=None):
        super(OptionContainer, self).__init__(id=id, style=style, content=content)
        self._create()

    def create(self):
        self._container = self  # TODO Why?
        self._impl = TogaOptionContainer(self)

    def _add_content(self, label, container, widget):
        tabPage1 = WinForms.TabPage()
        tabPage1.Text = label
        tabPage1.Size = Drawing.Size(256, 214)  # TODO test
        tabPage1.TabIndex = 0  # TODO remove?
        self._impl.Controls.Add(tabPage1)
        tabPage1.Controls.Add(container._impl)
