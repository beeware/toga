import enum

import toga
from toga.style import Pack
from toga.widgets.base import Widget


class DataRole(enum.Enum):
    Text = "text_accessor"
    Icon = "icon_accessor"
    CheckedState = "checked_state_accessor"


class Column(Widget):

    def __init__(
        self,
        title,
        text_accessor=None,
        icon_accessor=None,
        checked_state_accessor=None,
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
            text_accessor (str): Name of attribute in data source to be used as cell text.
                The corresponding data source value should be a string.
            icon_accessor (str): Name of attribute in data source to be used as cell icon.
                The corresponding data source value should be a toga.Icon.
            checked_state_accessor: Name of attribute in data source to be used as checked
                state. The corresponding data source value should be an int or boolean.
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
        self._accessors = {
            DataRole.Text: text_accessor,
            DataRole.Icon: icon_accessor,
            DataRole.CheckedState: checked_state_accessor
        }
        self.editable = editable
        self._text_fallback = text_fallback
        self.style = style or Pack()

    @property
    def text_accessor(self):
        return self._accessors[DataRole.Text]

    @text_accessor.setter
    def text_accessor(self, value):
        self._accessors[DataRole.Text] = value

    @property
    def icon_accessor(self):
        return self._accessors[DataRole.Icon]

    @icon_accessor.setter
    def icon_accessor(self, value):
        self._accessors[DataRole.Icon] = value

    @property
    def checked_state_accessor(self):
        return self._accessors[DataRole.CheckedState]

    @checked_state_accessor.setter
    def checked_state_accessor(self, value):
        self._accessors[DataRole.CheckedState] = value

    def get_data_for_node(self, node, role):
        """
        Returns the data for this column for the given node. If this column does not
        provide data for the requested role, return ``None``. If the data source does
        not provide the data, return a reasonable fallback.

        Args:
            node (``Node`` or ``Row``): A Node in a TreeSource or a Row in a ListSource
                that holds the data for this row.
            role (``DataRole``): The type of data to query.

        Returns:
            string if role is Role.Text
            toga.Icon if role is Role.Icon
            int if role is Role.CheckedState
        """
        accessor = self._accessors[role]

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
        if role is DataRole.Text:
            value = str(value)
        elif role is DataRole.Icon:
            if not isinstance(value, toga.Icon):
                value = toga.Icon(value)
        elif role is DataRole.CheckedState:
            value = int(value)

        return value

    def _fallback_data(self, role):
        if role is DataRole.Text:
            return self._text_fallback
        elif role is DataRole.Icon:
            return toga.Icon.TOGA_ICON
        else:
            return None

    def set_data_for_node(self, node, role, value):
        """
        Sets the data of the given node from column data. This is used by implementations
        to update the data source on user edits of the column data. Try to cast value
        back to the original type found in the source.

        Args:
            node (``Node`` or ``Row``): A Node in a TreeSource or a Row in a ListSource
                that holds the data for this row.
            role (``DataRole``): The type of data to set.
            value: The new value of the colum data.
        """
        if not self.editable:
            raise RuntimeError("Column is not editable")

        accessor = self._accessors[role]
        if accessor is not None:
            old_value = getattr(node, accessor)
            # Try to cast new value to original type.
            new_value = type(old_value)(value)
            # Use __setattr__ to trigger notification service.
            node.__setattr__(accessor, new_value)

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
