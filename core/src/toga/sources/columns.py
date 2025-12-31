from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from .accessors import build_accessors, to_accessor


@runtime_checkable
class Column(Protocol):
    """Protocol that Column types must adhere to."""

    @property
    @abstractmethod
    def heading(self) -> str | None:
        """The heading text for this column, or None if no heading."""

    # This will eventually be removed from the Protocol
    @property
    @abstractmethod
    def accessor(self) -> str:
        """The accessor for this column."""


class AccessorColumn(Column):
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
        return self._heading

    @property
    def accessor(self):
        return self._accessor

    @classmethod
    def columns_from_headings_and_accessors(
        cls,
        headings: Iterable[str] | None = None,
        accessors: Iterable[str] | None = None,
    ) -> list[Column]:
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
