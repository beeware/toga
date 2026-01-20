from .accessors import to_accessor  # noqa: F401
from .base import (  # noqa: F401
    ListListener,
    Source,
    TreeListener,
    ValueListener,
)
from .list_source import ListSource, ListSourceT, Row  # noqa: F401
from .tree_source import Node, TreeSource, TreeSourceT  # noqa: F401
from .value_source import ValueSource  # noqa: F401

__all__ = [
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
