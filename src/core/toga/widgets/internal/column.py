import toga
from toga.style import Pack
from toga.widgets.base import Widget


class Column(Widget):

    def __init__(
        self,
        title,
        text=None,
        icon=None,
        checked_state=None,
        editable=True,
        text_fallback='',
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
            text_fallback (str): String to show when the data source does not provide a value.
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
        self._text_fallback = text_fallback
        self.style = style or Pack()

    def get_data_for_node(self, node, role):
        """
        Returns the data for this column for the given node. If this column does not
        provide data for the requested role, return ``None``. If the data source does
        not provide the data, return a reasonable fallback.

        Args:
            node (``Node`` or ``Row``): A Node in a TreeSource or a Row in a ListSource
                that holds the data for this row.
            role (str): The type of data to query. Can be "text", "icon" or "checked_state".
        """
        try:
            accessor = getattr(self, role)
        except AttributeError:
            raise ValueError(f"Column has no '{role}' data")

        # Return None if this column does not provide data for the
        # requested role.
        if accessor is None:
            return None

        # Get data for role from our data source. Fall back to default if not
        # available.
        try:
            value = getattr(node, accessor)
        except AttributeError:
            return self._fallback_data(role)

        # Convert value to expected type.
        if role == "text":
            value = str(value)
        elif role == "icon":
            if isinstance(value, str):
                value = toga.Icon(value)
            elif not isinstance(value, toga.Icon):
                raise ValueError(f"Don't know how to convert {value} to Icon ")
        elif role == "checked_state":
            value = int(value)

        return value

    def _fallback_data(self, role):
        if role == "text":
            return self._text_fallback
        elif role == "icon":
            return toga.Icon.TOGA_ICON
        else:
            return None

    def set_data_for_node(self, node, role, value):
        """
        Sets the data of the given node from column data. This is used by implementations
        to update the data source on user edits of the column data.

        Args:
            node (``Node`` or ``Row``): A Node in a TreeSource or a Row in a ListSource
                that holds the data for this row.
            role (str): The type of data to query. Can be "text", "icon" or "checked_state".
            value: The new value of the colum data.
        """
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
