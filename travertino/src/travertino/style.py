from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from contextlib import contextmanager
from warnings import filterwarnings, warn

from .properties.shorthand import directional_property
from .properties.validated import validated_property

# Make sure deprecation warnings are shown by default
filterwarnings("default", category=DeprecationWarning)


class BaseStyle:
    """A base class for style declarations.

    Exposes a dict-like interface. Designed for subclasses to be decorated
    with @dataclass(kw_only=True, repr=False).

    The kw_only parameter was added in Python 3.10; for 3.9, init=False can be used
    instead to still get the keyword-only behavior from the included __init__.

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

    ########################################################################
    # 03-2025: Backwards compatibility for Toga < 0.5.0 *and* for Python 3.9
    ########################################################################

    # Fallback in case subclass isn't decorated as dataclass (probably from using
    # previous API) or for pre-3.10, before kw_only argument existed.
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
            try:
                self.apply()
            ######################################################################
            # 10-2024: Backwards compatibility for Toga < 0.5.0
            ######################################################################
            except Exception:
                warn(
                    (
                        "Failed to apply style when assigning applicator, or when "
                        "assigning a new style once applicator is present. Node should "
                        "be sufficiently initialized to apply its style before it is "
                        "assigned an applicator. This will be an exception in a future "
                        "version.\n"
                        "This error probably means you've updated Travertino to 0.5.0 "
                        "but are still using Toga <= 0.4.8; to fix, either update Toga "
                        "to >= 0.5.0, or pin Travertino to 0.3.0."
                    ),
                    RuntimeWarning,
                    stacklevel=2,
                )
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
                    "applicator afterward on the returned copy.\n"
                    "This error probably means you've updated Travertino to 0.5.0 but "
                    "are still using Toga <= 0.4.8; to fix, either update Toga to >= "
                    "0.5.0, or pin Travertino to 0.3.0."
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

    def _apply(self, names: set):
        raise NotImplementedError(
            "Style must define an _apply method"
        )  # pragma: no cover

    def layout(self, viewport):
        raise NotImplementedError(
            "Style must define a layout method"
        )  # pragma: no cover

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
        if name in self._ALL_PROPERTIES:
            return getattr(self, name)
        raise KeyError(name)

    def __setitem__(self, name, value):
        name = name.replace("-", "_")
        if name in self._ALL_PROPERTIES:
            setattr(self, name, value)
        else:
            raise KeyError(name)

    def __delitem__(self, name):
        name = name.replace("-", "_")
        if name in self._ALL_PROPERTIES:
            delattr(self, name)
        else:
            raise KeyError(name)

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
    # Backwards compatibility
    ######################################################################

    def reapply(self):
        warn(
            (
                "BaseStyle.reapply() is deprecated; call .apply with no arguments "
                "instead.\n"
                "This error probably means you've updated Travertino to 0.5.0 but are "
                "still using Toga <= 0.4.8; to fix, either update Toga to >= 0.5.0, or "
                "pin Travertino to 0.3.0."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        self.apply()

    @classmethod
    def validated_property(cls, name, choices, initial=None):
        warn(
            (
                "Defining style properties with class methods is deprecated; use class "
                "attributes instead.\n"
                "This error probably means you've updated Travertino to 0.5.0 but are "
                "still using Toga <= 0.4.8; to fix, either update Toga to >= 0.5.0, or "
                "pin Travertino to 0.3.0."
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
                "attributes instead.\n"
                "This error probably means you've updated Travertino to 0.5.0 but are "
                "still using Toga <= 0.4.8; to fix, either update Toga to >= 0.5.0, or "
                "pin Travertino to 0.3.0."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        name_format = name % "{}"
        name = name_format.format("")
        prop = directional_property(name_format)
        setattr(cls, name, prop)
        prop.__set_name__(cls, name)
