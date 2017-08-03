from .base import Widget


class Button(Widget):
    """
    Button widget, a clickable button

    :param label:       Text to be shown on the button
    :type label:        ``str``

    :param id:          An identifier for this widget.
    :type  id:          ``str``

    :param style:       an optional style object. If no style is provided then a
                        new one will be created for the widget.
    :type style:        :class:`colosseum.CSSNode`

    :param factory:     an optional factory object. If no factory is provided then a
                        new one will be created for the widget based on the current
                        platform.
    :type factory:      A Toga platform factory

    :param on_press:    Function to execute when pressed
    :type on_press:     ``callable``
    """

    def __init__(self, label, id=None, style=None, factory=None, on_press=None, enabled=True):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a Button
        self._impl = self.factory.Button(interface=self)

        # Set all the properties
        self.label = label
        self.on_press = on_press
        self.enabled = enabled

    @property
    def label(self):
        """
        :returns: The label value
        :rtype: ``str``
        """
        return self._label

    @label.setter
    def label(self, value):
        """
        Set the label value

        :param value: The new label value
        :type  value: ``str``
        """
        if value is None:
            self._label = ''
        else:
            self._label = str(value)
        self._impl.set_label(str(value))

    @property
    def on_press(self):
        """
        The callable function for when the button is pressed

        :rtype: ``callable``
        """
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        """
        Set the function to be executed on button press.

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_press = handler
        self._impl.set_on_press(handler)

    def _set_on_press(self, value):
        pass

    @property
    def enabled(self):
        """
        Indicates whether the button can be pressed by the user.

        :returns:   Button status. Default is True.
        :rtype:     ``Bool`
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """
        Set if the button can be pressed by the user.

        :param value:   Enabled state for button
        :type value:    ``Bool``
        """
        if value is None:
            self._enabled = True
        else:
            self._enabled = value
        self._impl.set_enabled(self._enabled)
