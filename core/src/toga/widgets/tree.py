import warnings

from toga.handlers import wrapped_handler
from toga.sources import TreeSource
from toga.sources.accessors import build_accessors

from .base import Widget


class Tree(Widget):
    """Tree Widget.

    :param headings: The list of headings for the interface.
    :param id:  An identifier for this widget.
    :param style: An optional style object. If no style is provided then a new
        one will be created for the widget.
    :param data: The data to display in the widget. Can be an instance of
        :class:`~toga.sources.TreeSource`, a list, dict or tuple with data to
        display in the tree widget, or a class instance which implements the
        interface of :class:`~toga.sources.TreeSource`. Entries can be:

          - any Python object ``value`` with a string representation. This
            string will be shown in the widget. If ``value`` has an attribute
            ``icon``, instance of (:class:`~toga.icons.Icon`), the icon will be
            shown in front of the text.

          - a tuple ``(icon, value)`` where again the string representation of
            ``value`` will be used as text.

    :param accessors: Optional; a list of attributes to access the value in the
        columns. If not given, the headings will be taken.
    :param multiple_select: Boolean; if ``True``, allows for the selection of
        multiple rows. Defaults to ``False``.
    :param on_select: A handler to be invoked when the user selects one or
        multiple rows.
    :param on_double_click: A handler to be invoked when the user double clicks a row.
    """

    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    def __init__(
        self,
        headings,
        id=None,
        style=None,
        data=None,
        accessors=None,
        multiple_select=False,
        on_select=None,
        on_double_click=None,
        factory=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style)
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self.headings = headings
        self._accessors = build_accessors(headings, accessors)
        self._multiple_select = multiple_select
        self._data = None
        self._on_select = None
        self._on_double_click = None

        self._impl = self.factory.Tree(interface=self)
        self.data = data

        self.on_select = on_select
        self.on_double_click = on_double_click

    @property
    def data(self):
        """
        :returns: The data source of the tree
        """
        return self._data

    @data.setter
    def data(self, data):
        """Set the data source of the data.

        :param data: Data source
        :type  data: ``dict`` or ``class``
        """
        if data is None:
            self._data = TreeSource(accessors=self._accessors, data=[])
        elif isinstance(data, (list, tuple, dict)):
            self._data = TreeSource(accessors=self._accessors, data=data)
        else:
            self._data = data

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

    @property
    def multiple_select(self):
        """Does the table allow multiple rows to be selected?"""
        return self._multiple_select

    @property
    def selection(self):
        """The current selection of the table.

        A value of None indicates no selection. If the tree allows
        multiple selection, returns a list of selected data nodes.
        Otherwise, returns a single data node.
        """
        return self._impl.get_selection()

    @property
    def on_select(self):
        """The callable function for when a node on the Tree is selected. The
        provided callback function has to accept two arguments tree
        (:obj:`Tree`) and node (``Node`` or ``None``).

        :rtype: ``callable``
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """Set the function to be executed on node select.

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)

    @property
    def on_double_click(self):
        """The callable function for when a node on the Tree is selected. The
        provided callback function has to accept two arguments tree
        (:obj:`Tree`) and node (``Node`` or ``None``).

        :rtype: ``callable``
        """
        return self._on_double_click

    @on_double_click.setter
    def on_double_click(self, handler):
        """Set the function to be executed on node double click.

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_double_click = wrapped_handler(self, handler)
        self._impl.set_on_double_click(self._on_double_click)
