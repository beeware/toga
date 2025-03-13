from ..colors import color


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
