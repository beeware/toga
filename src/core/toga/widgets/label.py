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
        wrap: Wrapping mode: see :attr:`wrap` for details.
    """

    def __init__(self, text, id=None, style=None, factory=None, wrap=None):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a Label
        self._impl = self.factory.Label(interface=self)

        self.text = text
        self.wrap = wrap

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
            value = ''
        else:
            value = str(value)
        self._text = value

        if getattr(self, "_wrap", None) is None:
            value = value.replace("\n", " ")
        self._impl.set_text(value)
        self._impl.rehint()

    @property
    def wrap(self):
        """Wrapping mode.

        * ``None`` (default): Text is displayed on a single line. Any newlines will appear
          as spaces.
        * ``'line'``: Newlines are preserved, but word-wrapping is disabled.
        """
        return self._wrap

    @wrap.setter
    def wrap(self, value):
        CHOICES = [None, "line"]
        if value not in CHOICES:
            raise ValueError(f"wrap must be one of {CHOICES}")
        self._wrap = value
        self.text = self.text  # Adjust newlines.
