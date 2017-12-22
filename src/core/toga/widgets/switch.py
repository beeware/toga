from toga.handlers import wrapped_handler

from .base import Widget


class Switch(Widget):
    """ Switch widget, a clickable button with two stable states, True (on, checked) and False (off, unchecked)

    Args:
        label (str): Text to be shown next to the switch.
        id (str): AN identifier for this widget.
        style (:obj:`Style`): An optional style object.
            If no style is provided then a new one will be created for the widget.
        on_toggle (``callable``): Function to execute when pressed.
        is_on (bool): Current on or off state of the switch.
        enabled (bool): Whether or not interaction with the button is possible, defaults to `True`.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """

    def __init__(self, label, id=None, style=None, on_toggle=None, is_on=False, enabled=True, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.Switch(interface=self)

        self.label = label
        self.on_toggle = on_toggle
        self.is_on = is_on
        self.enabled = enabled

    @property
    def label(self):
        """ Accompanying text label of the Switch.

        Returns:
            The label text of the widget as a ``str``.
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

    @property
    def on_toggle(self):
        """ The callable function for when the switch is pressed

        Returns:
            The ``callable`` on_toggle function.
        """
        return self._on_toggle

    @on_toggle.setter
    def on_toggle(self, handler):
        self._on_toggle = wrapped_handler(self, handler)
        self._impl.set_on_toggle(self._on_toggle)

    @property
    def is_on(self):
        """ Button Off/On state.

        Returns:
            ``True`` if on and ``False`` if the switch is off.
        """
        return self._impl.get_is_on()

    @is_on.setter
    def is_on(self, value):
        if value is True:
            self._impl.set_is_on(True)
        elif value is False:
            self._impl.set_is_on(False)
