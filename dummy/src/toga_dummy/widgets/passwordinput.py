from ..utils import not_required
from .textinput import TextInput


@not_required  # Testbed coverage is complete for this widget.
class PasswordInput(TextInput):
    def create(self):
        self._action("create PasswordInput")
