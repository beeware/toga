from toga.colors import TRANSPARENT
from toga.fonts import SYSTEM_DEFAULT_FONT_SIZE

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
        "font-family": f"{value.family}",
    }

    if value.size != SYSTEM_DEFAULT_FONT_SIZE:
        style["font-size"] = f"{value.size}pt"

    return style
