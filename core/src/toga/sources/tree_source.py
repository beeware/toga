from __future__ import annotations

from collections.abc import Iterator
from typing import Iterable, Mapping, TypeVar

from .base import Source
from .list_source import Row, _find_item

T = TypeVar("T")


class Node(Row[T]):
    _source: TreeSource

    def __init__(self, **data: T):
        """Create a new Node object.

        The keyword arguments specified in the constructor will be converted into
        attributes on the new object.

        When initially constructed, the Node will be a leaf node (i.e., no children,
        and marked unable to have children).

        When any public attributes of the node are modified (i.e., any attribute whose
        name doesn't start with ``_``), the source to which the node belongs will be
        notified.
        """
        super().__init__(**data)
        self._children: list[Node[T]] | None = None
        self._parent: Node[T] | None = None

    def __repr__(self) -> str:
        descriptor = " ".join(
            f"{attr}={getattr(self, attr)!r}"
            for attr in sorted(self.__dict__)
            if not attr.startswith("_")
        )
        if not descriptor:
            descriptor = "(no attributes)"
        if self._children is not None:
            descriptor += f"; {len(self)} children"

        return f"<{'Leaf ' if self._children is None else ''}Node {id(self):x} {descriptor}>"

    ######################################################################
    # Methods required by the TreeSource interface
    ######################################################################

    def __getitem__(self, index: int) -> Node[T]:
        if self._children is None:
            raise ValueError(f"{self} is a leaf node")

        return self._children[index]

    def __delitem__(self, index: int) -> None:
        if self._children is None:
            raise ValueError(f"{self} is a leaf node")

        child = self._children[index]
        del self._children[index]

        # Child isn't part of this source, or a child of this node anymore.
        child._parent = None
        child._source = None

        self._source.notify("remove", parent=self, index=index, item=child)

    def __len__(self) -> int:
        if self.can_have_children():
            return len(self._children)
        else:
            return 0

    def can_have_children(self) -> bool:
        """Can the node have children?

        A value of :any:`True` does not necessarily mean the node *has* any children,
        only that the node is *allowed* to have children. The value of ``len()`` for
        the node indicates the number of actual children.
        """
        return self._children is not None

    ######################################################################
    # Utility methods to make TreeSource more list-like
    ######################################################################

    def __iter__(self) -> Iterator[Node[T]]:
        return iter(self._children or [])

    def __setitem__(self, index: int, data: object) -> None:
        """Set the value of a specific child in the Node.

        :param index: The index of the child to change
        :param data: The data for the updated child. This data will be converted
            into a Node object.
        """
        if self._children is None:
            raise ValueError(f"{self} is a leaf node")

        old_node = self._children[index]
        old_node._parent = None
        old_node._source = None

        node = self._source._create_node(parent=self, data=data)
        self._children[index] = node
        self._source.notify("change", item=node)

    def insert(self, index: int, data: object, children: object = None) -> Node[T]:
        """Insert a node as a child of this node a specific index.

        :param index: The index at which to insert the new child.
        :param data: The data to insert into the Node as a child. This data will be
            converted into a Node object.
        :param children: The data for the children of the new child node.
        :returns: The new added child Node object.
        """
        if self._children is None:
            self._children = []

        if index < 0:
            index = max(len(self) + index, 0)
        else:
            index = min(len(self), index)

        node = self._source._create_node(parent=self, data=data, children=children)
        self._children.insert(index, node)
        self._source.notify("insert", parent=self, index=index, item=node)
        return node

    def append(self, data: object, children: object = None) -> Node[T]:
        """Append a node to the end of the list of children of this node.

        :param data: The data to append as a child of this node. This data will be
            converted into a Node object.
        :param children: The data for the children of the new child node.
        :returns: The new added child Node object.
        """
        return self.insert(len(self), data=data, children=children)

    def remove(self, child: Node[T]) -> None:
        """Remove a child node from this node.

        :param child: The child node to remove from this node.
        """
        # Index will raise ValueError if the node is a leaf
        del self[self.index(child)]

    def index(self, child: Node[T]) -> int:
        """The index of a specific node in children of this node.

        This search uses Node instances, and searches for an *instance* match.
        If two Node instances have the same values, only the Node that is the
        same Python instance will match. To search for values based on equality,
        use :meth:`~toga.sources.Node.find`.

        :param child: The node to find in the children of this node.
        :returns: The index of the node in the children of this node.
        :raises ValueError: If the node cannot be found in children of this node.
        """
        if self._children is None:
            raise ValueError(f"{self} is a leaf node")

        return self._children.index(child)

    def find(self, data: object, start: Node[T] | None = None) -> Node[T]:
        """Find the first item in the child nodes of this node that matches all the
        provided attributes.

        This is a value based search, rather than an instance search. If two Node
        instances have the same values, the first instance that matches will be
        returned. To search for a second instance, provide the first found instance as
        the ``start`` argument. To search for a specific Node instance, use the
        :meth:`~toga.sources.Node.index`.

        :param data: The data to search for. Only the values specified in data will be
            used as matching criteria; if the node contains additional data attributes,
            they won't be considered as part of the match.
        :param start: The instance from which to start the search. Defaults to ``None``,
            indicating that the first match should be returned.
        :return: The matching Node object.
        :raises ValueError: If no match is found.
        :raises ValueError: If the node is a leaf node.
        """
        if self._children is None:
            raise ValueError(f"{self} is a leaf node")

        return _find_item(
            candidates=self._children,
            data=data,
            accessors=self._source._accessors,
            start=start,
            error=f"No child matching {data!r} in {self}",
        )


class TreeSource(Source):
    _roots: list[Node]

    def __init__(self, accessors: Iterable[str], data: object | None = None):
        super().__init__()
        if isinstance(accessors, str) or not hasattr(accessors, "__iter__"):
            raise ValueError("accessors should be a list of attribute names")

        # Copy the list of accessors
        self._accessors = [a for a in accessors]
        if len(self._accessors) == 0:
            raise ValueError("TreeSource must be provided a list of accessors")

        if data is not None:
            self._roots = self._create_nodes(parent=None, value=data)
        else:
            self._roots = []

    ######################################################################
    # Methods required by the TreeSource interface
    ######################################################################

    def __len__(self) -> int:
        return len(self._roots)

    def __getitem__(self, index: int) -> Node:
        return self._roots[index]

    def __delitem__(self, index: int) -> None:
        node = self._roots[index]
        del self._roots[index]
        node._source = None
        self.notify("remove", parent=None, index=index, item=node)

    ######################################################################
    # Factory methods for new nodes
    ######################################################################

    def _create_node(
        self,
        parent: Node | None,
        data: object,
        children: object | None = None,
    ) -> Node:
        if isinstance(data, Mapping):
            node = Node(**data)
        elif hasattr(data, "__iter__") and not isinstance(data, str):
            node = Node(**dict(zip(self._accessors, data)))
        else:
            node = Node(**{self._accessors[0]: data})

        node._parent = parent
        node._source = self

        if children is not None:
            node._children = self._create_nodes(parent=node, value=children)

        return node

    def _create_nodes(self, parent: Node | None, value: object) -> list[Node]:
        if isinstance(value, Mapping):
            return [
                self._create_node(parent=parent, data=data, children=children)
                for data, children in value.items()
            ]
        elif hasattr(value, "__iter__") and not isinstance(value, str):
            return [
                self._create_node(parent=parent, data=item[0], children=item[1])
                for item in value
            ]
        else:
            return [self._create_node(parent=parent, data=value)]

    ######################################################################
    # Utility methods to make TreeSources more list-like
    ######################################################################

    def __setitem__(self, index: int, data: object) -> None:
        """Set the value of a specific root item in the data source.

        :param index: The root item to change
        :param data: The data for the updated item. This data will be converted
            into a Node object.
        """
        old_root = self._roots[index]
        old_root._parent = None
        old_root._source = None

        root = self._create_node(parent=None, data=data)
        self._roots[index] = root
        self.notify("change", item=root)

    def clear(self) -> None:
        """Clear all data from the data source."""
        self._roots = []
        self.notify("clear")

    def insert(self, index: int, data: object, children: object = None) -> Node:
        """Insert a root node into the data source at a specific index.

        If the node is a leaf node, it will be converted into a non-leaf node.

        :param index: The index into the list of children at which to insert the item.
        :param data: The data to insert into the TreeSource. This data will be converted
            into a Node object.
        :param children: The data for the children to insert into the TreeSource.
        :returns: The newly constructed Node object.
        :raises ValueError: If the provided parent is not part of this TreeSource.
        """
        if index < 0:
            index = max(len(self) + index, 0)
        else:
            index = min(len(self), index)

        node = self._create_node(parent=None, data=data, children=children)
        self._roots.insert(index, node)
        node._parent = None
        self.notify("insert", parent=None, index=index, item=node)

        return node

    def append(self, data: object, children: object | None = None) -> Node:
        """Append a root node at the end of the list of children of this source.

        If the node is a leaf node, it will be converted into a non-leaf node.

        :param data: The data to append onto the list of children of the given parent.
            This data will be converted into a Node object.
        :param children: The data for the children to insert into the TreeSource.
        :returns: The newly constructed Node object.
        :raises ValueError: If the provided parent is not part of this TreeSource.
        """
        return self.insert(len(self), data=data, children=children)

    def remove(self, node: Node) -> None:
        """Remove a node from the data source.

        This will also remove the node if it is a descendant of a root node.

        :param node: The node to remove from the data source.
        """
        if node._source != self:
            raise ValueError(f"{node} is not managed by this data source")

        if node._parent is None:
            del self[self.index(node)]
        else:
            node._parent.remove(node)

    def index(self, node: Node) -> int:
        """The index of a specific root node in the data source.

        This search uses Node instances, and searches for an *instance* match.
        If two Node instances have the same values, only the Node that is the
        same Python instance will match. To search for values based on equality,
        use :meth:`~toga.sources.TreeSource.find`.

        :param node: The node to find in the data source.
        :returns: The index of the node in the child list it is a part of.
        :raises ValueError: If the node cannot be found in the data source.
        """
        return self._roots.index(node)

    def find(self, data: object, start: Node | None = None) -> Node:
        """Find the first item in the child nodes of the given node that matches all the
        provided attributes.

        This is a value based search, rather than an instance search. If two Node
        instances have the same values, the first instance that matches will be
        returned. To search for a second instance, provide the first found instance as
        the ``start`` argument. To search for a specific Node instance, use the
        :meth:`~toga.sources.TreeSource.index`.

        :param data: The data to search for. Only the values specified in data will be
            used as matching criteria; if the node contains additional data attributes,
            they won't be considered as part of the match.
        :param start: The instance from which to start the search. Defaults to ``None``,
            indicating that the first match should be returned.
        :return: The matching Node object.
        :raises ValueError: If no match is found.
        :raises ValueError: If the provided parent is not part of this TreeSource.
        """
        return _find_item(
            candidates=self._roots,
            data=data,
            accessors=self._accessors,
            start=start,
            error=f"No root node matching {data!r} in {self}",
        )
