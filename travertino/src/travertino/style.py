from __future__ import annotations

from abc import ABC
from collections import defaultdict
from collections.abc import Mapping
from contextlib import contextmanager
from warnings import filterwarnings, warn

from .compat import _toga_lt_5
from .properties.shorthand import directional_property
from .properties.validated import validated_property

# Make sure deprecation warnings are shown by default
filterwarnings("default", category=DeprecationWarning)

_DEPRECATION_MSG = (
    "You're probably seeing this because you've updated Travertino to 0.5.x but are "
    "using Toga <= 0.4.8; to fix, either update Toga to >= 0.5.0, or pin Travertino to "
    "0.3.0."
)


# 2026-1: Backwards compatibility for Toga < 0.5.0; can eventually remove noqa
class BaseStyle(ABC):  # noqa: B024
    """A base class for style declarations.

    Exposes a dict-like interface. Designed for subclasses to be decorated
    with @dataclass(kw_only=True, repr=False).

    Most IDEs should see the dataclass decorator and provide autocompletion / type hints
    for parameters to the constructor.
    """

    # Only "real" properties
    _BASE_PROPERTIES = defaultdict(set)
    # Includes aliases and shorthands
    _BASE_ALL_PROPERTIES = defaultdict(set)

    def __init_subclass__(cls):
        # Give the subclass a direct reference to its properties.
        cls._PROPERTIES = cls._BASE_PROPERTIES[cls]
        cls._ALL_PROPERTIES = cls._BASE_ALL_PROPERTIES[cls]

    ###################################################
    # 03-2025: Backwards compatibility for Toga < 0.5.0
    ###################################################

    # Fallback in case subclass isn't decorated as dataclass (probably from using
    # previous API).
    def __init__(self, **properties):
        try:
            self.update(**properties)
            self.__post_init__()
        except NameError as error:
            # It still makes sense for update() to raise a NameError. However, here we
            # simulate the behavior of the dataclass-generated __init__() for
            # consistency.
            for name in properties:
                # This is redoing work, but it should only ever happen when a property
                # name is invalid, and only in outdated Python or Toga, and only once.
                if name not in self._ALL_PROPERTIES:
                    raise TypeError(
                        f"{type(self).__name__}.__init__() got an unexpected keyword "
                        f"argument '{name}'"
                    ) from error
            # The above for loop should never run to completion, so that needs to be
            # excluded from coverage.
            else:  # pragma: no cover
                pass

    ######################################################################
    # End backwards compatibility
    ######################################################################

    @property
    def _applicator(self):
        return getattr(self, "_assigned_applicator", None)

    @_applicator.setter
    def _applicator(self, value):
        self._assigned_applicator = value

        if value is not None:
            ######################################################################
            # 8-2025: Backwards compatibility for Toga < 0.5.0
            ######################################################################

            # Once this shim is removed, it still wouldn't be a bad idea to raise the
            # more specific RuntimeError.

            try:
                # By default, call the apply(). In the event of a TypeError, if Toga's <
                # 0.5.0, silently pass, since properties can't be successfully applied
                # yet. (They'll all get applied later, in each backend.)
                try:
                    self.apply()
                except TypeError:
                    if _toga_lt_5():  # pragma: no cover
                        # Style properties can't be applied yet.
                        pass
                    else:
                        raise

            except Exception as exc:
                msg = (
                    "Failed to apply style when assigning applicator, or when "
                    "assigning a new style once applicator is present. Node should "
                    "be sufficiently initialized to apply its style before it is "
                    "assigned an applicator."
                )
                if _toga_lt_5():  # pragma: no cover
                    import toga

                    if isinstance(value.node, toga.Widget):
                        warn(
                            (
                                f"{msg}\n{_DEPRECATION_MSG}\n"
                                "This will be an exception in a future version."
                            ),
                            RuntimeWarning,
                            stacklevel=2,
                        )
                        return
                # If either Toga's >= 0.5.0 *or* the node isn't a Toga widget, raise the
                # exception.
                raise RuntimeError(msg) from exc

                ######################################################################
                # End backwards compatibility
                ######################################################################

    def copy(self, applicator=None):
        """Create a duplicate of this style declaration."""
        dup = self.__class__()
        dup.update(**self)

        ######################################################################
        # 10-2024: Backwards compatibility for Toga < 0.5.0
        ######################################################################

        if applicator is not None:
            warn(
                (
                    "Providing an applicator to BaseStyle.copy() is deprecated. Set "
                    f"applicator afterward on the returned copy.\n{_DEPRECATION_MSG}"
                ),
                DeprecationWarning,
                stacklevel=2,
            )
            dup._applicator = applicator

        ######################################################################
        # End backwards compatibility
        ######################################################################

        return dup

    ######################################################################
    # Interface that style declarations must define
    ######################################################################

    def _apply(self, names: set):  # pragma: no cover
        """Apply the properties whose names are supplied."""

        # 2026-1: Backwards compatibility for Toga < 0.5.0: This should eventually be
        # marked as @abstractmethod, and the error and no-cover removed.
        raise NotImplementedError

    def layout(self, viewport):  # pragma: no cover
        """Lay out this style's node in the supplied viewport."""

        # 2026-1: Backwards compatibility for Toga < 0.5.0: This should eventually be
        # marked as @abstractmethod, and the error and no-cover removed.
        raise NotImplementedError

    ######################################################################
    # Support for batching calls to apply()
    ######################################################################

    def __post_init__(self):
        # Because batch_apply is a no-op with no applicator, it's fine that these aren't
        # set during the dataclass-generated __init__ — even when directional/composite
        # properties (which call batch_apply) are set.
        self._batched_mode = False
        self._batched_names = set()

    # After deprecation is removed, this should be the signature:
    # def apply(self, name: str | None = None) -> None:
    def apply(self, *names: list[str]) -> None:
        if not self._applicator:
            return

        ######################################################################
        # 03-2025: Backwards compatibility for Toga 0.5.1
        ######################################################################

        if len(names) > 1:
            cls = type(self).__name__
            warn(
                (
                    f"Calling {cls}.apply() with multiple arguments is deprecated. "
                    f'Use the "with {cls}.batch_apply():" context manager instead.'
                ),
                DeprecationWarning,
                stacklevel=2,
            )

        if self._batched_mode:
            self._batched_names.update(names)
        else:
            self._apply({*names} if names else self._PROPERTIES)

        ######################################################################
        # End backwards compatibility
        ######################################################################

        # if self._batched_mode:
        #     self._batched_names.add(name)
        # else:
        #     self._apply({name} if name else self._PROPERTIES)

    @contextmanager
    def batch_apply(self):
        """Aggregate calls to appl() into one single call to _apply().

        No-op if no applicator is present, or if already in batched mode.
        """
        # Short-circuit out if no applicator is set. This avoids trying to access the
        # nonexistent _batched_mode during __init__.
        if batch_entered := self._applicator and not self._batched_mode:
            self._batched_mode = True

        try:
            yield
        finally:
            if batch_entered:
                self._batched_mode = False

                if self._batched_names:
                    self._apply(self._batched_names)
                    self._batched_names.clear()

    ######################################################################
    # Provide a dict-like interface
    ######################################################################

    def update(self, **properties):
        """Set multiple styles on the style definition."""
        # Some aliases may be valid only in the presence of other property values, or
        # depend on other values to determine what to alias to. This update might be
        # setting those prerequisite properties. So we need to defer setting any
        # conditional aliases until last.
        deferred_aliases = {}

        with self.batch_apply():
            for name, value in properties.items():
                name = name.replace("-", "_")
                if name not in self._ALL_PROPERTIES:
                    raise NameError(f"Unknown property '{name}'")

                prop = getattr(type(self), name)
                if isinstance(getattr(prop, "source", None), dict):
                    deferred_aliases[name] = value
                else:
                    self[name] = value

            for name, value in deferred_aliases.items():
                self[name] = value

    def __getitem__(self, name):
        name = name.replace("-", "_")
        if name not in self._ALL_PROPERTIES:
            raise KeyError(name)
        return getattr(self, name)

    def __setitem__(self, name, value):
        name = name.replace("-", "_")
        if name not in self._ALL_PROPERTIES:
            raise KeyError(name)
        setattr(self, name, value)

    def __delitem__(self, name):
        name = name.replace("-", "_")
        if name not in self._ALL_PROPERTIES:
            raise KeyError(name)
        delattr(self, name)

    def keys(self):
        return {*self}

    def items(self):
        return [(name, self[name]) for name in self]

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, name):
        name = name.replace("-", "_")
        return name in self._ALL_PROPERTIES and (
            getattr(self.__class__, name).is_set_on(self)
        )

    def __iter__(self):
        yield from (name for name in self._PROPERTIES if name in self)

    def __or__(self, other):
        if not (type(self) is type(other) or isinstance(other, Mapping)):
            return NotImplemented

        result = self.copy()
        result.update(**other)
        return result

    def __ior__(self, other):
        if not (type(self) is type(other) or isinstance(other, Mapping)):
            return NotImplemented

        self.update(**other)
        return self

    ######################################################################
    # Get the rendered form of the style declaration
    ######################################################################

    def __str__(self):
        return "; ".join(
            f"{name.replace('_', '-')}: {value}" for name, value in sorted(self.items())
        )

    def __repr__(self):
        properties = ", ".join(
            f"{name}={repr(value)}" for name, value in sorted(self.items())
        )
        return f"{type(self).__name__}({properties})"

    ######################################################################
    # Backwards compatibility for Toga < 0.5.0
    ######################################################################

    def reapply(self):
        warn(
            (
                "BaseStyle.reapply() is deprecated; call .apply with no arguments "
                f"instead.\n{_DEPRECATION_MSG}"
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        for prop_name in self._PROPERTIES:
            self.apply(prop_name, self[prop_name])

    @classmethod
    def validated_property(cls, name, choices, initial=None):
        warn(
            (
                "Defining style properties with class methods is deprecated; use class "
                f"attributes instead.\n{_DEPRECATION_MSG}"
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        prop = validated_property(
            *choices.constants,
            string=choices.string,
            integer=choices.integer,
            number=choices.number,
            color=choices.color,
            initial=initial,
        )
        setattr(cls, name, prop)
        prop.__set_name__(cls, name)

    @classmethod
    def directional_property(cls, name):
        warn(
            (
                "Defining style properties with class methods is deprecated; use class "
                f"attributes instead.\n{_DEPRECATION_MSG}"
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        name_format = name % "{}"
        name = name_format.format("")
        prop = directional_property(name_format)
        setattr(cls, name, prop)
        prop.__set_name__(cls, name)
