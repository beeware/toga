from __future__ import annotations

import string

from .constants import *  # noqa: F403


def _clamp(value, lower, upper):
    return min(upper, max(lower, value))


class Color:
    """A base class for all colorspace representations."""

    def __eq__(self, other):
        try:
            c1 = self.rgb
            c2 = other.rgb

            return c1.r == c2.r and c1.g == c2.g and c1.b == c2.b and c1.a == c2.a
        except AttributeError:
            return False

    @staticmethod
    def _validate_zero_to_one(name, value):
        try:
            return _clamp(float(value), 0.0, 1.0)
        except (ValueError, TypeError) as exc:
            raise TypeError(
                f"Value for {name} must be a number; got {value!r}"
            ) from exc

    @property
    def a(self) -> float:
        return self._a

    @property
    def rgba(self) -> rgb:
        return self.rgb

    @property
    def hsla(self) -> hsl:
        return self.hsl

    def blend_over(self, back_color: Color) -> rgb:
        """Perform the "over" straight alpha blending operation, compositing
        the front color over the back color.

        **Straight alpha blending** is not the same as
        **Premultiplied alpha blending**, see:
        https://en.wikipedia.org/wiki/Alpha_compositing#Straight_versus_premultiplied

        :param back_color: The background color.

        :returns: The blended color.
        """
        # The blending operation implemented here is the "over" operation and
        # replicates CSS's rgba mechanism. For the formulae used here, see:
        # https://en.wikipedia.org/wiki/Alpha_compositing#Description

        # Convert the input colors to rgba in order to do the calculation.
        front_color = self.rgb
        back_color = back_color.rgb

        if front_color.a == 1:
            # If the front color is fully opaque then the result will be the same as
            # front color.
            return front_color

        blended_alpha = _clamp(
            front_color.a + ((1 - front_color.a) * back_color.a),
            0.0,
            1.0,
        )

        if blended_alpha == 0:
            # Don't further blend the color, to prevent divide by 0.
            return rgb(0, 0, 0, 0)
        else:
            bands = {}
            for band in "rgb":
                front = getattr(front_color, band)
                back = getattr(back_color, band)
                bands[band] = (
                    (front * front_color.a)
                    + (back * back_color.a * (1 - front_color.a))
                ) / blended_alpha

            return rgb(**bands, a=blended_alpha)

    def unblend_over(self, back_color: Color, front_color_alpha: float) -> rgb:
        """Perform the reverse of the "over" straight alpha blending operation,
        returning the front color.

        Note: Unblending of blended colors might produce front color with slightly
        imprecise component values compared to the original front color. This is
        due to the loss of some amount of precision during the calculation and
        conversion process between the different color formats. For example,
        unblending of an hsla blended color might might produce a slightly imprecise
        original front color, since the alpha blending and unblending is calculated
        after conversion to rgba values.

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

        blended_color = self.rgb
        back_color = back_color.rgb
        if not 0 < front_color_alpha <= 1:
            raise ValueError(
                "The value of front_color_alpha must be within the range of (0, 1]."
            )
        else:
            bands = {}
            for band in "rgb":
                blended = getattr(blended_color, band)
                back = getattr(back_color, band)
                bands[band] = (
                    (blended * blended_color.a)
                    - (back * back_color.a * (1 - front_color_alpha))
                ) / front_color_alpha

            return rgb(**bands, a=front_color_alpha)


class rgb(Color):
    """A representation of an RGB(A) color."""

    def __init__(self, r, g, b, a=1.0):
        self._r = self._validate_band("red", r)
        self._g = self._validate_band("green", g)
        self._b = self._validate_band("blue", b)
        self._a = self._validate_zero_to_one("alpha", a)

    def __hash__(self):
        return hash(("RGB-color", self.r, self.g, self.b, self.a))

    def __repr__(self):
        return f"rgb({self.r}, {self.g}, {self.b}, {self.a})"

    def __str__(self):
        return f"rgb({self.r} {self.g} {self.b} / {self.a})"

    @staticmethod
    def _validate_band(name, value):
        try:
            return _clamp(round(value), 0, 255)
        except TypeError as exc:
            raise TypeError(
                f"Value for {name} must be a number; got {value!r}"
            ) from exc

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    @property
    def rgb(self) -> rgb:
        return self

    @property
    def hsl(self) -> hsl:
        if cached := getattr(self, "_hsl", None):
            return cached

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

        self._hsl = hsl(hue, saturation, lightness, self.a)
        return self._hsl


# As in CSS, rgba is simply a direct alias for rgb.
rgba = rgb


class hsl(Color):
    """A representation of an HSL(A) color."""

    def __init__(self, h, s, l, a=1.0):  # noqa: E741
        try:
            self._h = round(h) % 360
        except TypeError as exc:
            raise TypeError(f"Value for hue must be a number; got {h!r}") from exc
        self._s = self._validate_zero_to_one("saturation", s)
        self._l = self._validate_zero_to_one("lightness", l)
        self._a = self._validate_zero_to_one("alpha", a)

    def __hash__(self):
        return hash(("HSL-color", self.h, self.s, self.l, self.a))

    def __repr__(self):
        return f"hsl({self.h}, {self.s}, {self.l}, {self.a})"

    def __str__(self):
        return f"hsl({self.h} {round(self.s * 100)}% {round(self.l * 100)}% / {self.a})"

    @property
    def h(self) -> int:
        return self._h

    @property
    def s(self) -> float:
        return self._s

    @property
    def l(self) -> float:  # noqa: E743
        return self._l

    @property
    def hsl(self) -> hsl:
        return self

    @property
    def rgb(self) -> rgb:
        if cached := getattr(self, "_rgb", None):
            return cached

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
            r, g, b = x + m, m, c + m
        else:
            r, g, b = c + m, m, x + m

        self._rgb = rgb(r * 0xFF, g * 0xFF, b * 0xFF, self.a)
        return self._rgb


# As in CSS, hsla is simply a direct alias for hsl.
hsla = hsl


def color(value: str) -> Color:
    """Parse a color from a value.

    Accepts:
    * An rgb() or hsl() instance
    * A named color
    * '#rgb'
    * '#rgba'
    * '#rrggbb'
    * '#rrggbbaa'
    """

    if isinstance(value, Color):
        return value

    elif isinstance(value, str):
        if result := NAMED_COLOR.get(value.lower()):
            return result

        pound, *digits = value
        if pound == "#" and all(d in string.hexdigits for d in digits):
            if len(digits) in {3, 4}:
                r, g, b, *a = digits
                return rgb(
                    r=int(f"{r}{r}", 16),
                    g=int(f"{g}{g}", 16),
                    b=int(f"{b}{b}", 16),
                    a=(int(f"{a[0]}{a[0]}", 16) / 0xFF) if a else 1.0,
                )

            elif len(digits) in {6, 8}:
                r1, r2, g1, g2, b1, b2, *a = digits
                return rgb(
                    r=int(f"{r1}{r2}", 16),
                    g=int(f"{g1}{g2}", 16),
                    b=int(f"{b1}{b2}", 16),
                    a=(int(f"{a[0]}{a[1]}", 16) / 0xFF) if a else 1.0,
                )

    raise ValueError(f"Unknown color: {value!r}")


NAMED_COLOR = {
    ALICEBLUE: rgb(0xF0, 0xF8, 0xFF),  # noqa: F405
    ANTIQUEWHITE: rgb(0xFA, 0xEB, 0xD7),  # noqa: F405
    AQUA: rgb(0x00, 0xFF, 0xFF),  # noqa: F405
    AQUAMARINE: rgb(0x7F, 0xFF, 0xD4),  # noqa: F405
    AZURE: rgb(0xF0, 0xFF, 0xFF),  # noqa: F405
    BEIGE: rgb(0xF5, 0xF5, 0xDC),  # noqa: F405
    BISQUE: rgb(0xFF, 0xE4, 0xC4),  # noqa: F405
    BLACK: rgb(0x00, 0x00, 0x00),  # noqa: F405
    BLANCHEDALMOND: rgb(0xFF, 0xEB, 0xCD),  # noqa: F405
    BLUE: rgb(0x00, 0x00, 0xFF),  # noqa: F405
    BLUEVIOLET: rgb(0x8A, 0x2B, 0xE2),  # noqa: F405
    BROWN: rgb(0xA5, 0x2A, 0x2A),  # noqa: F405
    BURLYWOOD: rgb(0xDE, 0xB8, 0x87),  # noqa: F405
    CADETBLUE: rgb(0x5F, 0x9E, 0xA0),  # noqa: F405
    CHARTREUSE: rgb(0x7F, 0xFF, 0x00),  # noqa: F405
    CHOCOLATE: rgb(0xD2, 0x69, 0x1E),  # noqa: F405
    CORAL: rgb(0xFF, 0x7F, 0x50),  # noqa: F405
    CORNFLOWERBLUE: rgb(0x64, 0x95, 0xED),  # noqa: F405
    CORNSILK: rgb(0xFF, 0xF8, 0xDC),  # noqa: F405
    CRIMSON: rgb(0xDC, 0x14, 0x3C),  # noqa: F405
    CYAN: rgb(0x00, 0xFF, 0xFF),  # noqa: F405
    DARKBLUE: rgb(0x00, 0x00, 0x8B),  # noqa: F405
    DARKCYAN: rgb(0x00, 0x8B, 0x8B),  # noqa: F405
    DARKGOLDENROD: rgb(0xB8, 0x86, 0x0B),  # noqa: F405
    DARKGRAY: rgb(0xA9, 0xA9, 0xA9),  # noqa: F405
    DARKGREY: rgb(0xA9, 0xA9, 0xA9),  # noqa: F405
    DARKGREEN: rgb(0x00, 0x64, 0x00),  # noqa: F405
    DARKKHAKI: rgb(0xBD, 0xB7, 0x6B),  # noqa: F405
    DARKMAGENTA: rgb(0x8B, 0x00, 0x8B),  # noqa: F405
    DARKOLIVEGREEN: rgb(0x55, 0x6B, 0x2F),  # noqa: F405
    DARKORANGE: rgb(0xFF, 0x8C, 0x00),  # noqa: F405
    DARKORCHID: rgb(0x99, 0x32, 0xCC),  # noqa: F405
    DARKRED: rgb(0x8B, 0x00, 0x00),  # noqa: F405
    DARKSALMON: rgb(0xE9, 0x96, 0x7A),  # noqa: F405
    DARKSEAGREEN: rgb(0x8F, 0xBC, 0x8F),  # noqa: F405
    DARKSLATEBLUE: rgb(0x48, 0x3D, 0x8B),  # noqa: F405
    DARKSLATEGRAY: rgb(0x2F, 0x4F, 0x4F),  # noqa: F405
    DARKSLATEGREY: rgb(0x2F, 0x4F, 0x4F),  # noqa: F405
    DARKTURQUOISE: rgb(0x00, 0xCE, 0xD1),  # noqa: F405
    DARKVIOLET: rgb(0x94, 0x00, 0xD3),  # noqa: F405
    DEEPPINK: rgb(0xFF, 0x14, 0x93),  # noqa: F405
    DEEPSKYBLUE: rgb(0x00, 0xBF, 0xFF),  # noqa: F405
    DIMGRAY: rgb(0x69, 0x69, 0x69),  # noqa: F405
    DIMGREY: rgb(0x69, 0x69, 0x69),  # noqa: F405
    DODGERBLUE: rgb(0x1E, 0x90, 0xFF),  # noqa: F405
    FIREBRICK: rgb(0xB2, 0x22, 0x22),  # noqa: F405
    FLORALWHITE: rgb(0xFF, 0xFA, 0xF0),  # noqa: F405
    FORESTGREEN: rgb(0x22, 0x8B, 0x22),  # noqa: F405
    FUCHSIA: rgb(0xFF, 0x00, 0xFF),  # noqa: F405
    GAINSBORO: rgb(0xDC, 0xDC, 0xDC),  # noqa: F405
    GHOSTWHITE: rgb(0xF8, 0xF8, 0xFF),  # noqa: F405
    GOLD: rgb(0xFF, 0xD7, 0x00),  # noqa: F405
    GOLDENROD: rgb(0xDA, 0xA5, 0x20),  # noqa: F405
    GRAY: rgb(0x80, 0x80, 0x80),  # noqa: F405
    GREY: rgb(0x80, 0x80, 0x80),  # noqa: F405
    GREEN: rgb(0x00, 0x80, 0x00),  # noqa: F405
    GREENYELLOW: rgb(0xAD, 0xFF, 0x2F),  # noqa: F405
    HONEYDEW: rgb(0xF0, 0xFF, 0xF0),  # noqa: F405
    HOTPINK: rgb(0xFF, 0x69, 0xB4),  # noqa: F405
    INDIANRED: rgb(0xCD, 0x5C, 0x5C),  # noqa: F405
    INDIGO: rgb(0x4B, 0x00, 0x82),  # noqa: F405
    IVORY: rgb(0xFF, 0xFF, 0xF0),  # noqa: F405
    KHAKI: rgb(0xF0, 0xE6, 0x8C),  # noqa: F405
    LAVENDER: rgb(0xE6, 0xE6, 0xFA),  # noqa: F405
    LAVENDERBLUSH: rgb(0xFF, 0xF0, 0xF5),  # noqa: F405
    LAWNGREEN: rgb(0x7C, 0xFC, 0x00),  # noqa: F405
    LEMONCHIFFON: rgb(0xFF, 0xFA, 0xCD),  # noqa: F405
    LIGHTBLUE: rgb(0xAD, 0xD8, 0xE6),  # noqa: F405
    LIGHTCORAL: rgb(0xF0, 0x80, 0x80),  # noqa: F405
    LIGHTCYAN: rgb(0xE0, 0xFF, 0xFF),  # noqa: F405
    LIGHTGOLDENRODYELLOW: rgb(0xFA, 0xFA, 0xD2),  # noqa: F405
    LIGHTGRAY: rgb(0xD3, 0xD3, 0xD3),  # noqa: F405
    LIGHTGREY: rgb(0xD3, 0xD3, 0xD3),  # noqa: F405
    LIGHTGREEN: rgb(0x90, 0xEE, 0x90),  # noqa: F405
    LIGHTPINK: rgb(0xFF, 0xB6, 0xC1),  # noqa: F405
    LIGHTSALMON: rgb(0xFF, 0xA0, 0x7A),  # noqa: F405
    LIGHTSEAGREEN: rgb(0x20, 0xB2, 0xAA),  # noqa: F405
    LIGHTSKYBLUE: rgb(0x87, 0xCE, 0xFA),  # noqa: F405
    LIGHTSLATEGRAY: rgb(0x77, 0x88, 0x99),  # noqa: F405
    LIGHTSLATEGREY: rgb(0x77, 0x88, 0x99),  # noqa: F405
    LIGHTSTEELBLUE: rgb(0xB0, 0xC4, 0xDE),  # noqa: F405
    LIGHTYELLOW: rgb(0xFF, 0xFF, 0xE0),  # noqa: F405
    LIME: rgb(0x00, 0xFF, 0x00),  # noqa: F405
    LIMEGREEN: rgb(0x32, 0xCD, 0x32),  # noqa: F405
    LINEN: rgb(0xFA, 0xF0, 0xE6),  # noqa: F405
    MAGENTA: rgb(0xFF, 0x00, 0xFF),  # noqa: F405
    MAROON: rgb(0x80, 0x00, 0x00),  # noqa: F405
    MEDIUMAQUAMARINE: rgb(0x66, 0xCD, 0xAA),  # noqa: F405
    MEDIUMBLUE: rgb(0x00, 0x00, 0xCD),  # noqa: F405
    MEDIUMORCHID: rgb(0xBA, 0x55, 0xD3),  # noqa: F405
    MEDIUMPURPLE: rgb(0x93, 0x70, 0xDB),  # noqa: F405
    MEDIUMSEAGREEN: rgb(0x3C, 0xB3, 0x71),  # noqa: F405
    MEDIUMSLATEBLUE: rgb(0x7B, 0x68, 0xEE),  # noqa: F405
    MEDIUMSPRINGGREEN: rgb(0x00, 0xFA, 0x9A),  # noqa: F405
    MEDIUMTURQUOISE: rgb(0x48, 0xD1, 0xCC),  # noqa: F405
    MEDIUMVIOLETRED: rgb(0xC7, 0x15, 0x85),  # noqa: F405
    MIDNIGHTBLUE: rgb(0x19, 0x19, 0x70),  # noqa: F405
    MINTCREAM: rgb(0xF5, 0xFF, 0xFA),  # noqa: F405
    MISTYROSE: rgb(0xFF, 0xE4, 0xE1),  # noqa: F405
    MOCCASIN: rgb(0xFF, 0xE4, 0xB5),  # noqa: F405
    NAVAJOWHITE: rgb(0xFF, 0xDE, 0xAD),  # noqa: F405
    NAVY: rgb(0x00, 0x00, 0x80),  # noqa: F405
    OLDLACE: rgb(0xFD, 0xF5, 0xE6),  # noqa: F405
    OLIVE: rgb(0x80, 0x80, 0x00),  # noqa: F405
    OLIVEDRAB: rgb(0x6B, 0x8E, 0x23),  # noqa: F405
    ORANGE: rgb(0xFF, 0xA5, 0x00),  # noqa: F405
    ORANGERED: rgb(0xFF, 0x45, 0x00),  # noqa: F405
    ORCHID: rgb(0xDA, 0x70, 0xD6),  # noqa: F405
    PALEGOLDENROD: rgb(0xEE, 0xE8, 0xAA),  # noqa: F405
    PALEGREEN: rgb(0x98, 0xFB, 0x98),  # noqa: F405
    PALETURQUOISE: rgb(0xAF, 0xEE, 0xEE),  # noqa: F405
    PALEVIOLETRED: rgb(0xDB, 0x70, 0x93),  # noqa: F405
    PAPAYAWHIP: rgb(0xFF, 0xEF, 0xD5),  # noqa: F405
    PEACHPUFF: rgb(0xFF, 0xDA, 0xB9),  # noqa: F405
    PERU: rgb(0xCD, 0x85, 0x3F),  # noqa: F405
    PINK: rgb(0xFF, 0xC0, 0xCB),  # noqa: F405
    PLUM: rgb(0xDD, 0xA0, 0xDD),  # noqa: F405
    POWDERBLUE: rgb(0xB0, 0xE0, 0xE6),  # noqa: F405
    PURPLE: rgb(0x80, 0x00, 0x80),  # noqa: F405
    REBECCAPURPLE: rgb(0x66, 0x33, 0x99),  # noqa: F405
    RED: rgb(0xFF, 0x00, 0x00),  # noqa: F405
    ROSYBROWN: rgb(0xBC, 0x8F, 0x8F),  # noqa: F405
    ROYALBLUE: rgb(0x41, 0x69, 0xE1),  # noqa: F405
    SADDLEBROWN: rgb(0x8B, 0x45, 0x13),  # noqa: F405
    SALMON: rgb(0xFA, 0x80, 0x72),  # noqa: F405
    SANDYBROWN: rgb(0xF4, 0xA4, 0x60),  # noqa: F405
    SEAGREEN: rgb(0x2E, 0x8B, 0x57),  # noqa: F405
    SEASHELL: rgb(0xFF, 0xF5, 0xEE),  # noqa: F405
    SIENNA: rgb(0xA0, 0x52, 0x2D),  # noqa: F405
    SILVER: rgb(0xC0, 0xC0, 0xC0),  # noqa: F405
    SKYBLUE: rgb(0x87, 0xCE, 0xEB),  # noqa: F405
    SLATEBLUE: rgb(0x6A, 0x5A, 0xCD),  # noqa: F405
    SLATEGRAY: rgb(0x70, 0x80, 0x90),  # noqa: F405
    SLATEGREY: rgb(0x70, 0x80, 0x90),  # noqa: F405
    SNOW: rgb(0xFF, 0xFA, 0xFA),  # noqa: F405
    SPRINGGREEN: rgb(0x00, 0xFF, 0x7F),  # noqa: F405
    STEELBLUE: rgb(0x46, 0x82, 0xB4),  # noqa: F405
    TAN: rgb(0xD2, 0xB4, 0x8C),  # noqa: F405
    TEAL: rgb(0x00, 0x80, 0x80),  # noqa: F405
    THISTLE: rgb(0xD8, 0xBF, 0xD8),  # noqa: F405
    TOMATO: rgb(0xFF, 0x63, 0x47),  # noqa: F405
    TURQUOISE: rgb(0x40, 0xE0, 0xD0),  # noqa: F405
    VIOLET: rgb(0xEE, 0x82, 0xEE),  # noqa: F405
    WHEAT: rgb(0xF5, 0xDE, 0xB3),  # noqa: F405
    WHITE: rgb(0xFF, 0xFF, 0xFF),  # noqa: F405
    WHITESMOKE: rgb(0xF5, 0xF5, 0xF5),  # noqa: F405
    YELLOW: rgb(0xFF, 0xFF, 0x00),  # noqa: F405
    YELLOWGREEN: rgb(0x9A, 0xCD, 0x32),  # noqa: F405
}


__all__ = [
    "Color",
    "rgba",
    "rgb",
    "hsla",
    "hsl",
    "color",
    "NAMED_COLOR",
    "TRANSPARENT",  # noqa: F405
] + [name.upper() for name in NAMED_COLOR]
