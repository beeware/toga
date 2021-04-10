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
