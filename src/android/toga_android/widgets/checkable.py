from .base import Widget

class TogaCheckable(extends=android.widget.Checkable):
    #let me do it later


class Checkable(Widget):
    def create(self):
        self.native = TogaCheckable(self.app._impl,self.interface)

    def set_checked(self,checked):
        self.checked = checked

    def is_checked(self):
        return self.checked

    def toggle(self):
        self.checked = not self.checked

