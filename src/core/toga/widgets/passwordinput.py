from .textinput import TextInput


class PasswordInput(TextInput):
    """ This widgets behaves like a TextInput but does not reveal what text is entered.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
        initial (str): The initial text that is displayed before the user inputs anything.
        placeholder (str): The text that is displayed if no input text is present.
        readonly (bool): Whether a user can write into the text input, defaults to `False`.
    """
    MIN_WIDTH = 100

    def __init__(self, id=None, style=None, factory=None,
                initial=None, placeholder=None, readonly=False, on_change=None):
        super(PasswordInput, self).__init__(
            id=id,
            style=style,
            factory=factory,
            initial=initial,
            placeholder=placeholder,
            readonly=readonly,
            on_change=on_change
        )

    def _initiate_implementation(self):
        self._impl = self.factory.PasswordInput(interface=self)
