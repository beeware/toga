from .base import Widget
from toga.constants import *


class Label(Widget):
    """

    Args:
        text (str): Text of the label.
        id (str): An identifier for this widget.
        style (:class:`colosseum.CSSNode`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
        alignment (int): Alignment of the label, default is left.
            Alignments can be found in `toga.constants
    """

    def __init__(self, text, id=None, style=None, factory=None, alignment=LEFT_ALIGNED):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a Label
        self._impl = self.factory.Label(interface=self)

        self.text = text
        self.alignment = alignment

    @property
    def alignment(self):
        """ The alignment of the label text

        Returns:
            (int) Alignment of the label, default is left.
        """
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        self._impl.set_alignment(value)

    @property
    def text(self):
        """ The label text of the.

        Returns:
            The text of the label as a ``str``.
        """
        return self._text

    @text.setter
    def text(self, value):
        if value is None:
            self._text = ''
        else:
            self._text = str(value)
        self._impl.set_text(self._text)
        self.rehint()
