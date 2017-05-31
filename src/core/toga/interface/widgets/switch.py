from .base import Widget


class Switch(Widget):
    """
    Switch widget, a clickable button with two stable states, True (on, checked) and False (off, unchecked)

    :param label:       Text to be shown next to the switch
    :type label:        ``str``

    :param id:          An identifier for this widget.
    :type  id:          ``str``

    :param style:       an optional style object. If no style is provided then a
                        new one will be created for the widget.
    :type style:        :class:`colosseum.CSSNode`

    :param on_toggle:    Function to execute when pressed
    :type on_toggle:     ``callable``

    :param is_on        Current on or off state of the switch
    :type is_on         ``Bool`
    """

    def __init__(self, label, id=None, style=None, on_toggle=None, is_on=False, enabled=True):
        super().__init__(id=id, style=style, label=label, on_toggle=on_toggle, is_on=is_on, enabled=enabled)

    def _configure(self, label, on_toggle, is_on, enabled):
        self.label = label
        self.on_toggle = on_toggle
        self.is_on = is_on
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
        self._set_label(value)
        self.rehint()

    def _set_label(self, value):
        raise NotImplementedError('The inheriting class of {} must define _set_label()'.format(__class__))

    @property
    def on_toggle(self):
        """
        The callable function for when the switch is pressed

        :rtype: ``callable``
        """
        return self._on_toggle

    @on_toggle.setter
    def on_toggle(self, handler):
        self._on_toggle = handler
        self._set_on_toggle(handler)

    def _set_on_toggle(self, value):
        pass

    @property
    def is_on(self):
        """
        :returns: The is_on value

        :rtype: ``Bool``
        """
        return self._get_is_on()

    @is_on.setter
    def is_on(self, value):
        """
        Set the is_on value

        :param value: The new is_on value
        :type  value: ``Bool``
        """
        if value is True:
            self._set_is_on(True)
        elif value is False:
            self._set_is_on(False)

    @property
    def enabled(self):
        """
        :returns: The enabled state of the switch

        :rtype  value: ``Bool``
        """
        return self._get_enabled()

    @enabled.setter
    def enabled(self, value):
        """
        Set the enabled state of the switch

        :param value: The new enabled value
        :type  value: ``Bool``
        """
        if value is True:
            self._set_enabled(True)
        elif value is False:
            self._set_enabled(False)

    def _set_is_on(self, value):
        raise NotImplementedError('The inheriting class of {} must define _set_is_on()'.format(__class__))

    def _get_is_on(self):
        raise NotImplementedError('The inheriting class of {} must define _get_is_on()'.format(__class__))

    def _set_enabled(self, value):
        raise NotImplementedError('The inheriting class of {} must define _set_enabled()'.format(__class__))

    def _get_enabled(self):
        raise NotImplementedError('The inheriting class of {} must define _get_enabled()'.format(__class__))
