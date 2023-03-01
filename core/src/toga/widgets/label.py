from .base import Widget


class Label(Widget):
    def __init__(
        self,
        text,
        id=None,
        style=None,
    ):
        """A text label.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param text: Text of the label.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a Label
        self._impl = self.factory.Label(interface=self)

        self.text = text

    @property
    def text(self):
        """The text displayed by the label."""
        return self._text

    @text.setter
    def text(self, value):
        if value is None:
            self._text = ""
        else:
            self._text = str(value)

        self._impl.set_text(value)
        self.refresh()
