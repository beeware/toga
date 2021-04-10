import enum
from toga.handlers import wrapped_handler
from toga.style import Pack

from ..base import Widget
from ...icons import Icon


class Column(Widget):

    def __init__(
        self,
        title,
        text=None,
        icon=None,
        checked_state=None,
        editable=True,
        on_change=None,
        on_toggle=None,
        id=None,
        style=None,
        factory=None,
    ):
        """
        A column for a toga.Table or toga.Tree.

        Args:
            title (str): Column title.
            text (str): Name of attribute in data source to be used as cell text. The
                corresponding data source value should be a string.
            icon (str): Name of attribute in data source to be used as cell icon. The
                corresponding data source value should be a toga.Icon.
            checked_state: Name of attribute in data source to be used as checked state.
                The corresponding data source value should be a boolean.
            editable (bool): Whether the column is editable / will change the data source.
            on_change (``callable``): Function to execute when text is changed. Will be
                called with the arguments (column, node, new_text).
            on_toggle (``callable``): Function to execute when checkbox is changed. Will
                be called with the arguments (column, node, checked_state).
            id (str): An identifier for this widget.
            style (:obj:`Style`): An optional style object.
                If no style is provided then a new one will be created for the widget.
            factory (:obj:`module`): A Python module that is capable to return an
                implementation of this class with the same name. (optional & normally
                not needed)
        """
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.Column(interface=self)

        self.title = title
        self.text = text
        self.icon = icon
        self.checked_state = checked_state
        self.editable = editable
        self.on_change = on_change
        self.on_toggle = on_toggle
        self.style = style or Pack()

    def get_data_for_node(self, node, role):
        try:
            accessor = getattr(self, role)
        except AttributeError:
            raise ValueError(f"Column has no '{role}' data")

        if not accessor:
            return None

        value = getattr(node, accessor, None)

        # convert value to expected type

        if role == "text":
            value = str(value)
        elif role == "icon":
            if isinstance(value, str):
                value = Icon(value)
            elif not isinstance(value, Icon):
                raise ValueError(f"Don't know how to convert {value} to Icon ")
        elif role == "checked_state":
            value = bool(value)

        return value

    def set_data_for_node(self, node, role, value):
        try:
            accessor = getattr(self, role)
        except AttributeError:
            raise ValueError(f"Column has no '{role}' data")

        if accessor is not None:
            setattr(node, accessor, value)

    @property
    def title(self):
        """The column title.

        Returns:
            The column title as ``str``.
        """
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self._impl.set_title(value)

    @property
    def editable(self):
        """Whether the column values are editable

        Returns:
            Editable as ``bool``.
        """
        return self._editable

    @editable.setter
    def editable(self, value):
        self._editable = value
        self._impl.set_editable(value)

    @property
    def on_change(self):
        """The handler to invoke when the text changes

        Returns:
            The function that is called on a text change.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)
        self._impl.set_on_change(self._on_change)

    @property
    def on_toggle(self):
        """The callable function for when the switch is pressed

        Returns:
            The function that is called on a state change.
        """
        return self._on_toggle

    @on_toggle.setter
    def on_toggle(self, handler):
        self._on_toggle = wrapped_handler(self, handler)
        self._impl.set_on_toggle(self._on_toggle)
