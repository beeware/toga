from travertino.constants import (
    ABSOLUTE_FONT_SIZES,
    RELATIVE_FONT_SIZES,
)

from toga.colors import TRANSPARENT
from toga.fonts import SYSTEM_DEFAULT_FONT_SIZE

from ..libs import GTK_VERSION

if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
    TOGA_DEFAULT_STYLES = b"""
    .toga-detailed-list-floating-buttons {
        min-width: 24px;
        min-height: 24px;
        color: white;
        background: #000000;
        border-style: none;
        border-radius: 0;
        opacity: 0.60;
    }
    """
else:  # pragma: no-cover-if-gtk3
    TOGA_DEFAULT_STYLES = """
    .toga-detailed-list-floating-buttons {
        min-width: 24px;
        min-height: 24px;
        color: white;
        background: #000000;
        border-style: none;
        border-radius: 0;
        opacity: 0.60;
    }
    """


def get_color_css(value):
    if value is None:
        return None
    else:
        return {
            "color": f"rgba({value.r}, {value.g}, {value.b}, {value.a})",
        }


def get_background_color_css(value):
    if value == TRANSPARENT:
        return {
            "background-color": "rgba(0, 0, 0, 0)",
            "background-image": "none",
        }
    elif value is None:
        return None
    else:
        return {
            "background-color": f"rgba({value.r}, {value.g}, {value.b}, {value.a})",
            "background-image": "none",
        }


def get_font_css(value):
    style = {
        "font-style": f"{value.style}",
        "font-variant": f"{value.variant}",
        "font-weight": f"{value.weight}",
        "font-family": f"{value.family!r}",
    }

    # If value is an absolute or relative keyword, use those to set size instead
    if value.size in ABSOLUTE_FONT_SIZES or value.size in RELATIVE_FONT_SIZES:
        style["font-size"] = f"{value.size}"
    elif value.size != SYSTEM_DEFAULT_FONT_SIZE:
        style["font-size"] = f"{value.size}pt"

    return style
