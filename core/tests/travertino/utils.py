import sys
from dataclasses import dataclass
from unittest.mock import Mock

if sys.version_info < (3, 10):
    _DATACLASS_KWARGS = {"init": False}
else:
    _DATACLASS_KWARGS = {"kw_only": True}


def prep_style_class(cls):
    """Decorator to apply dataclass and mock apply."""
    return mock_attr("apply")(dataclass(**_DATACLASS_KWARGS)(cls))


def mock_attr(attr):
    """Mock an arbitrary attribute of a class."""

    def returned_decorator(cls):
        orig_init = cls.__init__

        def __init__(self, *args, **kwargs):
            setattr(self, attr, Mock())
            orig_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return returned_decorator
