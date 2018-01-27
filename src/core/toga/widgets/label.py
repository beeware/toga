from .base import Widget


class Label(Widget):
    """A text label.

    Args:
        text (str): Text of the label.
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional; normally not needed)
    """

    def __init__(self, text, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a Label
        self._impl = self.factory.Label(interface=self)

        self.text = text

    @property
    def text(self):
        """The text displayed by the label.

        Returns:
            The text displayed by the label.
        """
        return self._text

    @text.setter
    def text(self, value):
        if value is None:
            self._text = ''
        else:
            self._text = str(value)
        self._impl.set_text(value)
        self._impl.rehint()
