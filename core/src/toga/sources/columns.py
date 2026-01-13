from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable

from ..icons import Icon
from ..widgets.base import Widget
from .accessors import build_accessors, to_accessor
from .list_source import Row

Value = TypeVar("Value", contravariant=False, covariant=False)


@runtime_checkable
class ColumnT(Protocol, Generic[Value]):
    """Protocol that Column types must adhere to."""

    @property
    @abstractmethod
    def heading(self) -> str:
        """The heading text for this column."""

    @abstractmethod
    def value(self, row: Any) -> Value | None:
        """Get a value from the row of a Source.

        :param row: A row object from the underlying Source.
        :returns: The value associated with this column, or
            None if no value.
        """

    @abstractmethod
    def text(self, row: Any, default: str | None = None) -> str | None:
        """Get the text to display for the row in this column.

        :param row: A row object from the underlying Source.
        :param default: A default value if the text cannot be determined.
        :returns: The text to display, or None if no Text.
        """

    @abstractmethod
    def icon(self, row: Any) -> Icon | None:
        """Get the icon to display for the row in this column.

        :param row: A row object from the underlying Source.
        :returns: The icon to display, or None if no Icon.
        """

    def widget(self, row: Row[Value]) -> Widget | None:
        """Get a widget from the Row or Node of a ListSource or TreeSource.

        If the value is a widget, it is returned, otherwise None is returned

        :param row: A row object from the underlying Source.
        :returns: The Widget to use, or None if no Widget.
        """


class AccessorColumn(ColumnT[Value]):
    """This is a column which implements accessor semantics.

    This requires at least one of the heading and the accessor to be
    supplied to the init method. If given just a heading, it generates
    the accessor from the heading.
    """

    def __init__(
        self,
        heading: str | None = None,
        accessor: str | None = None,
    ):
        if accessor is None:
            if heading is not None:
                accessor = to_accessor(heading)
            else:
                raise ValueError(
                    "Cannot create a column without either headings or accessors"
                )
        self._heading = heading
        self._accessor = accessor

    @property
    def heading(self):
        return self._heading if self._heading is not None else ""

    @property
    def accessor(self):
        return self._accessor

    def value(self, row: Row[Value]) -> Value | None:
        """Get a value from the Row or Node of a ListSource or TreeSource.

        :param row: A Row object from the underlying Source.
        :returns: The value associated with this column's accessor, or
            None if no value.
        """
        return getattr(row, self.accessor, None)

    def text(self, row: Row[Value], default: str | None = None) -> str | None:
        """Get text from the Row or Node of a ListSource or TreeSource.

        If the value is a tuple, the second item is assumed to be text.
        If the value is not None, it is converted to a string by calling
        str().
        If the value ends up being None, and a default is supplied, the default
        is returned.

        :param row: A row object from the underlying Source.
        :param default: A default value if the resulting value is otherwise None.
        :returns: The text to associated with this column's accessor, or
            None if no text.
        """
        match value := self.value(row):
            case Widget():
                return default
            case (_, None):
                return default
            case (_, value):
                return str(value)
            case None:
                return default
            case _:
                return str(value)

    def icon(self, row: Row[Value]) -> Icon | None:
        """Get text from the Row or Node of a ListSource or TreeSource.

        If the value is a tuple, the first item is assumed to be an Icon.
        Otherwise if the item has an `icon` attribute, that is assumed to
        be the icon.

        :param row: A row object from the underlying Source.
        :returns: The Icon to associated with this column's accessor, or
            None if no Icon.
        """
        match value := self.value(row):
            case Widget():
                return None
            case (icon, _):
                return icon
            case _:
                return getattr(value, "icon", None)

    def widget(self, row: Row[Value]) -> Widget | None:
        """Get a widget from the Row or Node of a ListSource or TreeSource.

        If the value is a widget, it is returned, otherwise None is returned

        :param row: A row object from the underlying Source.
        :returns: The Widget to associated with this column's accessor, or
            None if no Widget.
        """
        if isinstance(value := self.value(row), Widget):
            return value
        else:
            return None

    @classmethod
    def columns_from_headings_and_accessors(
        cls,
        headings: Iterable[str] | None = None,
        accessors: Iterable[str] | None = None,
    ) -> list[ColumnT]:
        """Get a list of columns from lists of headings and accessors.

        :param headings: A list of heading titles, or None if no headings.
        :param accessors: A list of accessor names, or None if accessors are
            to be generated from the headings automatically.

        :returns: A list of AccessorColumns matching the order of headers and
            accessors.
        :raises ValueError: If neither headings nor accessor liss are supplied.
        """
        if headings is not None:
            headings = [heading.splitlines()[0] for heading in headings]
            accessors = build_accessors(headings, accessors)
            return [
                cls(heading, accessor)
                for heading, accessor in zip(headings, accessors, strict=False)
            ]
        elif accessors is not None:
            accessors = list(accessors)
            return [cls(None, accessor) for accessor in accessors]
        else:
            raise ValueError(
                "Cannot create columns without either headings or accessors."
            )
