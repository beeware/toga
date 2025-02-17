from collections import defaultdict
from collections.abc import Mapping, Sequence
from warnings import filterwarnings, warn

from .colors import color
from .constants import BOTTOM, LEFT, RIGHT, TOP

# Make sure deprecation warnings are shown by default
filterwarnings("default", category=DeprecationWarning)


class ImmutableList:
    def __init__(self, iterable):
        self._data = list(iterable)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __eq__(self, other):
        return self._data == other

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __reversed__(self):
        return reversed(self._data)

    def index(self, value):
        return self._data.index(value)

    def count(self, value):
        return self._data.count(value)


Sequence.register(ImmutableList)


class Choices:
    "A class to define allowable data types for a property"

    def __init__(
        self,
        *constants,
        string=False,
        integer=False,
        number=False,
        color=False,
    ):
        self.constants = set(constants)

        self.string = string
        self.integer = integer
        self.number = number
        self.color = color

        self._options = sorted(str(c).lower().replace("_", "-") for c in self.constants)
        if self.string:
            self._options.append("<string>")
        if self.integer:
            self._options.append("<integer>")
        if self.number:
            self._options.append("<number>")
        if self.color:
            self._options.append("<color>")

    def validate(self, value):
        if self.string:
            try:
                return value.strip()
            except AttributeError:
                pass
        if self.integer:
            try:
                return int(value)
            except (ValueError, TypeError):
                pass
        if self.number:
            try:
                return float(value)
            except (ValueError, TypeError):
                pass
        if self.color:
            try:
                return color(value)
            except ValueError:
                pass
        for const in self.constants:
            if value == const:
                return const

        raise ValueError(f"{value!r} is not a valid value")

    def __str__(self):
        return ", ".join(self._options)


class validated_property:
    def __init__(
        self,
        *constants,
        string=False,
        integer=False,
        number=False,
        color=False,
        initial=None,
    ):
        """Define a simple validated property attribute.

        :param constants: Explicitly allowable values.
        :param string: Are strings allowed as values?
        :param integer: Are integers allowed as values?
        :param number: Are numbers allowed as values?
        :param color: Are colors allowed as values?
        :param initial: The initial value for the property. If the property has not been
            explicitly set, this is what is returned when it's accessed.
        """
        self.choices = Choices(
            *constants, string=string, integer=integer, number=number, color=color
        )
        self.initial = None if initial is None else self.validate(initial)

    def __set_name__(self, owner, name):
        self.name = name
        owner._BASE_PROPERTIES[owner].add(name)
        owner._BASE_ALL_PROPERTIES[owner].add(name)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        return getattr(obj, f"_{self.name}", self.initial)

    def __set__(self, obj, value):
        if value is self:
            # This happens during autogenerated dataclass __init__ when no value is
            # supplied.
            return

        if value is None:
            raise ValueError(
                "Python `None` cannot be used as a style value; "
                f"to reset a property, use del `style.{self.name}`."
            )

        value = self.validate(value)

        if (current := getattr(obj, f"_{self.name}", None)) is None:
            # If the value has not been explicitly set already, then we always want to
            # assign to the attribute -- even if the value being assigned is identical
            # to the initial value.
            setattr(obj, f"_{self.name}", value)
            if value != self.initial:
                obj.apply(self.name)

        elif value != current:
            setattr(obj, f"_{self.name}", value)
            obj.apply(self.name)

    def __delete__(self, obj):
        try:
            delattr(obj, f"_{self.name}")
        except AttributeError:
            pass
        else:
            obj.apply(self.name)

    @property
    def _name_if_set(self):
        return f" {self.name}" if hasattr(self, "name") else ""

    def validate(self, value):
        try:
            return self.choices.validate(value)
        except ValueError:
            raise ValueError(
                f"Invalid value {value!r} for property{self._name_if_set}; "
                f"Valid values are: {self.choices}"
            )

    def is_set_on(self, obj):
        return hasattr(obj, f"_{self.name}")


class list_property(validated_property):
    def validate(self, value):
        if isinstance(value, str):
            value = [value]
        elif not isinstance(value, Sequence):
            raise TypeError(
                f"Value for list property{self._name_if_set} must be a sequence."
            )

        if not value:
            name = getattr(self, "name", "prop_name")
            raise ValueError(
                "List properties cannot be set to an empty sequence; "
                f"to reset a property, use del `style.{name}`."
            )

        # This could be a comprehension, but then the error couldn't specify which value
        # is at fault.
        result = []
        for item in value:
            try:
                item = self.choices.validate(item)
            except ValueError:
                raise ValueError(
                    f"Invalid item value {item!r} for list "
                    f"property{self._name_if_set}; Valid values are: {self.choices}"
                )
            result.append(item)

        return ImmutableList(result)


class directional_property:
    DIRECTIONS = [TOP, RIGHT, BOTTOM, LEFT]
    ASSIGNMENT_SCHEMES = {
        #   T  R  B  L
        1: [0, 0, 0, 0],
        2: [0, 1, 0, 1],
        3: [0, 1, 2, 1],
        4: [0, 1, 2, 3],
    }

    def __init__(self, name_format):
        """Define a property that proxies for top/right/bottom/left alternatives.

        :param name_format: The format from which to generate subproperties. "{}" will
            be replaced with "_top", etc.
        """
        self.property_names = [
            name_format.format(f"_{direction}") for direction in self.DIRECTIONS
        ]

    def __set_name__(self, owner, name):
        self.name = name
        owner._BASE_ALL_PROPERTIES[owner].add(self.name)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        return tuple(obj[name] for name in self.property_names)

    def __set__(self, obj, value):
        if value is self:
            # This happens during autogenerated dataclass __init__ when no value is
            # supplied.
            return

        if not isinstance(value, tuple):
            value = (value,)

        if order := self.ASSIGNMENT_SCHEMES.get(len(value)):
            for name, index in zip(self.property_names, order):
                obj[name] = value[index]
        else:
            raise ValueError(
                f"Invalid value for '{self.name}'; value must be a number, or a 1-4 "
                f"tuple."
            )

    def __delete__(self, obj):
        for name in self.property_names:
            del obj[name]

    def is_set_on(self, obj):
        return any(hasattr(obj, name) for name in self.property_names)


class BaseStyle:
    """A base class for style declarations.

    Exposes a dict-like interface. Designed for subclasses to be decorated
    with @dataclass(kw_only=True), which most IDEs should be able to interpret and
    provide autocompletion of argument names. On Python < 3.10, init=False can be used
    to still get the keyword-only behavior from the included __init__.
    """

    _BASE_PROPERTIES = defaultdict(set)
    _BASE_ALL_PROPERTIES = defaultdict(set)

    # Give instances a direct reference to their properties.

    @property
    def _PROPERTIES(self):
        return self._BASE_PROPERTIES[type(self)]

    @property
    def _ALL_PROPERTIES(self):
        return self._BASE_ALL_PROPERTIES[type(self)]

    # Fallback in case subclass isn't decorated as subclass (probably from using
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
