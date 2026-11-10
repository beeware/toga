from .accessors import to_accessor
from .base import (
    ListListener,
    Source,
    TreeListener,
    ValueListener,
)
from .columns import AccessorColumn, Column, ColumnT
from .list_source import ListSource, ListSourceT, Row
from .tree_source import Node, TreeSource, TreeSourceT
from .value_source import ValueSource

__all__ = [
    "AccessorColumn",
    "Column",
    "ColumnT",
    "ListListener",
    "ListSource",
    "ListSourceT",
    "Listener",
    "Node",
    "Row",
    "Source",
    "TreeListener",
    "TreeSource",
    "TreeSourceT",
    "ValueListener",
    "ValueSource",
    "to_accessor",
]


def __getattr__(name):
    if name == "Listener":
        # Alias for backwards compatibility:
        # Jan 2025: In 0.5.3 and earlier, ListListener was named Listener
        global Listener
        from .base import Listener

        return Listener
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
