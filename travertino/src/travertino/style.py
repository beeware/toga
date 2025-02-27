from collections import defaultdict
from collections.abc import Mapping
from warnings import filterwarnings, warn

from .properties.shorthand import directional_property
from .properties.validated import validated_property

# Make sure deprecation warnings are shown by default
filterwarnings("default", category=DeprecationWarning)


class BaseStyle:
    """A base class for style declarations.

    Exposes a dict-like interface. Designed for subclasses to be decorated
    with @dataclass(kw_only=True), which most IDEs should be able to interpret and
    provide autocompletion of argument names. On Python < 3.10, init=False can be used
    to still get the keyword-only behavior from the included __init__.
    """

    _BASE_PROPERTIES = defaultdict(set)
    _BASE_ALL_PROPERTIES = defaultdict(set)

    def __init_subclass__(cls):
        # Give the subclass a direct reference to its properties.
        cls._PROPERTIES = cls._BASE_PROPERTIES[cls]
        cls._ALL_PROPERTIES = cls._BASE_ALL_PROPERTIES[cls]

    # Fallback in case subclass isn't decorated as dataclass (probably from using
    # previous API) or for pre-3.10, before kw_only argument existed.
    def __init__(self, **properties):
        self.update(**properties)

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
                    "Failed to apply style when assigning applicator, or when "
                    "assigning a new style once applicator is present. Node should be "
                    "sufficiently initialized to apply its style before it is assigned "
                    "an applicator. This will be an exception in a future version.\n"
                    "This error probably means you've updated Travertino to 0.5.0 but "
                    "are still using Toga <= 0.4.8; to fix, either update Toga to "
                    ">= 0.5.0, or pin Travertino to 0.3.0.",
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
                "Providing an applicator to BaseStyle.copy() is deprecated. Set "
                "applicator afterward on the returned copy.\n"
                "This error probably means you've updated Travertino to 0.5.0 but are "
                "still using Toga <= 0.4.8; to fix, either update Toga to >= 0.5.0, or "
                "pin Travertino to 0.3.0.",
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

    def apply(self, name):
        raise NotImplementedError(
            "Style must define an apply method"
        )  # pragma: no cover

    def layout(self, viewport):
        raise NotImplementedError(
            "Style must define a layout method"
        )  # pragma: no cover

    ######################################################################
    # Provide a dict-like interface
    ######################################################################

    def update(self, **properties):
        """Set multiple styles on the style definition."""
        for name, value in properties.items():
            name = name.replace("-", "_")
            if name not in self._ALL_PROPERTIES:
                raise NameError(f"Unknown style '{name}'")

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
        return name in self._ALL_PROPERTIES and (
            getattr(self.__class__, name).is_set_on(self)
        )

    def __iter__(self):
        yield from (name for name in self._PROPERTIES if name in self)

    def __or__(self, other):
        if isinstance(other, BaseStyle):
            if self.__class__ is not other.__class__:
                return NotImplemented
        elif not isinstance(other, Mapping):
            return NotImplemented

        result = self.copy()
        result.update(**other)
        return result

    def __ior__(self, other):
        if isinstance(other, BaseStyle):
            if self.__class__ is not other.__class__:
                return NotImplemented
        elif not isinstance(other, Mapping):
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

    ######################################################################
    # Backwards compatibility
    ######################################################################

    def reapply(self):
        warn(
            "BaseStyle.reapply() is deprecated; call .apply with no arguments "
            "instead.\n"
            "This error probably means you've updated Travertino to 0.5.0 but are "
            "still using Toga <= 0.4.8; to fix, either update Toga to >= 0.5.0, or pin "
            "Travertino to 0.3.0.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.apply()

    @classmethod
    def validated_property(cls, name, choices, initial=None):
        warn(
            "Defining style properties with class methods is deprecated; use class "
            "attributes instead.\n"
            "This error probably means you've updated Travertino to 0.5.0 but are "
            "still using Toga <= 0.4.8; to fix, either update Toga to >= 0.5.0, or pin "
            "Travertino to 0.3.0.",
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
            "Defining style properties with class methods is deprecated; use class "
            "attributes instead.\n"
            "This error probably means you've updated Travertino to 0.5.0 but are "
            "still using Toga <= 0.4.8; to fix, either update Toga to >= 0.5.0, or pin "
            "Travertino to 0.3.0.",
            DeprecationWarning,
            stacklevel=2,
        )
        name_format = name % "{}"
        name = name_format.format("")
        prop = directional_property(name_format)
        setattr(cls, name, prop)
        prop.__set_name__(cls, name)
