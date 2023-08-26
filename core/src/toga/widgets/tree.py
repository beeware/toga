from __future__ import annotations

import warnings
from typing import Any

from toga.handlers import wrapped_handler
from toga.sources import Node, Source, TreeSource
from toga.sources.accessors import build_accessors, to_accessor

from .base import Widget


class Tree(Widget):
    def __init__(
        self,
        headings: list[str] | None = None,
        id=None,
        style=None,
        data: Any = None,
        accessors: list[str] | None = None,
        multiple_select: bool = False,
        on_select: callable | None = None,
        on_activate: callable | None = None,
        missing_value: str = "",
        on_double_click=None,  # DEPRECATED
    ):
        """Create a new Tree Widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param headings: The list of headings for the tree. A value of :any:`None`
            can be used to specify a tree without headings. Individual headings cannot
            include newline characters; any text after a newline will be ignored
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param data: The data to be displayed on the tree. Can be a list of values or a
            TreeSource. See the definition of the :attr:`data` property for details on
            how data can be specified and used.
        :param accessors: A list of names, with same length as :attr:`headings`, that
            describes the attributes of the data source that will be used to populate
            each column. If unspecified, accessors will be automatically derived from
            the tree headings.
        :param multiple_select: Does the tree allow multiple selection?
        :param on_select: Initial :any:`on_select` handler.
        :param on_activate: Initial :any:`on_activate` handler.
        :param missing_value: The string that will be used to populate a cell when a
            data source doesn't provided a value for a given attribute.
        :param on_double_click: **DEPRECATED**; use :attr:`on_activate`.
        """
        super().__init__(id=id, style=style)

        ######################################################################
        # 2023-06: Backwards compatibility
        ######################################################################
        if on_double_click:
            if on_activate:
                raise ValueError("Cannot specify both on_double_click and on_activate")
            else:
                warnings.warn(
                    "Tree.on_double_click has been renamed Tree.on_activate.",
                    DeprecationWarning,
                )
                on_activate = on_double_click
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        if headings is not None:
            self._headings = [heading.split("\n")[0] for heading in headings]
            self._accessors = build_accessors(self._headings, accessors)
        elif accessors is not None:
            self._headings = None
            self._accessors = accessors
        else:
            raise ValueError(
                "Cannot create a tree without either headings or accessors"
            )
        self._multiple_select = multiple_select
        self._missing_value = missing_value or ""

        # Prime some properties that need to exist before the tree is created.
        self.on_select = None
        self.on_activate = None
        self._data = None

        self._impl = self.factory.Tree(interface=self)
        self.data = data

        self.on_select = on_select
        self.on_activate = on_activate

    @property
    def enabled(self) -> bool:
        """Is the widget currently enabled? i.e., can the user interact with the widget?
        Tree widgets cannot be disabled; this property will always return True; any
        attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value):
        pass

    def focus(self):
        "No-op; Tree cannot accept input focus"
        pass

    @property
    def data(self) -> TreeSource:
        """The data to display in the tree, as a TreeSource.

        When specifying data:

        * A TreeSource will be used as-is

        * A value of None is turned into an empty TreeSource.

        * A dictionary will be converted so that the keys of the dictionary are
          converted into Nodes, and the values are processed recursively as child nodes.

        * Any iterable object (except a string). Each value in the iterable will be
          treated as a 2-item tuple, with first item being data for the parent Node, and
          the second item being processed recursively as child nodes.

        * Any other object will be converted into a list containing a single node with
          no children.

        When converting individual values into Nodes:

        * If the value is a dictionary, the keys of the dictionary will become the
          attributes of the Node.

        * All other values will be converted into a Node with attributes matching the
          ``accessors`` provided at time of construction (or the ``accessors`` that were
          derived from the ``headings`` that were provided at construction).

          If the value is a string, or any other a non-iterable object, the Node will
          have a single attribute matching the first accessor.

          If the value is a list, tuple, or any other iterable, values in the iterable
          will be mapped in order to the accessors.

        """
        return self._data

    @data.setter
    def data(self, data: Any):
        if data is None:
            self._data = TreeSource(accessors=self._accessors, data=[])
        elif isinstance(data, Source):
            self._data = data
        else:
            self._data = TreeSource(accessors=self._accessors, data=data)

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

    @property
    def multiple_select(self) -> bool:
        """Does the tree allow multiple rows to be selected?"""
        return self._multiple_select

    @property
    def selection(self) -> list[Node] | Node | None:
        """The current selection of the tree.

        If multiple selection is enabled, returns a list of Tree objects from the data
        source matching the current selection. An empty list is returned if no rows are
        selected.

        If multiple selection is *not* enabled, returns the selected Node object, or
        :any:`None` if no row is currently selected.
        """
        return self._impl.get_selection()

    def expand(self, node: Node | None = None):
        """Expand the specified node of the tree.

        If no node is provided, all nodes of the tree will be expanded.

        If the provided node is a leaf node, or the node is already expanded, this is a
        no-op.

        If a node is specified, the children of that node will not be automatically
        expanded.

        :param node: The node to expand
        """
        if node is None:
            self._impl.expand_all()
        else:
            self._impl.expand_node(node)

    def collapse(self, node: Node | None = None):
        """Expand the specified node of the tree.

        If no node is provided, all nodes of the tree will be expanded.

        If the provided node is a leaf node, or the node is already collapsed,
        this is a no-op.

        :param node: The node to collapse
        """
        if node is None:
            self._impl.collapse_all()
        else:
            self._impl.collapse_node(node)

    def append_column(self, heading: str, accessor: str | None = None):
        """Append a column to the end of the tree.

        :param heading: The heading for the new column.
        :param accessor: The accessor to use on the data source when populating
            the tree. If not specified, an accessor will be derived from the
            heading.
        """
        self.insert_column(len(self._accessors), heading, accessor=accessor)

    def insert_column(
        self,
        index: int,
        heading: str | None,
        accessor: str | None = None,
    ):
        """Insert an additional column into the tree.

        :param index: The index at which to insert the column, or the accessor of the
            column before which the column should be inserted.
        :param heading: The heading for the new column. If the tree doesn't have
            headings, the value will be ignored.
        :param accessor: The accessor to use on the data source when populating the
            tree. If not specified, an accessor will be derived from the heading. An
            accessor *must* be specified if the tree doesn't have headings.
        """
        if self._headings is None:
            if accessor is None:
                raise ValueError("Must specify an accessor on a tree without headings")
            heading = None
        elif not accessor:
            accessor = to_accessor(heading)

        if isinstance(index, str):
            index = self._accessors.index(index)
        else:
            # Re-interpret negative indices, and clip indices outside valid range.
            if index < 0:
                index = max(len(self._accessors) + index, 0)
            else:
                index = min(len(self._accessors), index)

        if self._headings is not None:
            self._headings.insert(index, heading)
        self._accessors.insert(index, accessor)

        self._impl.insert_column(index, heading, accessor)

    def remove_column(self, column: int | str):
        """Remove a tree column.

        :param column: The index of the column to remove, or the accessor of the column
            to remove.
        """
        if isinstance(column, str):
            # Column is a string; use as-is
            index = self._accessors.index(column)
        else:
            if column < 0:
                index = len(self._accessors) + column
            else:
                index = column

        # Remove column
        if self._headings is not None:
            del self._headings[index]
        del self._accessors[index]
        self._impl.remove_column(index)

    @property
    def headings(self) -> list[str]:
        """The column headings for the tree"""
        return self._headings

    @property
    def accessors(self) -> list[str]:
        """The accessors used to populate the tree"""
        return self._accessors

    @property
    def missing_value(self) -> str:
        """The value that will be used when a data row doesn't provide an value for an
        attribute.
        """
        return self._missing_value

    @property
    def on_select(self) -> callable:
        """The callback function that is invoked when a row of the tree is selected."""
        return self._on_select

    @on_select.setter
    def on_select(self, handler: callable):
        self._on_select = wrapped_handler(self, handler)

    @property
    def on_activate(self) -> callable:
        """The callback function that is invoked when a row of the tree is activated,
        usually with a double click or similar action."""
        return self._on_activate

    @on_activate.setter
    def on_activate(self, handler):
        self._on_activate = wrapped_handler(self, handler)

    ######################################################################
    # 2023-06: Backwards compatibility
    ######################################################################

    @property
    def on_double_click(self):
        """**DEPRECATED**: Use ``on_activate``"""
        warnings.warn(
            "Tree.on_double_click has been renamed Tree.on_activate.",
            DeprecationWarning,
        )
        return self.on_activate

    @on_double_click.setter
    def on_double_click(self, handler):
        warnings.warn(
            "Tree.on_double_click has been renamed Tree.on_activate.",
            DeprecationWarning,
        )
        self.on_activate = handler
