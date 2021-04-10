import warnings

from toga.handlers import wrapped_handler
from toga.sources import TreeSource
from toga.sources.accessors import to_accessor, build_accessors
from toga.widgets.table import Column

from .base import Widget


class Tree(Widget):
    """Tree Widget

    :param columns: Can be a list of titles to generate columns or a list of
        :class:`Column` instances.
    :param accessors: Optional; a list of attributes to access the value in the
        columns. If not given, the headings will be taken.
    :param id:  An identifier for this widget.
    :param style: An optional style object. If no style is provided then a new
        one will be created for the widget.
    :param data: The data to display in the widget. Can be an instance of
        :class:`toga.sources.TreeSource`, a list, or tuple with data to
        display in the tree widget, or a class instance which implements the
        interface of :class:`toga.sources.TreeSource`.
    :param multiple_select: Boolean; if ``True``, allows for the selection of
        multiple rows. Defaults to ``False``.
    :param on_select: A handler to be invoked when the user selects one or
        multiple rows.
    :param on_double_click: A handler to be invoked when the user double clicks a row.
    :param factory:: A python module that is capable to return a implementation
        of this class with the same name. (optional; used only for testing)

    Examples:

        Lets prepare a data source first.

        >>> data = {
        >>>    ('father', 38): [('child 1', 17), ('child 1', 15)],
        >>>    ('mother', 42): [('child 1', 17)],
        >>> }
        >>> accessors = ['name', 'age']
        >>> tree_source = TreeSource(data, accessors)

        Columns can be provided in several forms.
        As a list of column titles which will be matched against accessors in the data:

        >>> columns = ['Name', 'Age']

        As ``Column`` instances with column properties assigned to data accessors:

        >>> columns = [
        >>>     Tree.Column(title='Name', text='name'),
        >>>     Tree.Column(title='Age', text='age'),
        >>> ]

        Now we can create our Table:

        >>> table = Tree(columns=columns, data=tree_source)
    """

    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    Column = Column

    def __init__(
        self,
        columns=None,
        headings=None,
        accessors=None,
        id=None,
        style=None,
        data=None,
        multiple_select=False,
        on_select=None,
        on_double_click=None,
        factory=None,
    ):
        super().__init__(id=id, style=style, factory=factory)

        # backward compatibility
        if not columns:
            warnings.warn(
                "Future versions will require a columns argument", DeprecationWarning
            )

        if headings is not None:
            warnings.warn(
                "'headings' and 'accessors' are deprecated and will be removed in a "
                "future version. Use 'columns' instead.", DeprecationWarning
            )
            accessors = build_accessors(headings, accessors)
            columns = [Tree.Column(title=h, text=a) for h, a in zip(headings, accessors)]

        if not (columns or headings):
            raise ValueError("Must provide columns or headers for table")

        self._columns = []
        for col_index, col in enumerate(columns):
            if isinstance(col, Tree.Column):
                self._columns.append(col)
            elif isinstance(col, str):
                title = col
                accessor = to_accessor(title)
                self._columns.append(Tree.Column(title, text=accessor, factory=self.factory))
            else:
                raise ValueError("Column must be str or Column instance")

        self._accessors = [col.text for col in self._columns]  # backward compatibility

        self._multiple_select = multiple_select
        self._data = TreeSource([], [])
        self._on_select = None
        self._on_double_click = None

        self._impl = self.factory.Tree(interface=self)
        self.data = data
        self.on_select = on_select
        self.on_double_click = on_double_click

    @property
    def columns(self):
        return self._columns

    @property
    def data(self):
        """
        The data source of the widget. It accepts table data in the form of
        :obj:`TreeSource`

        :returns: The data source of the tree
        :rtype: :class:`toga.sources.TreeSource`
        """
        return self._data

    @data.setter
    def data(self, data):
        if data is None:
            self._data = TreeSource([], [])
        elif isinstance(data, (list, tuple)):
            warnings.warn(
                "Future versions will only accept a TreeSource instance or None",
                DeprecationWarning
            )
            self._data = TreeSource(data=data, accessors=self._accessors)
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

        A value of None indicates no selection.
        If the tree allows multiple selection, returns a list of
        selected data nodes. Otherwise, returns a single data node.
        """
        return self._impl.get_selection()

    @property
    def on_select(self):
        """
        The callable function for when a node on the Tree is selected. The provided
        callback function has to accept two arguments tree (:obj:`Tree`) and node
        (``Node`` or ``None``).

        :rtype: ``callable``
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """
        Set the function to be executed on node select

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)

    @property
    def on_double_click(self):
        """
        The callable function for when a node on the Tree is selected. The provided
        callback function has to accept two arguments tree (:obj:`Tree`) and node
        (``Node`` or ``None``).

        :rtype: ``callable``
        """
        return self._on_double_click

    @on_double_click.setter
    def on_double_click(self, handler):
        """
        Set the function to be executed on node double click

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_double_click = wrapped_handler(self, handler)
        self._impl.set_on_double_click(self._on_double_click)
