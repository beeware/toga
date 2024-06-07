from __future__ import annotations

import warnings
from collections.abc import Iterable
from typing import Any, Literal, Protocol, TypeVar

import toga
from toga.handlers import wrapped_handler
from toga.sources import Node, Source, TreeSource
from toga.sources.accessors import build_accessors, to_accessor
from toga.style import Pack

from .base import Widget

SourceT = TypeVar("SourceT", bound=Source)


class OnSelectHandler(Protocol):
    def __call__(self, widget: Tree, /, **kwargs: Any) -> object:
        """A handler to invoke when the tree is selected.

        :param widget: The Tree that was selected.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class OnActivateHandler(Protocol):
    def __call__(self, widget: Tree, /, **kwargs: Any) -> object:
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
        data: SourceT | object | None = None,
        accessors: Iterable[str] | None = None,
        multiple_select: bool = False,
        on_select: toga.widgets.tree.OnSelectHandler | None = None,
        on_activate: toga.widgets.tree.OnActivateHandler | None = None,
        missing_value: str = "",
        on_double_click: None = None,  # DEPRECATED
    ):
        """Create a new Tree widget.

        :param headings: The column headings for the tree. Headings can only contain one
            line; any text after a newline will be ignored.

            A value of :any:`None` will produce a table without headings.
            However, if you do this, you *must* give a list of accessors.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param data: Initial :any:`data` to be displayed in the tree.

        :param accessors: Defines the attributes of the data source that will be used to
            populate each column. Must be either:

            * ``None`` to derive accessors from the headings, as described above; or
            * A list of the same size as ``headings``, specifying the accessors for each
              heading. A value of :any:`None` will fall back to the default generated
              accessor; or
            * A dictionary mapping headings to accessors. Any missing headings will fall
              back to the default generated accessor.

        :param multiple_select: Does the tree allow multiple selection?
        :param on_select: Initial :any:`on_select` handler.
        :param on_activate: Initial :any:`on_activate` handler.
        :param missing_value: The string that will be used to populate a cell when the
            value provided by its accessor is :any:`None`, or the accessor isn't
            defined.
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

        self._headings: list[str] | None
        self._data: SourceT | TreeSource

        if headings is not None:
            self._headings = [heading.split("\n")[0] for heading in headings]
            self._accessors = build_accessors(self._headings, accessors)
        elif accessors is not None:
            self._headings = None
            self._accessors = list(accessors)
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
    def enabled(self) -> Literal[True]:
        """Is the widget currently enabled? i.e., can the user interact with the widget?
        Tree widgets cannot be disabled; this property will always return True; any
        attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: object) -> None:
        pass

    def focus(self) -> None:
        """No-op; Tree cannot accept input focus."""
        pass

    @property
    def data(self) -> SourceT | TreeSource:
        """The data to display in the tree.

        When setting this property:

        * A :any:`Source` will be used as-is. It must either be a :any:`TreeSource`, or
          a custom class that provides the same methods.

        * A value of None is turned into an empty TreeSource.

        * Otherwise, the value must be a dictionary or an iterable, which is copied
          into a new TreeSource as shown :ref:`here <treesource-item>`.
        """
        return self._data

    @data.setter
    def data(self, data: SourceT | object | None) -> None:
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

        If multiple selection is enabled, returns a list of Node objects from the data
        source matching the current selection. An empty list is returned if no nodes are
        selected.

        If multiple selection is *not* enabled, returns the selected Node object, or
        :any:`None` if no node is currently selected.
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
        self.insert_column(len(self._accessors), heading, accessor=accessor)

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

    def remove_column(self, column: int | str) -> None:
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
    def headings(self) -> list[str] | None:
        """The column headings for the tree (read-only)"""
        return self._headings

    @property
    def accessors(self) -> list[str]:
        """The accessors used to populate the tree (read-only)"""
        return self._accessors

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

    ######################################################################
    # 2023-06: Backwards compatibility
    ######################################################################

    @property
    def on_double_click(self) -> OnActivateHandler:
        """**DEPRECATED**: Use ``on_activate``"""
        warnings.warn(
            "Tree.on_double_click has been renamed Tree.on_activate.",
            DeprecationWarning,
        )
        return self.on_activate

    @on_double_click.setter
    def on_double_click(self, handler: toga.widgets.tree.OnActivateHandler) -> None:
        warnings.warn(
            "Tree.on_double_click has been renamed Tree.on_activate.",
            DeprecationWarning,
        )
        self.on_activate = handler
