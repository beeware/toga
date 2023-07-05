from __future__ import annotations

import warnings
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
        primary_action: str | None = "Delete",
        on_primary_action: callable = None,
        secondary_action: str | None = "Action",
        on_secondary_action: callable = None,
        on_refresh: callable = None,
        on_select: callable = None,
        on_delete: callable = None,  # DEPRECATED
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
        :param primary_action: The name for the primary action.
        :param on_primary_action: Initial :any:`on_primary_action` handler.
        :param secondary_action: The name for the primary action.
        :param on_secondary_action: Initial :any:`on_secondary_action` handler.
        :param on_refresh: Initial :any:`on_refresh` handler.
        :param on_delete: **DEPRECATED**; use :attr:`on_activate`.
        """
        super().__init__(id=id, style=style)

        ######################################################################
        # 2023-06: Backwards compatibility
        ######################################################################
        if on_delete:
            if on_primary_action:
                raise ValueError("Cannot specify both on_delete and on_primary_action")
            else:
                warnings.warn(
                    "DetailedList.on_delete has been renamed DetailedList.on_primary_action.",
                    DeprecationWarning,
                )
                on_primary_action = on_delete
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        # Prime the attributes and handlers that need to exist when the widget is created.
        self._accessors = accessors
        self._primary_action = primary_action
        self._secondary_action = secondary_action
        self._missing_value = missing_value
        self._data = None
        self.on_select = None

        self._impl = self.factory.DetailedList(interface=self)

        self.data = data
        self.on_primary_action = on_primary_action
        self.on_secondary_action = on_secondary_action
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
        "No-op; DetailedList cannot accept input focus"
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
    def on_primary_action(self) -> callable:
        """The handler to invoke when the user performs the primary action on a row of
        the DetailedList.

        The primary action is "swipe left" on UIs that support swipe interactions;
        platforms that don't use swipe interactions may manifest this action in other
        ways (e.g, a context menu).

        If no ``on_primary_action`` handler is provided, the primary action will be
        disabled in the UI.
        """
        return self._on_primary_action

    @on_primary_action.setter
    def on_primary_action(self, handler: callable):
        self._on_primary_action = wrapped_handler(self, handler)
        self._impl.set_primary_action_enabled(handler is not None)

    @property
    def on_secondary_action(self) -> callable:
        """The handler to invoke when the user performs the secondary action on a row of
        the DetailedList.

        The secondary action is "swipe right" on UIs that support swipe interactions;
        platforms that don't use swipe interactions may manifest this action in other
        ways (e.g, a context menu).

        If no ``on_secondary_action`` handler is provided, the secondary action will be
        disabled in the UI.
        """
        return self._on_secondary_action

    @on_secondary_action.setter
    def on_secondary_action(self, handler: callable):
        self._on_secondary_action = wrapped_handler(self, handler)
        self._impl.set_secondary_action_enabled(handler is not None)

    @property
    def on_refresh(self) -> callable:
        """The callback function to invoke when the user performs a refresh action
        (usually "pull down to refresh") on the DetailedList.

        If no ``on_refresh`` handler is provided, the refresh UI action will be
        disabled.
        """
        return self._on_refresh

    @on_refresh.setter
    def on_refresh(self, handler: callable):
        self._on_refresh = wrapped_handler(
            self, handler, cleanup=self._impl.after_on_refresh
        )
        self._impl.set_refresh_enabled(handler is not None)

    @property
    def on_select(self) -> callable:
        """The callback function that is invoked when a row of the DetailedList is selected."""
        return self._on_select

    @on_select.setter
    def on_select(self, handler: callable):
        self._on_select = wrapped_handler(self, handler)

    ######################################################################
    # 2023-06: Backwards compatibility
    ######################################################################

    @property
    def on_delete(self):
        """**DEPRECATED**: Use ``on_primary_action``"""
        warnings.warn(
            "DetailedList.on_delete has been renamed DetailedList.on_primary_action.",
            DeprecationWarning,
        )
        return self.on_primary_action

    @on_delete.setter
    def on_delete(self, handler):
        warnings.warn(
            "DetailedList.on_delete has been renamed DetailedList.on_primary_action.",
            DeprecationWarning,
        )
        self.on_primary_action = handler
