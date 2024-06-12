from __future__ import annotations

import warnings
from collections.abc import Iterable
from typing import Any, Literal, Protocol, TypeVar

import toga
from toga.handlers import wrapped_handler
from toga.sources import ListSource, Row, Source
from toga.sources.accessors import build_accessors, to_accessor

from .base import StyleT, Widget

SourceT = TypeVar("SourceT", bound=Source)


class OnSelectHandler(Protocol):
    def __call__(self, widget: Table, /, **kwargs: Any) -> object:
        """A handler to invoke when the table is selected.

        :param widget: The Table that was selected.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class OnActivateHandler(Protocol):
    def __call__(self, widget: Table, /, row: Any, **kwargs: Any) -> object:
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
        data: SourceT | Iterable | None = None,
        accessors: Iterable[str] | None = None,
        multiple_select: bool = False,
        on_select: toga.widgets.table.OnSelectHandler | None = None,
        on_activate: toga.widgets.table.OnActivateHandler | None = None,
        missing_value: str = "",
        on_double_click: None = None,  # DEPRECATED
    ):
        """Create a new Table widget.

        :param headings: The column headings for the table. Headings can only contain
            one line; any text after a newline will be ignored.

            A value of :any:`None` will produce a table without headings.
            However, if you do this, you *must* give a list of accessors.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param data: Initial :any:`data` to be displayed in the table.

        :param accessors: Defines the attributes of the data source that will be used to
            populate each column. Must be either:

            * ``None`` to derive accessors from the headings, as described above; or
            * A list of the same size as ``headings``, specifying the accessors for each
              heading. A value of :any:`None` will fall back to the default generated
              accessor; or
            * A dictionary mapping headings to accessors. Any missing headings will fall
              back to the default generated accessor.

        :param multiple_select: Does the table allow multiple selection?
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
                    "Table.on_double_click has been renamed Table.on_activate.",
                    DeprecationWarning,
                )
                on_activate = on_double_click
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self._headings: list[str] | None
        self._accessors: list[str]
        self._data: SourceT | ListSource

        if headings is not None:
            self._headings = [heading.split("\n")[0] for heading in headings]
            self._accessors = build_accessors(self._headings, accessors)
        elif accessors is not None:
            self._headings = None
            self._accessors = list(accessors)
        else:
            raise ValueError(
                "Cannot create a table without either headings or accessors"
            )

        self._multiple_select = multiple_select
        self._missing_value = missing_value or ""

        # Prime some properties that need to exist before the table is created.
        self.on_select = None
        self.on_activate = None
        self._data = None

        self._impl = self.factory.Table(interface=self)
        self.data = data

        self.on_select = on_select
        self.on_activate = on_activate

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

    def focus(self) -> None:
        """No-op; Table cannot accept input focus."""
        pass

    @property
    def data(self) -> SourceT | ListSource:
        """The data to display in the table.

        When setting this property:

        * A :any:`Source` will be used as-is. It must either be a :any:`ListSource`, or
          a custom class that provides the same methods.

        * A value of None is turned into an empty ListSource.

        * Otherwise, the value must be an iterable, which is copied into a new
          ListSource. Items are converted as shown :ref:`here <listsource-item>`.
        """
        return self._data

    @data.setter
    def data(self, data: SourceT | Iterable | None) -> None:
        if data is None:
            self._data = ListSource(accessors=self._accessors, data=[])
        elif isinstance(data, Source):
            self._data = data
        else:
            self._data = ListSource(accessors=self._accessors, data=data)

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
        :any:`None` if no row is currently selected.
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

    def add_column(self, heading: str, accessor: str | None = None) -> None:
        """**DEPRECATED**: use :meth:`~toga.Table.append_column`"""
        self.insert_column(len(self._accessors), heading, accessor=accessor)

    def append_column(self, heading: str, accessor: str | None = None) -> None:
        """Append a column to the end of the table.

        :param heading: The heading for the new column.
        :param accessor: The accessor to use on the data source when populating
            the table. If not specified, an accessor will be derived from the
            heading.
        """
        self.insert_column(len(self._accessors), heading, accessor=accessor)

    def insert_column(
        self,
        index: int | str,
        heading: str,
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
        if self._headings is None:
            if accessor is None:
                raise ValueError("Must specify an accessor on a table without headings")
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
        """Remove a table column.

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
        """The column headings for the table, or None if there are no headings
        (read-only)
        """
        return self._headings

    @property
    def accessors(self) -> list[str]:
        """The accessors used to populate the table (read-only)"""
        return self._accessors

    @property
    def missing_value(self) -> str:
        """The value that will be used when a data row doesn't provide a value for an
        attribute.
        """
        return self._missing_value

    ######################################################################
    # 2023-06: Backwards compatibility
    ######################################################################

    @property
    def on_double_click(self) -> OnActivateHandler:
        """**DEPRECATED**: Use ``on_activate``"""
        warnings.warn(
            "Table.on_double_click has been renamed Table.on_activate.",
            DeprecationWarning,
        )
        return self.on_activate

    @on_double_click.setter
    def on_double_click(self, handler: toga.widgets.table.OnActivateHandler) -> None:
        warnings.warn(
            "Table.on_double_click has been renamed Table.on_activate.",
            DeprecationWarning,
        )
        self.on_activate = handler
