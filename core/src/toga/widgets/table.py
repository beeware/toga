from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Literal, Protocol

import toga
from toga.handlers import wrapped_handler
from toga.sources import ListSource, ListSourceT, Row, Source
from toga.sources.columns import AccessorColumn, ColumnT

from .base import StyleT, Widget


class OnSelectHandler(Protocol):
    def __call__(self, widget: Table, **kwargs: Any) -> None:
        """A handler to invoke when the table is selected.

        :param widget: The Table that was selected.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class OnActivateHandler(Protocol):
    def __call__(self, widget: Table, row: Any, **kwargs: Any) -> None:
        """A handler to invoke when the table is activated.

        :param widget: The Table that was activated.
        :param row: The Table Row that was activated.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class Table(Widget):
    def __init__(
        self,
        headings: Iterable[str] | None = None,
        id: str | None = None,
        style: StyleT | None = None,
        data: ListSourceT | Iterable | None = None,
        accessors: Iterable[str] | None = None,
        multiple_select: bool = False,
        on_select: toga.widgets.table.OnSelectHandler | None = None,
        on_activate: toga.widgets.table.OnActivateHandler | None = None,
        missing_value: str = "",
        **kwargs,
    ):
        """Create a new Table widget.

        :param headings: The column headings for the table. Headings can only contain
            one line; any text after a newline will be ignored.

            A value of [`None`][] will produce a table without headings.
            However, if you do this, you *must* give a list of accessors.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param data: Initial [`data`][toga.Table.data] to be displayed in the table.

        :param accessors: Defines the attributes of the data source that will be used to
            populate each column. Must be either:

            * `None` to derive accessors from the headings, as described above; or

            * A list of the same size as `headings`, specifying the accessors for each
              heading. A value of [`None`][] will fall back to the default generated
              accessor; or

            * A dictionary mapping headings to accessors. Any missing headings will fall
              back to the default generated accessor.

            The accessors are also passed to any `ListSources` created by the Table to
            tell the source how to map lists and tuples to accessor values. This
            ordering does not change even when columns are added or removed.

        :param multiple_select: Does the table allow multiple selection?
        :param on_select: Initial [`on_select`][toga.Table.on_select] handler.
        :param on_activate: Initial [`on_activate`][toga.Table.on_activate] handler.
        :param missing_value: The string that will be used to populate a cell when the
            value provided by its accessor is [`None`][], or the accessor isn't
            defined.
        :param kwargs: Initial style properties.
        """
        self._data: ListSourceT | ListSource

        self._missing_value = missing_value or ""
        self._show_headings = headings is not None
        self._multiple_select = multiple_select

        if headings is None and accessors is None:
            raise ValueError(
                "Cannot create a table without either headings or accessors."
            )

        self._columns: list[ColumnT] = (
            AccessorColumn.columns_from_headings_and_accessors(headings, accessors)
        )

        # The accessors used for ad-hoc TreeSources may have more than just column
        # accessors.
        self._data_accessor_order: list[str] = (
            self.accessors if accessors is None else list(accessors)
        )

        # Prime some properties that need to exist before the table is created.
        self.on_select = None
        self.on_activate = None

        super().__init__(id, style, **kwargs)

        self.data = data

        self.on_select = on_select
        self.on_activate = on_activate

    def _create(self) -> Any:
        return self.factory.Table(interface=self)

    @property
    def enabled(self) -> Literal[True]:
        """Is the widget currently enabled? i.e., can the user interact with the widget?
        Table widgets cannot be disabled; this property will always return True; any
        attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: object) -> None:
        pass

    @property
    def data(self) -> ListSourceT | ListSource:
        """The data to display in the table.

        When setting this property:

        * A [`Source`][toga.sources.Source] will be used as-is. It must either be a
          [`ListSource`][toga.sources.ListSource], or
          a custom class that provides the same methods.

        * A value of None is turned into an empty ListSource.

        * Otherwise, the value must be an iterable, which is copied into a new
          ListSource. Items are converted as shown [here][listsource-item].
        """
        return self._data

    @data.setter
    def data(self, data: ListSourceT | Iterable | None) -> None:
        if hasattr(self, "_data"):
            self._data.remove_listener(self._impl)

        if data is None:
            self._data = ListSource(accessors=self._data_accessor_order, data=[])
        elif isinstance(data, Source):
            self._data = data
        else:
            self._data = ListSource(accessors=self._data_accessor_order, data=data)

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

    @property
    def multiple_select(self) -> bool:
        """Does the table allow multiple rows to be selected?"""
        return self._multiple_select

    @property
    def selection(self) -> list[Row] | Row | None:
        """The current selection of the table.

        If multiple selection is enabled, returns a list of Row objects from the data
        source matching the current selection. An empty list is returned if no rows are
        selected.

        If multiple selection is *not* enabled, returns the selected Row object, or
        [`None`][] if no row is currently selected.
        """
        selection = self._impl.get_selection()
        if isinstance(selection, list):
            return [self.data[index] for index in selection]
        elif selection is None:
            return None
        else:
            return self.data[selection]

    def scroll_to_top(self) -> None:
        """Scroll the view so that the top of the list (first row) is visible."""
        self.scroll_to_row(0)

    def scroll_to_row(self, row: int) -> None:
        """Scroll the view so that the specified row index is visible.

        :param row: The index of the row to make visible. Negative values refer to the
            nth last row (-1 is the last row, -2 second last, and so on).
        """
        if len(self.data) > 1:
            if row >= 0:
                self._impl.scroll_to_row(min(row, len(self.data)))
            else:
                self._impl.scroll_to_row(max(len(self.data) + row, 0))

    def scroll_to_bottom(self) -> None:
        """Scroll the view so that the bottom of the list (last row) is visible."""
        self.scroll_to_row(-1)

    @property
    def on_select(self) -> OnSelectHandler:
        """The callback function that is invoked when a row of the table is selected."""
        return self._on_select

    @on_select.setter
    def on_select(self, handler: toga.widgets.table.OnSelectHandler) -> None:
        self._on_select = wrapped_handler(self, handler)

    @property
    def on_activate(self) -> OnActivateHandler:
        """The callback function that is invoked when a row of the table is activated,
        usually with a double click or similar action."""
        return self._on_activate

    @on_activate.setter
    def on_activate(self, handler: toga.widgets.table.OnActivateHandler) -> None:
        self._on_activate = wrapped_handler(self, handler)

    def append_column(
        self,
        heading: str | None = None,
        accessor: str | None = None,
    ) -> None:
        """Append a column to the end of the table.

        :param heading: The heading for the new column.
        :param accessor: The accessor to use on the data source when populating
            the table. If not specified, an accessor will be derived from the
            heading.
        """
        self.insert_column(len(self._columns), heading, accessor=accessor)

    def insert_column(
        self,
        index: int | str,
        heading: str | None = None,
        accessor: str | None = None,
    ) -> None:
        """Insert an additional column into the table.

        :param index: The index at which to insert the column, or the accessor of the
            column before which the column should be inserted.
        :param heading: The heading for the new column. If the table doesn't have
            headings, the value will be ignored.
        :param accessor: The accessor to use on the data source when populating the
            table. If not specified, an accessor will be derived from the heading. An
            accessor *must* be specified if the table doesn't have headings.
        """
        if self._show_headings:
            column = AccessorColumn(heading, accessor)
        elif accessor is not None:
            column = AccessorColumn(None, accessor)
        else:
            raise ValueError("Must specify an accessor on a table without headings")

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
        """Remove a table column.

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
        """The column headings for the table, or None if there are no headings
        (read-only)
        """
        if not self._show_headings:
            return None
        else:
            return [column.heading for column in self._columns]

    @property
    def accessors(self) -> list[str]:
        """The accessors used to populate the table (read-only)"""
        return [column.accessor for column in self._columns]

    @property
    def missing_value(self) -> str:
        """The value that will be used when a data row doesn't provide a value for an
        attribute.
        """
        return self._missing_value
