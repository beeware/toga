from toga.handlers import wrapped_handler

from .base import Widget


class Checkable(Widget):
    """A widget to depict user boolean choice

    Args:
        id(str): An identifier for this widget
        initial(bool): The Initial option of the checkable, defaults to `False`.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
        """


    def __init__(self, initial=False, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.Switch(interface=self)

        #check if convention is prefered over documentation
        #self.initial = initial
        #self.is_checked = initial
        self.is_checked = initial



    @property
    def on_checked(self):
        """
        The callable function when the checkable is checked

        Returns:
             The ``callable`` on_checked function.
        """
        return self._on_checked

    @on_checked.setter
    def on_checked(self, handler):
        self._on_checked = wrapped_handler(self, handler)
        self._impl.set_on_checked(self._on_checked)
        ## Check if I should be implementing those or they are already present

    @property
    def is_checked(self):
        """ Checkable On/Off state.

        Returns:
            ``True`` if on and ``False`` if the switch is off."""
        return self._impl.get_is_checked()

    @is_checked.setter
    def is_checked(self,value):
        if value is True:
            self._impl.set_is_checked(True)
        if value is False:
            self._impl.set_is_checked(False)
