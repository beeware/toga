from ..constants import BOTTOM, LEFT, RIGHT, TOP


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
        return any(name in obj for name in self.property_names)
