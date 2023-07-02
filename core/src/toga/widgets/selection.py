from __future__ import annotations

import warnings

from toga.handlers import wrapped_handler
from toga.sources import ListSource

from .base import Widget


class Selection(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        items: list | ListSource | None = None,
        accessor: str | None = None,
        value: None = None,
        on_change: callable | None = None,
        enabled=True,
        on_select: callable | None = None,  # DEPRECATED
    ):
        """Create a new Selection widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param items: The items to display for selection. Can be a list of values or a
            ListSource. See the definition of the ``items`` property for details on how
            items can be specified and used.
        :param accessor: The accessor to use to extract display values from the list of
            items. See the definition of the ``items`` property for details on how
            ``accessor`` alters the interpretation of data in the Selection.
        :param value: Initial value for the selection. If unspecified, the first item in
            ``items`` will be selected.
        :param on_change: Initial :any:`on_change` handler.
        :param enabled: Whether the user can interact with the widget.
        """
        super().__init__(id=id, style=style)

        ######################################################################
        # 2023-05: Backwards compatibility
        ######################################################################
        if on_select:  # pragma: no cover
            if on_change:
                raise ValueError("Cannot specify both on_select and on_change")
            else:
                warnings.warn(
                    "Selection.on_select has been renamed Selection.on_change",
                    DeprecationWarning,
                )
                on_change = on_select
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self.on_change = None  # needed for _impl initialization
        self._impl = self.factory.Selection(interface=self)

        self._accessor = accessor
        self.items = items
        if value:
            self.value = value

        self.on_change = on_change
        self.enabled = enabled

    @property
    def items(self) -> ListSource:
        """The list of items to display in the selection, as a ListSource.

        When specifying items:

        * A ListSource will be used as-is

        * A value of None is turned into an empty ListSource.

        * A list or tuple of values will be converted into a ListSource. Each item in
          the list will be converted into a Row object.

          * If the item in the list is a dictionary, the keys of the dictionary will
            become the attributes of the Row.

          * All other items will be converted into a Row with a single attribute
            attribute whose name matches the ``accessor`` provided when the Selection
            was constructed (with an attribute of ``value`` being used if no accessor
            was specified).

            If the item is a string, or any other a non-iterable object, the value of
            the attribute will be the item value.

            If the item is list, tuple, or other iterable, the value of the attribute
            will be the first item in the iterable.
        """
        return self._items

    @items.setter
    def items(self, items):
        if self._accessor is None:
            accessors = ["value"]
        else:
            accessors = [self._accessor]

        if items is None:
            self._items = ListSource(accessors=accessors, data=[])
        elif isinstance(items, (list, tuple)):
            self._items = ListSource(accessors=accessors, data=items)
        else:
            if self._accessor is None:
                raise ValueError("Must specify an accessor to use a data source")
            self._items = items

        self._items.add_listener(self._impl)

        # Temporarily halt notifications
        orig_on_change = self._on_change
        self.on_change = None

        # Clear the widget, and insert all the data rows
        self._impl.clear()
        for index, item in enumerate(self.items):
            self._impl.insert(index, item)

        # Restore the original change handler and trigger it.
        self._on_change = orig_on_change
        self.on_change(None)

        self.refresh()

    def _title_for_item(self, item):
        """Internal utility method; return the display title for an item"""
        if self._accessor:
            title = getattr(item, self._accessor)
        else:
            title = item.value

        return str(title)

    @property
    def value(self):
        """The currently selected item.

        Returns None if there are no items in the selection.

        If an ``accessor`` was specified when the Selection was constructed, the value
        returned will be Row objects from the ListSource; to change the selection, a Row
        object from the ListSource must be provided.

        If no ``accessor`` was specified when the Selection was constructed, the value
        returned will be the value stored as the ``value`` attribute on the Row object.
        When setting the value, the widget will search for the first Row object whose
        ``value`` attribute matches the provided value. In practice, this means that you
        can treat the selection as containing a list of literal values, rather than a
        ListSource containing Row objects.
        """
        index = self._impl.get_selected_index()
        if index is None:
            return None

        item = self._items[index]
        # If there was no accessor specified, the data values are literals.
        # Dereference the value out of the Row object.
        if item and self._accessor is None:
            return item.value
        return item

    @value.setter
    def value(self, value):
        try:
            if self._accessor is None:
                item = self._items.find(dict(value=value))
            else:
                item = value

            index = self._items.index(item)
            self._impl.select_item(index=index, item=item)
        except ValueError:
            raise ValueError(f"{value!r} is not a current item in the selection")

    @property
    def on_change(self) -> callable:
        """Handler to invoke when the value of the selection is changed, either by the user
        or programmatically."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)

    ######################################################################
    # 2023-05: Backwards compatibility
    ######################################################################

    @property
    def on_select(self) -> callable:
        """**DEPRECATED**: Use ``on_change``"""
        warnings.warn(
            "Selection.on_select has been renamed Selection.on_change.",
            DeprecationWarning,
        )
        return self.on_change

    @on_select.setter
    def on_select(self, handler):
        warnings.warn(
            "Selection.on_select has been renamed Selection.on_change.",
            DeprecationWarning,
        )
        self.on_change = handler
