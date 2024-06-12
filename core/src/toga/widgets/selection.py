from __future__ import annotations

import warnings
from collections.abc import Iterable
from typing import Any, Protocol, TypeVar

import toga
from toga.handlers import wrapped_handler
from toga.sources import ListSource, Source

from .base import StyleT, Widget

SourceT = TypeVar("SourceT", bound=Source)


class OnChangeHandler(Protocol):
    def __call__(self, widget: Selection, /, **kwargs: Any) -> object:
        """A handler to invoke when the value is changed.

        :param widget: The Selection that was changed.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class Selection(Widget):
    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        items: SourceT | Iterable | None = None,
        accessor: str | None = None,
        value: object | None = None,
        on_change: toga.widgets.selection.OnChangeHandler | None = None,
        enabled: bool = True,
        on_select: None = None,  # DEPRECATED
    ):
        """Create a new Selection widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param items: Initial :any:`items` to display for selection.
        :param accessor: The accessor to use to extract display values from the list of
            items. See :any:`items` and :any:`value` for details on how
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

        self._items: SourceT | ListSource

        self.on_change = None  # needed for _impl initialization
        self._impl = self.factory.Selection(interface=self)

        self._accessor = accessor
        self.items = items
        if value:
            self.value = value

        self.on_change = on_change
        self.enabled = enabled

    @property
    def items(self) -> SourceT | ListSource:
        """The items to display in the selection.

        When setting this property:

        * A :any:`Source` will be used as-is. It must either be a :any:`ListSource`, or
          a custom class that provides the same methods.

        * A value of None is turned into an empty ListSource.

        * Otherwise, the value must be an iterable, which is copied into a new
          ListSource using the widget's accessor, or "value" if no accessor was
          specified. Items are converted as shown :ref:`here <listsource-item>`.
        """
        return self._items

    @items.setter
    def items(self, items: SourceT | Iterable | None) -> None:
        if self._accessor is None:
            accessors = ["value"]
        else:
            accessors = [self._accessor]

        if items is None:
            self._items = ListSource(accessors=accessors, data=[])
        elif isinstance(items, Source):
            if self._accessor is None:
                raise ValueError("Must specify an accessor to use a data source")
            self._items = items
        else:
            self._items = ListSource(accessors=accessors, data=items)

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
        self.on_change()

        self.refresh()

    def _title_for_item(self, item: Any) -> str:
        """Internal utility method; return the display title for an item"""
        if self._accessor:
            title = getattr(item, self._accessor)
        else:
            title = item.value

        return str(title).split("\n")[0]

    @property
    def value(self) -> object | None:
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
    def value(self, value: object) -> None:
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
    def on_change(self) -> OnChangeHandler:
        """Handler to invoke when the value of the selection is changed, either by the user
        or programmatically."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler: toga.widgets.selection.OnChangeHandler) -> None:
        self._on_change = wrapped_handler(self, handler)

    ######################################################################
    # 2023-05: Backwards compatibility
    ######################################################################

    @property
    def on_select(self) -> OnChangeHandler:
        """**DEPRECATED**: Use ``on_change``"""
        warnings.warn(
            "Selection.on_select has been renamed Selection.on_change.",
            DeprecationWarning,
        )
        return self.on_change

    @on_select.setter
    def on_select(self, handler: toga.widgets.selection.OnChangeHandler) -> None:
        warnings.warn(
            "Selection.on_select has been renamed Selection.on_change.",
            DeprecationWarning,
        )
        self.on_change = handler
