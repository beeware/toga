_hints = [
    "Any",
    "ContextManager",
    "Generic",
    "Literal",
    "NamedTuple",
    "NoReturn",
    "Protocol",
    "SupportsFloat",
    "SupportsInt",
    "TypeAlias",
    "TypeVar",
    "Union",
]

__all__ = _hints + ["TYPE_CHECKING"]


TYPE_CHECKING = False

for cls_name in _hints:
    globals()[cls_name] = type(cls_name, (object,), {})
