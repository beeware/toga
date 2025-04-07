from toga_web.libs import create_proxy

from .textinput import TextInput


class DateInput(TextInput):
    def create(self):
        super().create()
        self.native.setAttribute("type", "date")
        self.native.addEventListener("sl-change", create_proxy(self.dom_onchange))

    def dom_onchange(self, event):
        self.interface.on_change(None)

    def is_valid(self):
        self.interface.factory.not_implemented("DateInput.is_valid()")
        return True
