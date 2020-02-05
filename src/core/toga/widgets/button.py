from .base import Widget
from toga.events import Event


class Button(Widget):
    """A clickable button widget.

    Args:
        label (str): Text to be shown on the button.
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        enabled (bool): Whether or not interaction with the button is possible, defaults to `True`.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """

    def __init__(self, label, id=None, style=None, enabled=True, factory=None, **kwargs):
        super().__init__(id=id, enabled=enabled, style=style, factory=factory, **kwargs)

        # Create a platform specific implementation of a Button
        self._impl = self.factory.Button(interface=self)

        # Set all the properties
        self.label = label

    on_press = Event('Called when the button is pressed')

    @property
    def label(self):
        """
        Returns:
            The button label as a ``str``
        """
        return self._label

    @label.setter
    def label(self, value):
        if value is None:
            self._label = ''
        else:
            self._label = str(value)
        self._impl.set_label(value)
        self._impl.rehint()
