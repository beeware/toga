from toga_winforms.container import Container
from toga_winforms.libs import WinForms

from .base import Widget


class OptionContainer(Widget):
    def create(self):
        self.native = WinForms.TabControl()

        self.containers = []

    def add_content(self, label, widget):
        item = WinForms.TabPage()
        item.Text = label

        if widget.native is None:
            container = Container()
            container.content = widget
        else:
            container = widget

        self.containers.append((label, container, widget))

        # Enable AutoSize on the container to fill
        # the available space in the OptionContainer.
        container.native.AutoSize = True

        item.Controls.Add(container.native)

        self.native.Controls.Add(item)
