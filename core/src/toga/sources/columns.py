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


class Column(ColumnT[Value], Generic[Value]):
    """An implementation the ColumnT protocol for easy subclassing.

    This abstract base class provides default implementations of the ColumnT:
    the value, icon and widget methods all return None, and the text method
    returns the str() of the value, or the default string if the value is None.
    The constructor takes the heading text and makes it available as a property.

    Unmodified, the column will display the default text value in each cell.

    Subclasses should override the value method at a minimum, and other methods
    as needed.
    """

    def __init__(self, heading: str | None):
        self._heading = heading

    @property
    def heading(self) -> str:
        """The heading text for this column."""
        return self._heading if self._heading is not None else ""

    def value(self, row: Any) -> Value | None:
        """Get a value from the row of a Source.

        The base implementation always returns None.

        :param row: A row object from the underlying Source.
        :returns: The value associated with this column, or
            None if no value.
        """
        return None

    def text(self, row: Any, default: str | None = None) -> str | None:
        """Get the text to display for the row in this column.

        This returns the str() of the value unless the value is
        None, in which case it returns the default.

        :param row: A row object from the underlying Source.
        :param default: A default value if the text cannot be determined.
        :returns: The text to display, or None if no Text.
        """
        value = self.value(row)
        return str(value) if value is not None else default

    def icon(self, row: Any) -> Icon | None:
        """Get the icon to display for the row in this column.

        The default

        :param row: A row object from the underlying Source.
        :returns: The icon to display, or None if no Icon.
        """
        return None

    def widget(self, row: Any) -> Widget | None:
        """Get a widget from the Row or Node of a ListSource or TreeSource.

        If the value is a widget, it is returned, otherwise None is returned

        :param row: A row object from the underlying Source.
        :returns: The Widget to use, or None if no Widget.
        """
        return None


class AccessorColumn(Column[Value], Generic[Value]):
    """This is a column which implements accessor semantics.

    The value of a cell in an AccessorColumn is found by getting the value of
    the attribute on the row whose name matches the `accessor`. This value
    can be:

    This requires at least one of the heading and the accessor to be
    supplied to the init method. If given just a heading, it generates
    the accessor from the heading.

    The value provided by an accessor is interpreted as follows:

    - If the value is a [Widget][], that widget will be displayed in the cell.
      Note that this is currently a beta API: see the Notes section.
    - If the value is a [`tuple`][], it must have two elements: an icon, and a
      second element which will be interpreted as one of the options below.
    - Any other value will be converted into a string. If an icon has not already
      been provided in a tuple, it can also be provided using the value's `icon`
      attribute.

    Icon values must either be an [Icon][], which will be displayed on the left
    of the cell, or `None` to display no icon.
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
        super().__init__(heading)
        self._accessor = accessor

    def __eq__(self, other):
        if type(other) is type(self):
            return self._heading == other._heading and self._accessor == other._accessor
        return NotImplemented

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}(heading={self.heading!r}, accessor={self.accessor!r})"

    def __hash__(self):
        return hash((self.__class__, self._heading, self._accessor))

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

        If the value is a tuple, it must be of length two; the second item is assumed to
        be text.

        If the value is None, and a default is supplied, the default is returned.

        All other values are converted to a string by calling str().

        :param row: A row object from the underlying Source.
        :param default: A default value if the resulting value is otherwise None.
        :returns: The text to associated with this column's accessor, or None if no
            text.
        """
        match value := self.value(row):
            case Widget():
                return default
            case tuple((_, None)):
                return default
            case tuple((_, value)):
                return str(value)
            case tuple():
                raise ValueError("Data tuples must have length 2")
            case None:
                return default
            case _:
                return str(value)

    def icon(self, row: Row[Value]) -> Icon | None:
        """Get text from the Row or Node of a ListSource or TreeSource.

        If the value is a tuple, it must be of length 2, and the first item is assumed
        to be an Icon. A tuple of any other length will raise a ValueError. Otherwise if
        the item has an `icon` attribute, that is assumed to be the icon.

        :param row: A row object from the underlying Source.
        :returns: The Icon to associated with this column's accessor, or None if no
            Icon.
        """
        match value := self.value(row):
            case Widget():
                return None
            case tuple((icon, _)):
                return icon
            case tuple():
                raise ValueError("Data tuples must have length 2")
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
