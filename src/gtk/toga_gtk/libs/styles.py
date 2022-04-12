from . import Gtk

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


def apply_gtk_style(style_context, style, name):
    # creating StyleProvider (i.e CssProvider)
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(style.encode())

    # setting the StyleProvider to StyleContext
    style_context.add_provider(
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER,
    )
    style_context.add_class(name)


def get_color_css(value):
    return (
        ".toga-color {"
        f"color: rgba({value.r}, {value.g}, {value.b}, {value.a});"
        "}"
    )


def get_bg_color_css(value):
    return (
        ".toga-bg-color {"
        f"background-color: rgba({value.r}, {value.g}, {value.b}, {value.a});"
        "background-image: none;"
        "}"
    )


def get_font_css(value):
    style = [
        ".toga-font { "
        f"font-style: {value.style}; "
        f"font-variant: {value.variant}; "
        f"font-weight: {value.weight}; "
        f"font-family: {value.family}; "
    ]

    if value.size != -1:
        style.append(f"font-size: {value.size}px; ")

    style.append("}")

    return " ".join(style)
