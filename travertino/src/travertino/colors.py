from __future__ import annotations

# flake8: NOQA: F405
from .constants import *


class Color:
    "A base class for all colorspace representations."

    def __eq__(self, other):
        try:
            c1 = self.rgba
            c2 = other.rgba

            return c1.r == c2.r and c1.g == c2.g and c1.b == c2.b and c1.a == c2.a
        except AttributeError:
            return False

    @classmethod
    def _validate_between(cls, content_name, value, min_value, max_value):
        if value < min_value or value > max_value:
            raise ValueError(
                "{} value should be between {}-{}. Got {}".format(
                    content_name, min_value, max_value, value
                )
            )

    @classmethod
    def _validate_partial(cls, content_name, value):
        cls._validate_between(content_name, value, 0, 1)

    @classmethod
    def _validate_alpha(cls, value):
        cls._validate_partial("alpha", value)

    def blend_over(
        self,
        back_color: Color,
        round_to_nearest_int: bool = True,
    ) -> rgba:
        """Performs the "over" straight alpha blending operation, compositing
        the front color over the back color.

        **Straight alpha blending** is not the same as
        **Premultiplied alpha blending**, see:
        https://en.wikipedia.org/wiki/Alpha_compositing#Straight_versus_premultiplied

        :param back_color: The background color.
        :param round_to_nearest_int: Should the rgb values of the blended color be
            rounded to the nearest int? If the blended color will be later
            deblended to get the original front color, then keeping the decimal
            precision will give a more accurate value of the original front
            color.

        :returns: The blended color.
        """
        # The blending operation implemented here is the "over" operation and
        # replicates CSS's rgba mechanism. For the formulae used here, see:
        # https://en.wikipedia.org/wiki/Alpha_compositing#Description

        # Convert the input colors to rgba in order to do the calculation.
        front_color = self.rgba
        back_color = back_color.rgba

        if front_color.a == 1:
            # If the front color is fully opaque then the result will be the same as
            # front color.
            return front_color.rgba

        blended_alpha = min(
            1, max(0, (front_color.a + ((1 - front_color.a) * back_color.a)))
        )

        if blended_alpha == 0:
            # Don't further blend the color, to prevent divide by 0.
            return rgba(0, 0, 0, 0)
        else:
            blended_color = rgba(
                # Red Component
                min(
                    255,
                    max(
                        0,
                        (
                            (
                                (front_color.r * front_color.a)
                                + (back_color.r * back_color.a * (1 - front_color.a))
                            )
                            / blended_alpha
                        ),
                    ),
                ),
                # Green Component
                min(
                    255,
                    max(
                        0,
                        (
                            (
                                (front_color.g * front_color.a)
                                + (back_color.g * back_color.a * (1 - front_color.a))
                            )
                            / blended_alpha
                        ),
                    ),
                ),
                # Blue Component
                min(
                    255,
                    max(
                        0,
                        (
                            (
                                (front_color.b * front_color.a)
                                + (back_color.b * back_color.a * (1 - front_color.a))
                            )
                            / blended_alpha
                        ),
                    ),
                ),
                # Alpha component
                min(1, max(0, blended_alpha)),
            )
            if round_to_nearest_int:
                return rgba(
                    int(round(blended_color.r)),
                    int(round(blended_color.g)),
                    int(round(blended_color.b)),
                    round(blended_color.a, 2),
                )
            else:
                return blended_color.rgba

    def unblend_over(self, back_color: Color, front_color_alpha: float) -> rgba:
        """Performs the reverse of the "over" straight alpha blending operation,
        returning the front color.

        Note: Unblending of blended colors might produce front color with slightly
        imprecise component values compared to the original front color. This is
        due to the loss of some amount of precision during the calculation and
        conversion process between the different color formats. For example,
        unblending of a hsla blended color might might produce a slightly imprecise
        original front color, since the alpha blending and unblending is calculated
        after conversion to rgba values.

        :param blended_color: The blended color resultant from the alpha blending
         "over" operation, in the form of :any:`rgba()`.
        :param back_color: The background color.
        :param front_color_alpha: The original alpha value of the front color,
         within the range of (0, 1].

        :raises ValueError: If the value of :any:`front_color_alpha` is not within
         the range of (0, 1]. The value cannot be 0, since the blended color produced
         will be equal to the back color, and all information related to the front
         color will be lost.

        :returns: The original front color.
        """
        # The blending operation implemented here is the reverse of the "over"
        # operation and replicates CSS's rgba mechanism. The formula used here
        # are derived from the "over" straight alpha blending operation formula,
        # see: https://en.wikipedia.org/wiki/Alpha_compositing#Description

        blended_color = self.rgba
        back_color = back_color.rgba
        if not (0 < front_color_alpha <= 1):
            raise ValueError(
                "The value of front_color_alpha must be within the range of (0, 1]."
            )
        else:
            front_color = rgba(
                # Red Component
                min(
                    255,
                    max(
                        0,
                        (
                            (
                                (blended_color.r * blended_color.a)
                                - (
                                    back_color.r
                                    * back_color.a
                                    * (1 - front_color_alpha)
                                )
                            )
                            / front_color_alpha
                        ),
                    ),
                ),
                # Green Component
                min(
                    255,
                    max(
                        0,
                        (
                            (
                                (blended_color.g * blended_color.a)
                                - (
                                    back_color.g
                                    * back_color.a
                                    * (1 - front_color_alpha)
                                )
                            )
                            / front_color_alpha
                        ),
                    ),
                ),
                # Blue Component
                min(
                    255,
                    max(
                        0,
                        (
                            (
                                (blended_color.b * blended_color.a)
                                - (
                                    back_color.b
                                    * back_color.a
                                    * (1 - front_color_alpha)
                                )
                            )
                            / front_color_alpha
                        ),
                    ),
                ),
                # Alpha Component
                front_color_alpha,
            )
            return front_color.rgba


class rgba(Color):
    "A representation of an RGBA color."

    def __init__(self, r, g, b, a):
        self._validate_rgb("red", r)
        self._validate_rgb("green", g)
        self._validate_rgb("blue", b)
        self._validate_alpha(a)
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __hash__(self):
        return hash(("RGBA-color", self.r, self.g, self.b, self.a))

    def __repr__(self):
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"

    @classmethod
    def _validate_rgb(cls, content_name, value):
        cls._validate_between(content_name, value, 0, 255)

    @property
    def rgba(self):
        return rgba(self.r, self.g, self.b, self.a)

    @property
    def rgb(self):
        return rgb(self.r, self.g, self.b)

    @property
    def hsla(self) -> hsla:
        # Formula used here is from: https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
        r_prime = self.r / 255
        g_prime = self.g / 255
        b_prime = self.b / 255

        max_component = max(r_prime, g_prime, b_prime)
        min_component = min(r_prime, g_prime, b_prime)
        value = max_component
        chroma = max_component - min_component

        lightness = (max_component + min_component) / 2

        if chroma == 0:
            hue = 0
        elif value == r_prime:
            hue = 60 * (((g_prime - b_prime) / chroma) % 6)
        elif value == g_prime:
            hue = 60 * (((b_prime - r_prime) / chroma) + 2)
        else:  # value == b_prime:
            hue = 60 * (((r_prime - g_prime) / chroma) + 4)

        if lightness in {0, 1}:
            saturation = 0
        else:
            saturation = chroma / (1 - abs((2 * value) - chroma - 1))

        return hsla(
            hue % 360,  # [0,360)
            min(1, max(0, saturation)),  # [0,1]
            min(1, max(0, lightness)),  # [0,1]
            min(1, max(0, self.a)),  # [0,1]
        )

    @property
    def hsl(self):
        return self.hsla.hsl


class rgb(rgba):
    "A representation of an RGB color"

    def __init__(self, r, g, b):
        super().__init__(r, g, b, 1.0)

    def __repr__(self):
        return f"rgb({self.r}, {self.g}, {self.b})"


class hsla(Color):
    "A representation of an HSLA color."

    def __init__(self, h, s, l, a=1.0):
        self._validate_between("hue", h, 0, 360)
        self._validate_partial("saturation", s)
        self._validate_partial("lightness", l)
        self._validate_alpha(a)
        self.h = h
        self.s = s
        self.l = l  # NOQA; E741
        self.a = a

    def __hash__(self):
        return hash(("HSLA-color", self.h, self.s, self.l, self.a))

    def __repr__(self):
        return f"hsla({self.h}, {self.s}, {self.l}, {self.a})"

    @property
    def hsla(self):
        return hsla(self.h, self.s, self.l, self.a)

    @property
    def hsl(self):
        return hsl(self.h, self.s, self.l)

    @property
    def rgba(self):
        c = (1.0 - abs(2.0 * self.l - 1.0)) * self.s
        h = self.h / 60.0
        x = c * (1.0 - abs(h % 2 - 1.0))
        m = self.l - 0.5 * c

        if h < 1.0:
            r, g, b = c + m, x + m, m
        elif h < 2.0:
            r, g, b = x + m, c + m, m
        elif h < 3.0:
            r, g, b = m, c + m, x + m
        elif h < 4.0:
            r, g, b = m, x + m, c + m
        elif h < 5.0:
            r, g, b = m, x + m, c + m
        else:
            r, g, b = c + m, m, x + m

        return rgba(
            round(r * 0xFF),
            round(g * 0xFF),
            round(b * 0xFF),
            self.a,
        )

    @property
    def rgb(self):
        return self.rgba.rgb


class hsl(hsla):
    "A representation of an HSL color"

    def __init__(self, h, s, l):
        super().__init__(h, s, l, 1.0)

    def __repr__(self):
        return f"hsl({self.h}, {self.s}, {self.l})"


def color(value):
    """Parse a color from a value.

    Accepts:
    * rgb() instances
    * hsl() instances
    * '#rgb'
    * '#rgba'
    * '#rrggbb'
    * '#rrggbbaa'
    * '#RGB'
    * '#RGBA'
    * '#RRGGBB'
    * '#RRGGBBAA'
    * 'rgb(0, 0, 0)'
    * 'rgba(0, 0, 0, 0.0)'
    * 'hsl(0, 0%, 0%)'
    * 'hsla(0, 0%, 0%, 0.0)'
    * A named color
    """

    if isinstance(value, Color):
        return value

    elif isinstance(value, str):
        if value[0] == "#":
            if len(value) == 4:
                return rgb(
                    r=int(value[1] + value[1], 16),
                    g=int(value[2] + value[2], 16),
                    b=int(value[3] + value[3], 16),
                )
            elif len(value) == 5:
                return rgba(
                    r=int(value[1] + value[1], 16),
                    g=int(value[2] + value[2], 16),
                    b=int(value[3] + value[3], 16),
                    a=int(value[4] + value[4], 16) / 0xFF,
                )
            elif len(value) == 7:
                return rgb(
                    r=int(value[1:3], 16),
                    g=int(value[3:5], 16),
                    b=int(value[5:7], 16),
                )
            elif len(value) == 9:
                return rgba(
                    r=int(value[1:3], 16),
                    g=int(value[3:5], 16),
                    b=int(value[5:7], 16),
                    a=int(value[7:9], 16) / 0xFF,
                )
        elif value.startswith("rgba"):
            try:
                values = value[5:-1].split(",")
                if len(values) == 4:
                    return rgba(
                        int(values[0]),
                        int(values[1]),
                        int(values[2]),
                        float(
                            values[3],
                        ),
                    )
            except ValueError:
                pass
        elif value.startswith("rgb"):
            try:
                values = value[4:-1].split(",")
                if len(values) == 3:
                    return rgb(
                        int(values[0]),
                        int(values[1]),
                        int(values[2]),
                    )
            except ValueError:
                pass

        elif value.startswith("hsla"):
            try:
                values = value[5:-1].split(",")
                if len(values) == 4:
                    return hsla(
                        int(values[0]),
                        int(values[1].strip().rstrip("%")) / 100.0,
                        int(values[2].strip().rstrip("%")) / 100.0,
                        float(values[3]),
                    )
            except ValueError:
                pass

        elif value.startswith("hsl"):
            try:
                values = value[4:-1].split(",")
                if len(values) == 3:
                    return hsl(
                        int(values[0]),
                        int(values[1].strip().rstrip("%")) / 100.0,
                        int(values[2].strip().rstrip("%")) / 100.0,
                    )
            except ValueError:
                pass
        else:
            try:
                return NAMED_COLOR[value.lower()]
            except KeyError:
                pass

    raise ValueError("Unknown color %s" % value)


NAMED_COLOR = {
    ALICEBLUE: rgb(0xF0, 0xF8, 0xFF),
    ANTIQUEWHITE: rgb(0xFA, 0xEB, 0xD7),
    AQUA: rgb(0x00, 0xFF, 0xFF),
    AQUAMARINE: rgb(0x7F, 0xFF, 0xD4),
    AZURE: rgb(0xF0, 0xFF, 0xFF),
    BEIGE: rgb(0xF5, 0xF5, 0xDC),
    BISQUE: rgb(0xFF, 0xE4, 0xC4),
    BLACK: rgb(0x00, 0x00, 0x00),
    BLANCHEDALMOND: rgb(0xFF, 0xEB, 0xCD),
    BLUE: rgb(0x00, 0x00, 0xFF),
    BLUEVIOLET: rgb(0x8A, 0x2B, 0xE2),
    BROWN: rgb(0xA5, 0x2A, 0x2A),
    BURLYWOOD: rgb(0xDE, 0xB8, 0x87),
    CADETBLUE: rgb(0x5F, 0x9E, 0xA0),
    CHARTREUSE: rgb(0x7F, 0xFF, 0x00),
    CHOCOLATE: rgb(0xD2, 0x69, 0x1E),
    CORAL: rgb(0xFF, 0x7F, 0x50),
    CORNFLOWERBLUE: rgb(0x64, 0x95, 0xED),
    CORNSILK: rgb(0xFF, 0xF8, 0xDC),
    CRIMSON: rgb(0xDC, 0x14, 0x3C),
    CYAN: rgb(0x00, 0xFF, 0xFF),
    DARKBLUE: rgb(0x00, 0x00, 0x8B),
    DARKCYAN: rgb(0x00, 0x8B, 0x8B),
    DARKGOLDENROD: rgb(0xB8, 0x86, 0x0B),
    DARKGRAY: rgb(0xA9, 0xA9, 0xA9),
    DARKGREY: rgb(0xA9, 0xA9, 0xA9),
    DARKGREEN: rgb(0x00, 0x64, 0x00),
    DARKKHAKI: rgb(0xBD, 0xB7, 0x6B),
    DARKMAGENTA: rgb(0x8B, 0x00, 0x8B),
    DARKOLIVEGREEN: rgb(0x55, 0x6B, 0x2F),
    DARKORANGE: rgb(0xFF, 0x8C, 0x00),
    DARKORCHID: rgb(0x99, 0x32, 0xCC),
    DARKRED: rgb(0x8B, 0x00, 0x00),
    DARKSALMON: rgb(0xE9, 0x96, 0x7A),
    DARKSEAGREEN: rgb(0x8F, 0xBC, 0x8F),
    DARKSLATEBLUE: rgb(0x48, 0x3D, 0x8B),
    DARKSLATEGRAY: rgb(0x2F, 0x4F, 0x4F),
    DARKSLATEGREY: rgb(0x2F, 0x4F, 0x4F),
    DARKTURQUOISE: rgb(0x00, 0xCE, 0xD1),
    DARKVIOLET: rgb(0x94, 0x00, 0xD3),
    DEEPPINK: rgb(0xFF, 0x14, 0x93),
    DEEPSKYBLUE: rgb(0x00, 0xBF, 0xFF),
    DIMGRAY: rgb(0x69, 0x69, 0x69),
    DIMGREY: rgb(0x69, 0x69, 0x69),
    DODGERBLUE: rgb(0x1E, 0x90, 0xFF),
    FIREBRICK: rgb(0xB2, 0x22, 0x22),
    FLORALWHITE: rgb(0xFF, 0xFA, 0xF0),
    FORESTGREEN: rgb(0x22, 0x8B, 0x22),
    FUCHSIA: rgb(0xFF, 0x00, 0xFF),
    GAINSBORO: rgb(0xDC, 0xDC, 0xDC),
    GHOSTWHITE: rgb(0xF8, 0xF8, 0xFF),
    GOLD: rgb(0xFF, 0xD7, 0x00),
    GOLDENROD: rgb(0xDA, 0xA5, 0x20),
    GRAY: rgb(0x80, 0x80, 0x80),
    GREY: rgb(0x80, 0x80, 0x80),
    GREEN: rgb(0x00, 0x80, 0x00),
    GREENYELLOW: rgb(0xAD, 0xFF, 0x2F),
    HONEYDEW: rgb(0xF0, 0xFF, 0xF0),
    HOTPINK: rgb(0xFF, 0x69, 0xB4),
    INDIANRED: rgb(0xCD, 0x5C, 0x5C),
    INDIGO: rgb(0x4B, 0x00, 0x82),
    IVORY: rgb(0xFF, 0xFF, 0xF0),
    KHAKI: rgb(0xF0, 0xE6, 0x8C),
    LAVENDER: rgb(0xE6, 0xE6, 0xFA),
    LAVENDERBLUSH: rgb(0xFF, 0xF0, 0xF5),
    LAWNGREEN: rgb(0x7C, 0xFC, 0x00),
    LEMONCHIFFON: rgb(0xFF, 0xFA, 0xCD),
    LIGHTBLUE: rgb(0xAD, 0xD8, 0xE6),
    LIGHTCORAL: rgb(0xF0, 0x80, 0x80),
    LIGHTCYAN: rgb(0xE0, 0xFF, 0xFF),
    LIGHTGOLDENRODYELLOW: rgb(0xFA, 0xFA, 0xD2),
    LIGHTGRAY: rgb(0xD3, 0xD3, 0xD3),
    LIGHTGREY: rgb(0xD3, 0xD3, 0xD3),
    LIGHTGREEN: rgb(0x90, 0xEE, 0x90),
    LIGHTPINK: rgb(0xFF, 0xB6, 0xC1),
    LIGHTSALMON: rgb(0xFF, 0xA0, 0x7A),
    LIGHTSEAGREEN: rgb(0x20, 0xB2, 0xAA),
    LIGHTSKYBLUE: rgb(0x87, 0xCE, 0xFA),
    LIGHTSLATEGRAY: rgb(0x77, 0x88, 0x99),
    LIGHTSLATEGREY: rgb(0x77, 0x88, 0x99),
    LIGHTSTEELBLUE: rgb(0xB0, 0xC4, 0xDE),
    LIGHTYELLOW: rgb(0xFF, 0xFF, 0xE0),
    LIME: rgb(0x00, 0xFF, 0x00),
    LIMEGREEN: rgb(0x32, 0xCD, 0x32),
    LINEN: rgb(0xFA, 0xF0, 0xE6),
    MAGENTA: rgb(0xFF, 0x00, 0xFF),
    MAROON: rgb(0x80, 0x00, 0x00),
    MEDIUMAQUAMARINE: rgb(0x66, 0xCD, 0xAA),
    MEDIUMBLUE: rgb(0x00, 0x00, 0xCD),
    MEDIUMORCHID: rgb(0xBA, 0x55, 0xD3),
    MEDIUMPURPLE: rgb(0x93, 0x70, 0xDB),
    MEDIUMSEAGREEN: rgb(0x3C, 0xB3, 0x71),
    MEDIUMSLATEBLUE: rgb(0x7B, 0x68, 0xEE),
    MEDIUMSPRINGGREEN: rgb(0x00, 0xFA, 0x9A),
    MEDIUMTURQUOISE: rgb(0x48, 0xD1, 0xCC),
    MEDIUMVIOLETRED: rgb(0xC7, 0x15, 0x85),
    MIDNIGHTBLUE: rgb(0x19, 0x19, 0x70),
    MINTCREAM: rgb(0xF5, 0xFF, 0xFA),
    MISTYROSE: rgb(0xFF, 0xE4, 0xE1),
    MOCCASIN: rgb(0xFF, 0xE4, 0xB5),
    NAVAJOWHITE: rgb(0xFF, 0xDE, 0xAD),
    NAVY: rgb(0x00, 0x00, 0x80),
    OLDLACE: rgb(0xFD, 0xF5, 0xE6),
    OLIVE: rgb(0x80, 0x80, 0x00),
    OLIVEDRAB: rgb(0x6B, 0x8E, 0x23),
    ORANGE: rgb(0xFF, 0xA5, 0x00),
    ORANGERED: rgb(0xFF, 0x45, 0x00),
    ORCHID: rgb(0xDA, 0x70, 0xD6),
    PALEGOLDENROD: rgb(0xEE, 0xE8, 0xAA),
    PALEGREEN: rgb(0x98, 0xFB, 0x98),
    PALETURQUOISE: rgb(0xAF, 0xEE, 0xEE),
    PALEVIOLETRED: rgb(0xDB, 0x70, 0x93),
    PAPAYAWHIP: rgb(0xFF, 0xEF, 0xD5),
    PEACHPUFF: rgb(0xFF, 0xDA, 0xB9),
    PERU: rgb(0xCD, 0x85, 0x3F),
    PINK: rgb(0xFF, 0xC0, 0xCB),
    PLUM: rgb(0xDD, 0xA0, 0xDD),
    POWDERBLUE: rgb(0xB0, 0xE0, 0xE6),
    PURPLE: rgb(0x80, 0x00, 0x80),
    REBECCAPURPLE: rgb(0x66, 0x33, 0x99),
    RED: rgb(0xFF, 0x00, 0x00),
    ROSYBROWN: rgb(0xBC, 0x8F, 0x8F),
    ROYALBLUE: rgb(0x41, 0x69, 0xE1),
    SADDLEBROWN: rgb(0x8B, 0x45, 0x13),
    SALMON: rgb(0xFA, 0x80, 0x72),
    SANDYBROWN: rgb(0xF4, 0xA4, 0x60),
    SEAGREEN: rgb(0x2E, 0x8B, 0x57),
    SEASHELL: rgb(0xFF, 0xF5, 0xEE),
    SIENNA: rgb(0xA0, 0x52, 0x2D),
    SILVER: rgb(0xC0, 0xC0, 0xC0),
    SKYBLUE: rgb(0x87, 0xCE, 0xEB),
    SLATEBLUE: rgb(0x6A, 0x5A, 0xCD),
    SLATEGRAY: rgb(0x70, 0x80, 0x90),
    SLATEGREY: rgb(0x70, 0x80, 0x90),
    SNOW: rgb(0xFF, 0xFA, 0xFA),
    SPRINGGREEN: rgb(0x00, 0xFF, 0x7F),
    STEELBLUE: rgb(0x46, 0x82, 0xB4),
    TAN: rgb(0xD2, 0xB4, 0x8C),
    TEAL: rgb(0x00, 0x80, 0x80),
    THISTLE: rgb(0xD8, 0xBF, 0xD8),
    TOMATO: rgb(0xFF, 0x63, 0x47),
    TURQUOISE: rgb(0x40, 0xE0, 0xD0),
    VIOLET: rgb(0xEE, 0x82, 0xEE),
    WHEAT: rgb(0xF5, 0xDE, 0xB3),
    WHITE: rgb(0xFF, 0xFF, 0xFF),
    WHITESMOKE: rgb(0xF5, 0xF5, 0xF5),
    YELLOW: rgb(0xFF, 0xFF, 0x00),
    YELLOWGREEN: rgb(0x9A, 0xCD, 0x32),
}


__all__ = [
    "Color",
    "rgba",
    "rgb",
    "hsla",
    "hsl",
    "color",
    "NAMED_COLOR",
    "TRANSPARENT",
] + [name.upper() for name in NAMED_COLOR.keys()]
