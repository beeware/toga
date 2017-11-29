from gi.repository import Gtk

from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        self.native = Gtk.Entry()
        self.native.interface = self.interface
        self.native.set_visibility(False)
        self.native.connect('show', lambda event: self.rehint())
