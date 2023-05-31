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
        """Create a new Slider widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param items: The items to display for selection. Can be either a list
            of literal items, or a ListSource.
        :param accessor: The accessor for the ListSource. If ``items`` is
            provided as a list of items that are non-string iterable objects,
            the ``accessor`` is used to select the attribute of the item that
            will be used for display purposes. Not required if the ``items`` is
            a list of strings, a list of non-iterable objects, or a ListSource.
        :param value: Initial value for the selection. If unspecified, the first
            item will be selected.
        :param on_change: Initial :any:`on_change` handler.
        :param enabled: Whether the user can interact with the widget.
        """
        super().__init__(id=id, style=style)

        self.on_change = None  # needed for _impl initialization
        self._impl = self.factory.Selection(interface=self)

        self._accessor = accessor
        self.items = items
        if value:
            self.value = value

        # 2023-05-29: Rename on_select to on_change
        if on_select:  # pragma: no cover
            if on_change:
                raise ValueError(
                    "Cannot specify both `on_select` and `on_change`; "
                    "`on_select` has been deprecated, use `on_change`"
                )
            else:
                warnings.warn(
                    "Selection.on_select has been renamed Selection.on_change"
                )
                on_change = on_select

        self.on_change = on_change
        self.enabled = enabled

    @property
    def items(self) -> ListSource:
        """The list of items to display in the selection, as a ListSource.

        A value of None is turned into an empty ListSource.

        A literal list of values will be converted into a ListSource. The
        conversion that takes place depends on the type of data in the list:

         * Literal strings will be used as-is.

         * Non-iterable objects will be converted to a string for display
           purposes, but will be returned in their original form.

         * If the object is iterable, the value of the attribute described
           by the ``accessor`` argument provided at the time of construction
           will be used. If no ``accessor`` was provided, the ListSource will
           look for an attribute named ``value``.
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
        self._impl.change_source(source=self._items)
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

        If changing the current value, ValueError is raised if the specified
        item cannot be found in the data source.
        """
        item = self._impl.get_selected_item()
        # If there was no accessor specified, the data values are literals.
        # Dereference the value out of the Row object.
        if item and self._accessor is None:
            return item.value
        return item

    @value.setter
    def value(self, value):
        try:
            if self._accessor is None:
                item = self._items.find(value=value)
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
