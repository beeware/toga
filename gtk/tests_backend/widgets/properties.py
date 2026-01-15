import pytest

from toga.colors import TRANSPARENT, rgb
from toga.fonts import Font
from toga.style.pack import BOTTOM, CENTER, JUSTIFY, LEFT, RIGHT, TOP
from toga_gtk.libs import GTK_VERSION, Gtk, parse_css_color


def toga_color(color):
    if color:
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            c = rgb(
                int(color.red * 255),
                int(color.green * 255),
                int(color.blue * 255),
                color.alpha,
            )
        else:  # pragma: no-cover-if-gtk3
            c = parse_css_color(color)

        # Background color of rgb(0,0,0,0.0) is TRANSPARENT.
        if c.r == 0 and c.g == 0 and c.b == 0 and c.a == 0.0:
            return TRANSPARENT
        else:
            return c
    else:
        return None


def toga_x_text_align(xalign, justify=None):
    try:
        return {
            0.0: JUSTIFY if justify == Gtk.Justification.FILL else LEFT,
            1.0: RIGHT,
            0.5: CENTER,
        }[xalign]
    except KeyError:
        pytest.fail(
            f"Can't interpret GTK x text alignment {xalign} with justify {justify}"
        )


def toga_y_text_align(yalign):
    try:
        return {
            0.0: TOP,
            0.5: CENTER,
            1.0: BOTTOM,
        }[yalign]
    except KeyError:
        pytest.fail(f"Can't interpret GTK y text alignment {yalign}")


def toga_text_align_from_justification(justify):
    return {
        Gtk.Justification.LEFT: LEFT,
        Gtk.Justification.RIGHT: RIGHT,
        Gtk.Justification.CENTER: CENTER,
        Gtk.Justification.FILL: JUSTIFY,
    }[justify]


def toga_font(font: str) -> Font:
    """
    Convert CSS font definition to a Toga Font object.

    Args:
        font (str): CSS font definition string, for example:
            {
              font-family: "Helvetica Neue";
              font-size: 14px;
              font-style: normal;
              font-variant: normal;
              font-weight: 400;
            }

    Returns:
        Font: A Toga Font object with the parsed properties
    """
    css_dict = {}
    for line in font.split("\n"):
        line = line.strip()
        if ":" in line:
            property_name, value = line.split(":", 1)
            property_name = property_name.strip()
            value = value.strip().rstrip(";")
            css_dict[property_name] = value

    family_font_value = css_dict.get("font-family", "")
    size_font_value = css_dict.get("font-size", -1)
    style_font_value = css_dict.get("font-style", "normal")
    # GTK4 stores small-caps information in font-variant-caps.
    variant_font_value = css_dict.get("font-variant-caps", None) or css_dict.get(
        "font-variant", "normal"
    )
    weight_font_value = css_dict.get("font-weight", "normal")

    if variant_font_value == "initial":
        variant_font_value = "normal"

    if weight_font_value == "400":
        weight_font_value = "normal"
    elif weight_font_value == "700":
        weight_font_value = "bold"

    return Font(
        family=family_font_value,
        size=size_font_value,
        style=style_font_value,
        variant=variant_font_value,
        weight=weight_font_value,
    )
