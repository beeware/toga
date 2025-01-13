from .constants import (
    BOLD,
    FONT_STYLES,
    FONT_VARIANTS,
    FONT_WEIGHTS,
    ITALIC,
    NORMAL,
    OBLIQUE,
    SMALL_CAPS,
    SYSTEM_DEFAULT_FONT_SIZE,
)


class Font:
    def __init__(self, family, size, style=NORMAL, variant=NORMAL, weight=NORMAL):
        if (family[0] == "'" and family[-1] == "'") or (
            family[0] == '"' and family[-1] == '"'
        ):
            self.family = family[1:-1]
        else:
            self.family = family

        try:
            self.size = int(size)
        except ValueError:
            try:
                if size.strip().endswith("pt"):
                    self.size = int(size[:-2])
                else:
                    raise ValueError(f"Invalid font size {size!r}")
            except Exception:
                raise ValueError(f"Invalid font size {size!r}")
        self.style = style if style in FONT_STYLES else NORMAL
        self.variant = variant if variant in FONT_VARIANTS else NORMAL
        self.weight = weight if weight in FONT_WEIGHTS else NORMAL

    def __hash__(self):
        return hash(
            ("FONT", self.family, self.size, self.style, self.variant, self.weight)
        )

    def __repr__(self):
        return "<Font: {}{}{}{} {}>".format(
            "" if self.style is NORMAL else (self.style + " "),
            "" if self.variant is NORMAL else (self.variant + " "),
            "" if self.weight is NORMAL else (self.weight + " "),
            (
                "system default size"
                if self.size == SYSTEM_DEFAULT_FONT_SIZE
                else f"{self.size}pt"
            ),
            self.family,
        )

    def __eq__(self, other):
        try:
            return (
                self.family == other.family
                and self.size == other.size
                and self.style == other.style
                and self.variant == other.variant
                and self.weight == other.weight
            )
        except AttributeError:
            return False

    def normal_style(self):
        "Generate a normal style version of this font"
        return Font(
            self.family,
            self.size,
            style=NORMAL,
            variant=self.variant,
            weight=self.weight,
        )

    def italic(self):
        "Generate an italic version of this font"
        return Font(
            self.family,
            self.size,
            style=ITALIC,
            variant=self.variant,
            weight=self.weight,
        )

    def oblique(self):
        "Generate an oblique version of this font"
        return Font(
            self.family,
            self.size,
            style=OBLIQUE,
            variant=self.variant,
            weight=self.weight,
        )

    def normal_variant(self):
        "Generate a normal variant of this font"
        return Font(
            self.family, self.size, style=self.style, variant=NORMAL, weight=self.weight
        )

    def small_caps(self):
        "Generate a small-caps variant of this font"
        return Font(
            self.family,
            self.size,
            style=self.style,
            variant=SMALL_CAPS,
            weight=self.weight,
        )

    def normal_weight(self):
        "Generate a normal weight version of this font"
        return Font(
            self.family,
            self.size,
            style=self.style,
            variant=self.variant,
            weight=NORMAL,
        )

    def bold(self):
        "Generate a bold version of this font"
        return Font(
            self.family, self.size, style=self.style, variant=self.variant, weight=BOLD
        )


def font(value):
    """Parse a font from a string.

    Accepts:
    * Font instances

    style: normal / italic / oblique
    variant: normal / small-caps
    weight: normal / bold

    style variant weight size family
    variant weight size family
    weight size family
    size family
    """

    if isinstance(value, Font):
        return value

    elif isinstance(value, str):
        parts = value.split(" ")

        style = None
        variant = None
        weight = None
        size = None

        while size is None:
            part = parts.pop(0)
            if part == NORMAL:
                if style is None:
                    style = NORMAL
                elif variant is None:
                    variant = NORMAL
                elif weight is None:
                    weight = NORMAL
            elif part in FONT_STYLES:
                if style is not None:
                    raise ValueError(f"Invalid font declaration '{value}'")
                style = part
            elif part in FONT_VARIANTS:
                if variant is not None:
                    raise ValueError(f"Invalid font declaration '{value}'")
                if style is None:
                    style = NORMAL
                variant = part
            elif part in FONT_WEIGHTS:
                if weight is not None:
                    raise ValueError(f"Invalid font declaration '{value}'")
                if style is None:
                    style = NORMAL
                if variant is None:
                    variant = NORMAL
                weight = part
            else:
                try:
                    if part.endswith("pt"):
                        size = int(part[:-2])
                    else:
                        size = int(part)
                except ValueError:
                    raise ValueError(f"Invalid size in font declaration '{value}'")

                if parts[0] == "pt":
                    parts.pop(0)

        family = " ".join(parts)
        return Font(family, size, style=style, variant=variant, weight=weight)

    raise ValueError("Unknown font '%s'" % value)
