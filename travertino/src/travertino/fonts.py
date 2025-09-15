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
            except Exception as exc:
                raise ValueError(f"Invalid font size {size!r}") from exc
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
