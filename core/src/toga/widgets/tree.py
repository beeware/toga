from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Literal, Protocol

import toga
from toga.handlers import wrapped_handler
from toga.sources import Node, Source, TreeSource, TreeSourceT
from toga.sources.columns import AccessorColumn, ColumnT
from toga.style import Pack

from .base import Widget


class OnSelectHandler(Protocol):
    def __call__(self, widget: Tree, **kwargs: Any) -> None:
        """A handler to invoke when the tree is selected.

        :param widget: The Tree that was selected.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class OnActivateHandler(Protocol):
    def __call__(self, widget: Tree, **kwargs: Any) -> None:
        """A handler to invoke when the tree is activated.

        :param widget: The Tree that was activated.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class Tree(Widget):
    def __init__(
        self,
        headings: Iterable[str] | None = None,
        id: str | None = None,
        style: Pack | None = None,
        data: TreeSourceT | object | None = None,
        accessors: Iterable[str] | None = None,
        multiple_select: bool = False,
        on_select: toga.widgets.tree.OnSelectHandler | None = None,
        on_activate: toga.widgets.tree.OnActivateHandler | None = None,
        missing_value: str = "",
        **kwargs,
    ):
        """Create a new Tree widget.

        :param headings: The column headings for the tree. Headings can only contain one
            line; any text after a newline will be ignored.

            A value of [`None`][] will produce a table without headings.
            However, if you do this, you *must* give a list of accessors.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param data: Initial [`data`][toga.Tree.data] to be displayed in the tree.

        :param accessors: Defines the attributes of the data source that will be used to
            populate each column. Must be either:

            * `None` to derive accessors from the headings, as described above; or
            * A list of the same size as `headings`, specifying the accessors for each
              heading. A value of [`None`][] will fall back to the default generated
              accessor; or
            * A dictionary mapping headings to accessors. Any missing headings will fall
              back to the default generated accessor.

            The accessors are also passed to any `TreeSources` created by the Tree to
            tell the source how to map lists and tuples to accessor values. This
            ordering does not change even when columns are added or removed.

        :param multiple_select: Does the tree allow multiple selection?
        :param on_select: Initial [`on_select`][toga.Tree.on_select] handler.
        :param on_activate: Initial [`on_activate`][toga.Tree.on_activate] handler.
        :param missing_value: The string that will be used to populate a cell when the
            value provided by its accessor is [`None`][], or the accessor isn't
            defined.
        :param kwargs: Initial style properties.
        """
        self._data: TreeSourceT | TreeSource

        self._missing_value = missing_value or ""
        self._show_headings = headings is not None
        self._multiple_select = multiple_select

        if headings is None and accessors is None:
            raise ValueError(
                "Cannot create a tree without either headings or accessors."
            )

        self._columns: list[ColumnT] = (
            AccessorColumn.columns_from_headings_and_accessors(headings, accessors)
        )

        # The accessors used for ad-hoc TreeSources may have more than just column
        # accessors.
        self._data_accessor_order: list[str] = (
            self.accessors if accessors is None else list(accessors)
        )

        # Prime some properties that need to exist before the tree is created.
        self.on_select = None
        self.on_activate = None

        super().__init__(id, style, **kwargs)

        self.data = data

        self.on_select = on_select
        self.on_activate = on_activate

    def _create(self):
        return self.factory.Tree(interface=self)

    @property
    def enabled(self) -> Literal[True]:
        """Is the widget currently enabled? i.e., can the user interact with the widget?
        Tree widgets cannot be disabled; this property will always return True; any
        attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: object) -> None:
        pass

    @property
    def data(self) -> TreeSourceT | TreeSource:
        """The data to display in the tree.

        When setting this property:

        * A [`Source`][toga.sources.Source] will be used as-is. It must either be a
        [`TreeSource`][toga.sources.TreeSource], or
          a custom class that provides the same methods.

        * A value of None is turned into an empty TreeSource.

        * Otherwise, the value must be a dictionary or an iterable, which is copied
          into a new TreeSource as shown [here][treesource-item].
        """
        return self._data

    @data.setter
    def data(self, data: TreeSourceT | object | None) -> None:
        if hasattr(self, "_data"):
            self._data.remove_listener(self._impl)

        if data is None:
            self._data = TreeSource(accessors=self._data_accessor_order, data=[])
        elif isinstance(data, Source):
            self._data = data
        else:
            self._data = TreeSource(accessors=self._data_accessor_order, data=data)

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

    @property
    def multiple_select(self) -> bool:
        """Does the tree allow multiple rows to be selected?"""
        return self._multiple_select

    @property
    def selection(self) -> list[Node] | Node | None:
        """The current selection of the tree.

        If multiple selection is enabled, returns a list of Node objects from the data
        source matching the current selection. An empty list is returned if no nodes are
        selected.

        If multiple selection is *not* enabled, returns the selected Node object, or
        [`None`][] if no node is currently selected.
        """
        return self._impl.get_selection()

    def expand(self, node: Node | None = None) -> None:
        """Expand the specified node of the tree.

        If no node is provided, all nodes of the tree will be expanded.

        If the provided node is a leaf node, or the node is already expanded, this is a
        no-op.

        If a node is specified, the children of that node will also be expanded.

        :param node: The node to expand
        """
        if node is None:
            self._impl.expand_all()
        else:
            self._impl.expand_node(node)

    def collapse(self, node: Node | None = None) -> None:
        """Collapse the specified node of the tree.

        If no node is provided, all nodes of the tree will be collapsed.

        If the provided node is a leaf node, or the node is already collapsed,
        this is a no-op.

        :param node: The node to collapse
        """
        if node is None:
            self._impl.collapse_all()
        else:
            self._impl.collapse_node(node)

    def append_column(self, heading: str, accessor: str | None = None) -> None:
        """Append a column to the end of the tree.

        :param heading: The heading for the new column.
        :param accessor: The accessor to use on the data source when populating
            the tree. If not specified, an accessor will be derived from the
            heading.
        """
        self.insert_column(len(self._columns), heading, accessor=accessor)

    def insert_column(
        self,
        index: int | str,
        heading: str,
        accessor: str | None = None,
    ) -> None:
        """Insert an additional column into the tree.

        :param index: The index at which to insert the column, or the accessor of the
            column before which the column should be inserted.
        :param heading: The heading for the new column. If the tree doesn't have
            headings, the value will be ignored.
        :param accessor: The accessor to use on the data source when populating the
            tree. If not specified, an accessor will be derived from the heading. An
            accessor *must* be specified if the tree doesn't have headings.
        """
        if self._show_headings:
            column = AccessorColumn(heading, accessor)
        elif accessor is not None:
            column = AccessorColumn(None, accessor)
        else:
            raise ValueError("Must specify an accessor on a tree without headings")

        if isinstance(index, str):
            index = self.accessors.index(index)
        else:
            # Re-interpret negative indices, and clip indices outside valid range.
            if index < 0:
                index = max(len(self._columns) + index, 0)
            else:
                index = min(len(self._columns), index)

        self._columns.insert(index, column)
        self._impl.insert_column(index, column.heading, column.accessor)

    def remove_column(self, column: int | str) -> None:
        """Remove a tree column.

        :param column: The index of the column to remove, or the accessor of the column
            to remove.
        """
        if isinstance(column, str):
            # Column is a string; use as-is
            index = self.accessors.index(column)
        else:
            if column < 0:
                index = len(self._columns) + column
            else:
                index = column

        # Remove column
        del self._columns[index]
        self._impl.remove_column(index)

    @property
    def headings(self) -> list[str] | None:
        """The column headings for the tree (read-only)"""
        if not self._show_headings:
            return None
        else:
            return [column.heading for column in self._columns]

    @property
    def accessors(self) -> list[str]:
        """The accessors used to populate the tree (read-only)"""
        return [column.accessor for column in self._columns]

    @property
    def missing_value(self) -> str:
        """The value that will be used when a data row doesn't provide a value for an
        attribute.
        """
        return self._missing_value

    @property
    def on_select(self) -> OnSelectHandler:
        """The callback function that is invoked when a row of the tree is selected."""
        return self._on_select

    @on_select.setter
    def on_select(self, handler: toga.widgets.tree.OnSelectHandler) -> None:
        self._on_select = wrapped_handler(self, handler)

    @property
    def on_activate(self) -> OnActivateHandler:
        """The callback function that is invoked when a row of the tree is activated,
        usually with a double click or similar action."""
        return self._on_activate

    @on_activate.setter
    def on_activate(self, handler: toga.widgets.tree.OnActivateHandler) -> None:
        self._on_activate = wrapped_handler(self, handler)
