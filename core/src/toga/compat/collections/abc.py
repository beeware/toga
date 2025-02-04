# MicroPython apparently doesn't provide any way to create an object T such that both
# `T` and `T[args]` evaluate to a usable type object:
#
# * Regular classes don't accept [] syntax.
# * __class_getitem__ isn't supported at all.
# * A metaclass with a __getitem__ method can be instantiated into a class, but that
#   class can't be used as the base of another class.
#
# This doesn't matter in type annotations, because they aren't evaluated anyway, but it
# does matter for declarations such as `class DocumentSet(Sequence[Document])`. So we
# prioritize the [] syntax to support that.
#
# This means that expressions like `isinstance(x, Sequence)` won't work, and will need
# to be replaced with hasattr checks. But that would probably be necessary anyway,
# because I don't think MicroPython has enough ABC support for even a standard list to
# be treated as an instance of Sequence.
#
# This approach should also allow our ABCs to include a proper inheritance hierarchy and
# mixin methods, once that becomes necessary.

__all__ = [  # noqa: F822
    "Container",
    "Iterable",
    "Iterator",
    "Generator",
    "Callable",
    "Collection",
    "Sequence",
    "MutableSequence",
    "Set",
    "MutableSet",
    "Mapping",
    "MutableMapping",
    "Awaitable",
    "Coroutine",
]


class _SubscriptWrapper:
    def __init__(self, abc_cls):
        self.abc_cls = abc_cls

    def __getitem__(self, key):
        return self.abc_cls

    def register(self, cls):
        pass


for cls_name in __all__:
    globals()[cls_name] = _SubscriptWrapper(type(cls_name, (object,), {}))
