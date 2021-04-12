from typing import Iterable, Union, Dict, List, Any, Optional


from .base import Source
from .list_source import Row


Data = Union[Iterable, Dict[Iterable, 'Data']]


class Node(Row):
    """A node in a :class:`TreeSource`.

    The containing data can be accessed through instance attributes. Children can be
    accessed by indexing into or iterating over the node.

    Examples:

        >>> node = Node(region='United Kingdom', population=67*10**6)
        >>> print(len(node))
        0
        >>> node.insert(0, region='London', population=9*10**6)
        >>> print(len(node))
        1
        >>> print(node[0].region)
        'London'
        >>> print(node[0].population)
        9000000
        :param data: Keyword arguments with data to create the row. Argument names will
            become instance attributes.
    """

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._children = None
        self._parent = None

    ######################################################################
    # Methods required by the TreeSource interface
    ######################################################################

    def __getitem__(self, index: int) -> Any:
        return self._children[index]

    def __len__(self) -> int:
        if self.can_have_children():
            return len(self._children)
        else:
            return 0

    def can_have_children(self) -> bool:
        """Returns whether the node can have children."""
        return self._children is not None

    ######################################################################
    # Utility methods to make TreeSource more dict-like
    ######################################################################

    def __iter__(self) -> Iterable["Node"]:
        return iter(self._children or [])

    def __setitem__(self, index: int, value: Any) -> None:
        node = self._source._create_node(value)
        self._children[index] = node
        self._source._notify("change", item=node)

    def insert(self, index: int, *values: Any, **named: Any) -> "Node":
        """
        Creates and inserts a new child node at the given index from the given data.

        :param index: Index for insertion.
        :param values: An iterable of values to insert. The length must match the length
            of accessors.
        :param named: Keyword arguments with accessor names and corresponding values.
        :return: The created node.
        """
        return self._source.insert(self, index, *values, **named)

    def prepend(self, *values: Any, **named: Any) -> "Node":
        """
        Creates and prepends a new child node from the given data.

        :param values: An iterable of values to insert. The length must match the length
            of accessors.
        :param named: Keyword arguments with accessor names and corresponding values.
        :return: The created node.
        """
        return self._source.prepend(self, *values, **named)

    def append(self, *values: Any, **named: Any) -> "Node":
        """
        Creates and appends a new child node from the given data.

        :param values: An iterable of values to insert. The length must match the length
            of accessors.
        :param named: Keyword arguments with accessor names and corresponding values.
        :return: The created node.
        """
        return self._source.append(self, *values, **named)

    def remove(self, node: "Node") -> "Node":
        """
        Removes the given child node.

        :return: The removed node.
        """
        return self._source.remove(self, node)


class TreeSource(Source):
    """A data source to store a tree of data.

    The :class:`TreeSource` acts like Python list where entries are
    :class:`Node` instances. Data values of each node are accessible as attributes
    of the node and the attribute names are defined by the ``accessor`` argument.

    Listeners can be registered with :meth:`add_listener` and should implement methods
    ``insert``, ``change``, ``remove`` and ``clear`` to react to changes to the data
    source. If the :class:`TreeSource` is set as a data store for a :class:`toga.Tree`,
    the tree will be automatically registered as a listener.

    :param data: The data in the tree. This should be in the form of a dictionary
        where keys are iterables (except for str) that represent the data for each Node
        and values are iterables over their children.
    :param accessors: A list of attribute names for accessing the value in each column
        of the row.

    :Example:

        Data should be provided as a dictionary where the keys represent nodes and the
        values are lists of their child nodes. Nodes can are provided as iterables with
        accessors provided separately:

        >>> data = {
        ...     ('mother', 68): {
        ...         ('son', 32): [('grandchild', 4)],
        ...         ('daughter', 29): [],
        ...     },
        ...     ('father', 70): [('child 1', 17)],
        ... }
        >>> accessors = ['name', 'age']
        >>> source = TreeSource(data, accessors)

        Nodes in the source can be accessed by index:

        >>> node = source[0]
        >>> print(node)
        <Node(name='mother', age=68)>

        Data values can be accessed as row attributes:

        >>> print(node.name)
        'mother'

        Children can be accessed by iterating over a parent:

        >>> for child in node:
        >>>     print(child)
        <Node(name='son', age=32)>
        <Node(name='daughter', age=29)>
    """

    def __init__(self, data: Data, accessors: Iterable[str]) -> None:
        super().__init__()
        self.accessors = list(accessors)
        self._roots = self._create_nodes(data)

    ######################################################################
    # Methods required by the TreeSource interface
    ######################################################################

    def __len__(self) -> int:
        return len(self._roots)

    def __getitem__(self, index: int) -> Node:
        return self._roots[index]

    def can_have_children(self) -> bool:
        """Returns whether this source can have children. Always returns True."""
        return True

    ######################################################################
    # Factory methods for new nodes
    ######################################################################

    def _create_node(
        self,
        data: Union[Dict[str, Any], Iterable],
        children: Optional[Data] = None,
    ) -> Node:
        """Create a Node object from the given data.

        :param data: The type of ``data`` determines how it is handled.
            ``dict``: each key corresponds to a column accessor
            iterables, except ``str`` and ``dict``: each item corresponds to a column
        :param children: Data for children.
        """

        if isinstance(data, dict):
            node = Node(**data)
        elif hasattr(data, "__iter__") and not isinstance(data, str):
            node = Node(**dict(zip(self.accessors, data)))
        else:
            raise ValueError("Invalid data format")

        node._source = self

        if children is not None:
            node._children = []
            for child_node in self._create_nodes(children):
                node._children.append(child_node)
                child_node._parent = node
                child_node._source = self

        return node

    def _create_nodes(self, data: Data) -> List[Node]:
        """Creates a list of Nodes from the data.

        :param data: The source data with the same structure as provided to init.
        """
        if isinstance(data, dict):
            return [
                self._create_node(value, children) for value, children in data.items()
            ]
        else:
            return [self._create_node(value) for value in data]

    ######################################################################
    # Utility methods to make TreeSources more dict-like
    ######################################################################

    def __setitem__(self, index: int, value: Union[Dict[str, Any], Iterable]) -> None:
        root = self._create_node(value)
        self._roots[index] = root
        self._notify("change", item=root)

    def __iter__(self) -> Iterable[Node]:
        return iter(self._roots)

    def clear(self) -> None:
        """Removes all nodes from this source."""
        self._roots = []
        self._notify("clear")

    def insert(self, parent: Optional[Node], index: int, *values: Any, **named: Any) -> Node:
        """
        Create and insert a new node at the given index as a child of ``parent``. The
        data for the new node can be provided either as iterable to populate the fields
        of the node or as keywords arguments with accessors as names.

        :Example:

            >>> data = {
            ...    ('father', 38): [('child 1', 17), ('child 2', 15)],
            ...    ('mother', 42): [('child 1', 17)],
            ... }
            >>> source = TreeSource(data, accessors=['name', 'age'])
            >>> mother = source[1]
            >>> source.insert(mother, 0, name='Kevin', age=7)
            >>> source.insert(mother, 1, ['Justin', 3])
            >>> print(mother)
            <Node(name='Kevin', age=7)>
            <Node(name='Justin', age=3)>
            <Node(name='child 1', age=17)>

        :param parent: Parent node to insert into. If None, the new node will be created
            as a root node.
        :param index: Index relative to parent to insert new node.
        :param values: An iterable of values to insert. The length must match the length
            of accessors.
        :param named: Keyword arguments assigning values to accessor names.
        :return: The created node.
        """
        node = self._create_node(dict(zip(self.accessors, values), **named))

        if parent is None:
            self._roots.insert(index, node)
        else:
            if parent._children is None:
                parent._children = []
            parent._children.insert(index, node)

        node._parent = parent
        self._notify("insert", parent=parent, index=index, item=node)
        return node

    def prepend(self, parent: Node, *values: Any, **named: Any) -> Node:
        """
        Create and prepend a node to a given parent. The syntax is similar to
        :meth:`insert`.

        :param parent: Parent node to prepend to. If None, the new node will be created
            as a root node.
        :param values: An iterable of values to insert. The length must match the length
            of accessors.
        :param named: Keyword arguments assigning values to accessor names.
        :return: The created node.
        """
        return self.insert(parent, 0, *values, **named)

    def append(self, parent: Node, *values: Any, **named: Any) -> Node:
        """
        Create and append a node to a given parent. The syntax is similar to
        :meth:`insert`.

        :param parent: Parent node to append to. If None, the new node will be created
            as a root node.
        :param values: An iterable of values to insert. The length must match the length
            of accessors.
        :param named: Keyword arguments assigning values to accessor names.
        :return: The created node.
        """
        return self.insert(parent, len(parent or self), *values, **named)

    def remove(self, node: Node) -> Node:
        """
        Remove the given node from this :class:`TreeSource`.

        :param node: The node to remove.
        :return: The removed node.
        """
        i = self.index(node)
        parent = node._parent
        if node._parent is None:
            del self._roots[i]
        else:
            del node._parent._children[i]
            # node is not in parent's children so it shouldn't keep a link to parent
            del node._parent

        self._notify("remove", parent=parent, index=i, item=node)
        return node

    def index(self, node: Node) -> int:
        """
        Retrieves the index of a node in the :class:`TreeSource`.

        :param node: A node in the tree source.
        :return: The index of the node.
        """
        if node._parent:
            return node._parent._children.index(node)
        else:
            return self._roots.index(node)
