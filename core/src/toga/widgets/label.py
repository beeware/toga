from __future__ import annotations

from .base import Widget


class Label(Widget):
    def __init__(
        self,
        text: str,
        id=None,
        style=None,
    ):
        """Create a new text label.

        :param text: Text of the label.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a Label
        self._impl = self.factory.Label(interface=self)

        self.text = text

    def focus(self):
        "No-op; Label cannot accept input focus"
        pass

    @property
    def text(self) -> str:
        """The text displayed by the label.

        ``None``, and the Unicode codepoint U+200B (ZERO WIDTH SPACE), will be
        interpreted and returned as an empty string. Any other object will be
        converted to a string using ``str()``.
        """
        return self._impl.get_text()

    @text.setter
    def text(self, value):
        if value is None or value == "\u200B":
            text = ""
        else:
            text = str(value)

        self._impl.set_text(text)
        self.refresh()
