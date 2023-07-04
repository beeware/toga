from __future__ import annotations

from typing import Any

from toga.handlers import wrapped_handler
from toga.sources import ListSource, Row, Source

from .base import Widget


class DetailedList(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        data: Any = None,
        accessors: tuple[str, str, str] = ("title", "subtitle", "icon"),
        missing_value: str = "",
        on_delete: callable = None,
        on_refresh: callable = None,
        on_select: callable = None,
    ):
        """Create a new DetailedList widget.

        Inherits from :class:`toga.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param data: The data to be displayed on the table. Can be a list of values or a
            ListSource. See the definition of the :attr:`data` property for details on
            how data can be specified and used.
        :param accessors: The accessors to use to retrieve the data for each item. A tuple,
            specifying the accessors for (title, subtitle, icon).
        :param missing_value: The data to use subtitle to use when the data source doesn't provide a
            title for a data item.
        :param on_select: Initial :any:`on_select` handler.
        :param on_refresh: Initial :any:`on_refresh` handler.
        :param on_delete: Initial :any:`on_delete` handler.
        """
        super().__init__(id=id, style=style)
        self._accessors = accessors
        self._missing_value = missing_value
        self._data = None
        self.on_delete = None
        self.on_refresh = None
        self.on_select = None

        self._impl = self.factory.DetailedList(interface=self)

        self.data = data
        self.on_delete = on_delete
        self.on_refresh = on_refresh
        self.on_select = on_select

    @property
    def enabled(self) -> bool:
        """Is the widget currently enabled? i.e., can the user interact with the widget?
        DetailList widgets cannot be disabled; this property will always return True; any
        attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value):
        pass

    def focus(self):
        "No-op; DetailList cannot accept input focus"
        pass

    @property
    def data(self) -> ListSource:
        """The data to display in the DetailedList, as a ListSource.

        When specifying data:

        * A ListSource will be used as-is

        * A value of None is turned into an empty ListSource.

        * A list or tuple of values will be converted into a ListSource. Each item in
          the list will be converted into a Row object.

          * If the item in the list is a dictionary, the keys of the dictionary will
            become the attributes of the Row.

          * All other values will be converted into a Row with attributes matching the
            ``accessors`` provided at time of construction (with the default accessors
            of ``("title", "subtitle", "icon")``.

            If the value is a string, or any other a non-iterable object, the Row will
            have a single attribute matching the title's accessor.

            If the value is a list, tuple, or any other iterable, values in the iterable
            will be mapped in order to the accessors.
        """
        return self._data

    @data.setter
    def data(self, data: Any):
        if data is None:
            self._data = ListSource(data=[], accessors=self.accessors)
        elif isinstance(data, Source):
            self._data = data
        else:
            self._data = ListSource(data=data, accessors=self.accessors)

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

    def scroll_to_top(self):
        """Scroll the view so that the top of the list (first row) is visible."""
        self.scroll_to_row(0)

    def scroll_to_row(self, row: int):
        """Scroll the view so that the specified row index is visible.

        :param row: The index of the row to make visible. Negative values refer to the
            nth last row (-1 is the last row, -2 second last, and so on).
        """
        if len(self.data) > 1:
            if row >= 0:
                self._impl.scroll_to_row(min(row, len(self.data)))
            else:
                self._impl.scroll_to_row(max(len(self.data) + row, 0))

    def scroll_to_bottom(self):
        """Scroll the view so that the bottom of the list (last row) is visible."""
        self.scroll_to_row(-1)

    @property
    def accessors(self) -> list[str]:
        """The accessors used to populate the table"""
        return self._accessors

    @property
    def missing_value(self) -> str:
        """The value that will be used when a data row doesn't provide an value for an
        attribute.
        """
        return self._missing_value

    @property
    def selection(self) -> Row | None:
        """The current selection of the table.

        Returns the selected Row object, or :any:`None` if no row is currently selected.
        """
        try:
            return self.data[self._impl.get_selection()]
        except TypeError:
            return None

    @property
    def on_delete(self) -> callable:
        """The handler to invoke when the user performs a deletion action on a row of the
        DetailedList."""
        return self._on_delete

    @on_delete.setter
    def on_delete(self, handler: callable):
        self._on_delete = wrapped_handler(self, handler)

    @property
    def on_refresh(self) -> callable:
        """The callback function to invoke when the user performs a refresh action on the
        DetailedList."""
        return self._on_refresh

    @on_refresh.setter
    def on_refresh(self, handler: callable):
        self._on_refresh = wrapped_handler(self, handler)

    @property
    def on_select(self) -> callable:
        """The callback function that is invoked when a row of the DetailedList is selected."""
        return self._on_select

    @on_select.setter
    def on_select(self, handler: callable):
        self._on_select = wrapped_handler(self, handler)
