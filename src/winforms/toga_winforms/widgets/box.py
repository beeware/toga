from toga_winforms.libs import WinForms

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()
