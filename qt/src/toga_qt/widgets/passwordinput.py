from PySide6.QtWidgets import QLineEdit

from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        super().create()
        self.native.setEchoMode(QLineEdit.Password)
