from toga_web.libs import add_event_listener

from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        super().create()
        self.native.setAttribute("type", "password")
        add_event_listener(self.native.id, "sl-change", self.dom_onchange)

    def dom_onchange(self, event):
        self.interface.on_change(None)

    def is_valid(self):
        self.interface.factory.not_implemented("PasswordInput.is_valid()")
        return True
